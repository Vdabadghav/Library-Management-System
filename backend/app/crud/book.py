"""
CRUD operations for Book model
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional
from app.models.models import Book, Author, Genre, Language
from app.schemas.schemas import BookCreate, BookUpdate, BookResponse
from app.utils.exceptions import NotFoundError, DuplicateEntryError, DatabaseError, BusinessLogicError
from app.core.logging_config import logger


def create_book(db: Session, book_create: BookCreate) -> Book:
    """Create a new book"""
    try:
        # Check if ISBN already exists
        existing_book = db.query(Book).filter(Book.isbn == book_create.isbn).first()
        if existing_book:
            raise DuplicateEntryError(f"Book with ISBN '{book_create.isbn}' already exists")

        # Verify language exists
        language = db.query(Language).filter(Language.id == book_create.language_id).first()
        if not language:
            raise NotFoundError(f"Language with ID {book_create.language_id} not found")

        # Create book
        db_book = Book(
            isbn=book_create.isbn,
            title=book_create.title,
            language_id=book_create.language_id,
            publisher=book_create.publisher,
            publication_year=book_create.publication_year,
            edition=book_create.edition,
            shelf_location=book_create.shelf_location,
            total_copies=book_create.total_copies
        )

        # Add authors
        if book_create.author_ids:
            authors = db.query(Author).filter(Author.id.in_(book_create.author_ids)).all()
            if len(authors) != len(book_create.author_ids):
                raise NotFoundError("One or more authors not found")
            db_book.authors = authors

        # Add genres
        if book_create.genre_ids:
            genres = db.query(Genre).filter(Genre.id.in_(book_create.genre_ids)).all()
            if len(genres) != len(book_create.genre_ids):
                raise NotFoundError("One or more genres not found")
            db_book.genres = genres

        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        logger.info(f"Book created: {db_book.title} (ISBN: {db_book.isbn})")
        return db_book
    except (DuplicateEntryError, NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error creating book: {str(e)}")
        raise


def get_book_by_id(db: Session, book_id: int) -> Book:
    """Get book by ID"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundError(f"Book with ID {book_id} not found")
    return book


def get_book_by_isbn(db: Session, isbn: str) -> Book:
    """Get book by ISBN"""
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        raise NotFoundError(f"Book with ISBN '{isbn}' not found")
    return book


def _book_query(db: Session):
    return db.query(Book).options(
        joinedload(Book.authors),
        joinedload(Book.genres),
        joinedload(Book.language),
    )


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """Get all books with pagination"""
    return _book_query(db).offset(skip).limit(limit).all()


def search_books(
    db: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    language_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Book]:
    """Search books by various criteria"""
    query = _book_query(db)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if author:
        query = query.join(Book.authors).filter(
            Author.full_name.ilike(f"%{author}%")
        )

    if genre:
        query = query.join(Book.genres).filter(
            Genre.name.ilike(f"%{genre}%")
        )

    if language_id:
        query = query.filter(Book.language_id == language_id)

    return query.offset(skip).limit(limit).all()


def book_to_detail(db: Session, book: Book) -> dict:
    """Serialize a book with availability and related catalog data."""
    available = get_available_copies(db, book.id)
    data = BookResponse.model_validate(book).model_dump()
    data["copies_available"] = available
    data["copies_issued"] = book.total_copies - available
    return data


def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Book:
    """Update book information"""
    try:
        book = get_book_by_id(db, book_id)

        # Update basic fields
        update_data = book_update.model_dump(
            exclude_unset=True,
            exclude={'author_ids', 'genre_ids'}
        )
        for field, value in update_data.items():
            if value is not None:
                setattr(book, field, value)

        # Update authors
        if book_update.author_ids is not None:
            authors = db.query(Author).filter(Author.id.in_(book_update.author_ids)).all()
            if len(authors) != len(book_update.author_ids):
                raise NotFoundError("One or more authors not found")
            book.authors = authors

        # Update genres
        if book_update.genre_ids is not None:
            genres = db.query(Genre).filter(Genre.id.in_(book_update.genre_ids)).all()
            if len(genres) != len(book_update.genre_ids):
                raise NotFoundError("One or more genres not found")
            book.genres = genres

        book.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(book)
        logger.info(f"Book updated: {book.title}")
        return book
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating book: {str(e)}")
        raise


def delete_book(db: Session, book_id: int) -> bool:
    """Delete a book (only if no copies are issued)"""
    try:
        book = get_book_by_id(db, book_id)

        # Check if any copies are issued
        from app.models.models import BookIssue
        issued_copies = db.query(BookIssue).filter(
            BookIssue.book_id == book_id,
            BookIssue.status == "issued"
        ).count()

        if issued_copies > 0:
            raise BusinessLogicError(
                f"Cannot delete book. {issued_copies} copy/copies are currently issued."
            )

        db.delete(book)
        db.commit()
        logger.info(f"Book deleted: {book.title}")
        return True
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error deleting book: {str(e)}")
        raise


def get_available_copies(db: Session, book_id: int) -> int:
    """Get number of available copies of a book"""
    from app.models.models import BookIssue
    book = get_book_by_id(db, book_id)

    issued_copies = db.query(BookIssue).filter(
        BookIssue.book_id == book_id,
        BookIssue.status == "issued"
    ).count()

    return book.total_copies - issued_copies


def update_total_copies(db: Session, book_id: int, new_total: int) -> Book:
    """Update total copies of a book"""
    try:
        book = get_book_by_id(db, book_id)

        # Validate new total is not less than issued copies
        from app.models.models import BookIssue
        issued_copies = db.query(BookIssue).filter(
            BookIssue.book_id == book_id,
            BookIssue.status == "issued"
        ).count()

        if new_total < issued_copies:
            raise BusinessLogicError(
                f"Cannot reduce total copies below issued copies ({issued_copies})"
            )

        book.total_copies = new_total
        book.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(book)
        logger.info(f"Book total copies updated: {book.title} -> {new_total}")
        return book
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating total copies: {str(e)}")
        raise

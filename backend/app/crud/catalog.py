"""
CRUD operations for Language, Genre, and Author models
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime

from app.models.models import Language, Genre, Author, Book
from app.utils.exceptions import NotFoundError, DuplicateEntryError, BusinessLogicError
from app.core.logging_config import logger


# ==================== Language CRUD ====================
def create_language(db: Session, name: str, code: str) -> Language:
    """Create a new language"""
    try:
        existing = db.query(Language).filter(
            (Language.name == name) | (Language.code == code)
        ).first()
        if existing:
            raise DuplicateEntryError(f"Language '{name}' with code '{code}' already exists")

        language = Language(name=name, code=code)
        db.add(language)
        db.commit()
        db.refresh(language)
        logger.info(f"Language created: {language.name}")
        return language
    except (DuplicateEntryError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error creating language: {str(e)}")
        raise


def get_language_by_id(db: Session, language_id: int) -> Language:
    """Get language by ID"""
    language = db.query(Language).filter(Language.id == language_id).first()
    if not language:
        raise NotFoundError(f"Language with ID {language_id} not found")
    return language


def get_all_languages(db: Session) -> List[Language]:
    """Get all languages"""
    return db.query(Language).all()


def delete_language(db: Session, language_id: int) -> bool:
    """Delete language (only if not in use)"""
    try:
        language = get_language_by_id(db, language_id)

        # Check if language is in use
        book_count = db.query(Book).filter(Book.language_id == language_id).count()
        if book_count > 0:
            raise BusinessLogicError(
                f"Cannot delete language. {book_count} book(s) are using this language."
            )

        db.delete(language)
        db.commit()
        logger.info(f"Language deleted: {language.name}")
        return True
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error deleting language: {str(e)}")
        raise


# ==================== Genre CRUD ====================
def create_genre(db: Session, name: str, description: str = None) -> Genre:
    """Create a new genre"""
    try:
        existing = db.query(Genre).filter(Genre.name == name).first()
        if existing:
            raise DuplicateEntryError(f"Genre '{name}' already exists")

        genre = Genre(name=name, description=description)
        db.add(genre)
        db.commit()
        db.refresh(genre)
        logger.info(f"Genre created: {genre.name}")
        return genre
    except (DuplicateEntryError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error creating genre: {str(e)}")
        raise


def get_genre_by_id(db: Session, genre_id: int) -> Genre:
    """Get genre by ID"""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise NotFoundError(f"Genre with ID {genre_id} not found")
    return genre


def get_all_genres(db: Session) -> List[Genre]:
    """Get all genres"""
    return db.query(Genre).all()


def update_genre(db: Session, genre_id: int, name: str = None, description: str = None) -> Genre:
    """Update genre"""
    try:
        genre = get_genre_by_id(db, genre_id)

        if name and name != genre.name:
            existing = db.query(Genre).filter(
                (Genre.name == name) & (Genre.id != genre_id)
            ).first()
            if existing:
                raise DuplicateEntryError(f"Genre '{name}' already exists")
            genre.name = name

        if description is not None:
            genre.description = description

        db.commit()
        db.refresh(genre)
        logger.info(f"Genre updated: {genre.name}")
        return genre
    except (NotFoundError, DuplicateEntryError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating genre: {str(e)}")
        raise


def delete_genre(db: Session, genre_id: int) -> bool:
    """Delete genre (only if not in use)"""
    try:
        genre = get_genre_by_id(db, genre_id)

        # Check if genre is in use
        book_count = db.query(Book).join(Book.genres).filter(Genre.id == genre_id).count()
        if book_count > 0:
            raise BusinessLogicError(
                f"Cannot delete genre. {book_count} book(s) are using this genre."
            )

        db.delete(genre)
        db.commit()
        logger.info(f"Genre deleted: {genre.name}")
        return True
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error deleting genre: {str(e)}")
        raise


# ==================== Author CRUD ====================
def create_author(db: Session, full_name: str, biography: str = None) -> Author:
    """Create a new author"""
    try:
        author = Author(full_name=full_name, biography=biography)
        db.add(author)
        db.commit()
        db.refresh(author)
        logger.info(f"Author created: {author.full_name}")
        return author
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating author: {str(e)}")
        raise


def get_author_by_id(db: Session, author_id: int) -> Author:
    """Get author by ID"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise NotFoundError(f"Author with ID {author_id} not found")
    return author


def get_all_authors(db: Session) -> List[Author]:
    """Get all authors"""
    return db.query(Author).all()


def update_author(db: Session, author_id: int, full_name: str = None, biography: str = None) -> Author:
    """Update author"""
    try:
        author = get_author_by_id(db, author_id)

        if full_name:
            author.full_name = full_name

        if biography is not None:
            author.biography = biography

        db.commit()
        db.refresh(author)
        logger.info(f"Author updated: {author.full_name}")
        return author
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating author: {str(e)}")
        raise


def delete_author(db: Session, author_id: int) -> bool:
    """Delete author (only if not linked to any books)"""
    try:
        author = get_author_by_id(db, author_id)

        # Check if author is linked to books
        book_count = db.query(Book).join(Book.authors).filter(Author.id == author_id).count()
        if book_count > 0:
            raise BusinessLogicError(
                f"Cannot delete author. {book_count} book(s) are linked to this author."
            )

        db.delete(author)
        db.commit()
        logger.info(f"Author deleted: {author.full_name}")
        return True
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error deleting author: {str(e)}")
        raise

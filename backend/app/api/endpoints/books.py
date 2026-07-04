"""
Book management endpoints
- CRUD operations for books
- Search and filter books
- Book availability information
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.schemas import BookCreate, BookUpdate, BookResponse, BookDetailResponse
from app.crud import book as book_crud
from app.utils.exceptions import NotFoundError, DuplicateEntryError, BusinessLogicError
from app.core.logging_config import logger

router = APIRouter()


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_create: BookCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new book
    
    - **isbn**: Unique ISBN (10-20 characters)
    - **title**: Book title
    - **language_id**: Language ID
    - **publisher**: Publisher name
    - **publication_year**: Year of publication (1000-2100)
    - **edition**: Edition (optional)
    - **shelf_location**: Shelf or location reference
    - **total_copies**: Total copies available (default: 1)
    - **author_ids**: List of author IDs
    - **genre_ids**: List of genre IDs
    
    Returns: Created book
    """
    try:
        book = book_crud.create_book(db, book_create)
        logger.info(f"Book created: {book.title}")
        return book
    except DuplicateEntryError as e:
        logger.warning(f"Book creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except NotFoundError as e:
        logger.warning(f"Book creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[BookDetailResponse])
async def list_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all books with pagination
    
    - **skip**: Number of books to skip
    - **limit**: Maximum number of books to return
    
    Returns: List of books
    """
    try:
        books = book_crud.get_all_books(db, skip=skip, limit=limit)
        return [book_crud.book_to_detail(db, book) for book in books]
    except Exception as e:
        logger.error(f"Error listing books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve books"
        )


@router.get("/search", response_model=List[BookDetailResponse])
async def search_books(
    title: Optional[str] = Query(None, description="Search by title (partial match)"),
    author: Optional[str] = Query(None, description="Search by author name (partial match)"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    language_id: Optional[int] = Query(None, description="Filter by language ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Search and filter books
    
    - **title**: Search by book title (partial match)
    - **author**: Search by author name (partial match)
    - **genre**: Filter by genre
    - **language_id**: Filter by language
    - **skip**: Pagination offset
    - **limit**: Pagination limit
    
    Returns: List of matching books
    """
    try:
        books = book_crud.search_books(
            db,
            title=title,
            author=author,
            genre=genre,
            language_id=language_id,
            skip=skip,
            limit=limit
        )
        return [book_crud.book_to_detail(db, book) for book in books]
    except Exception as e:
        logger.error(f"Error searching books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search books"
        )


@router.get("/{book_id}", response_model=BookDetailResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get book details by ID including availability information
    
    - **book_id**: Book ID
    
    Returns: Book details with copy information
    """
    try:
        book = book_crud.get_book_by_id(db, book_id)
        return book_crud.book_to_detail(db, book)
    except NotFoundError as e:
        logger.warning(f"Book not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve book"
        )


@router.get("/isbn/{isbn}", response_model=BookDetailResponse)
async def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    """
    Get book by ISBN
    
    - **isbn**: Book ISBN
    
    Returns: Book details
    """
    try:
        book = book_crud.get_book_by_isbn(db, isbn)
        return book_crud.book_to_detail(db, book)
    except NotFoundError as e:
        logger.warning(f"Book not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve book"
        )


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):
    """
    Update book information
    
    - **book_id**: Book ID
    - **book_update**: Fields to update
    
    Returns: Updated book
    """
    try:
        book = book_crud.update_book(db, book_id, book_update)
        logger.info(f"Book updated: {book.title}")
        return book
    except NotFoundError as e:
        logger.warning(f"Book not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book (only if no copies are currently issued)
    
    - **book_id**: Book ID to delete
    
    Returns: No content (204)
    """
    try:
        book_crud.delete_book(db, book_id)
        logger.info(f"Book deleted: ID {book_id}")
    except NotFoundError as e:
        logger.warning(f"Book not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessLogicError as e:
        logger.warning(f"Cannot delete book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete book"
        )


@router.get("/{book_id}/available-copies", response_model=dict)
async def get_available_copies(book_id: int, db: Session = Depends(get_db)):
    """
    Get number of available copies for a book
    
    - **book_id**: Book ID
    
    Returns: Available copies count
    """
    try:
        available = book_crud.get_available_copies(db, book_id)
        book = book_crud.get_book_by_id(db, book_id)
        return {
            "book_id": book_id,
            "title": book.title,
            "total_copies": book.total_copies,
            "available_copies": available,
            "issued_copies": book.total_copies - available
        }
    except NotFoundError as e:
        logger.warning(f"Book not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting available copies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get available copies"
        )

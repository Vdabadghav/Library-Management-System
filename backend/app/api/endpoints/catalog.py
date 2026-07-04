"""
Catalog management endpoints
- Languages, Genres, Authors management
- Catalog administration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.schemas import LanguageResponse, GenreResponse, AuthorResponse, AuthorCreate, AuthorUpdate
from app.crud import catalog as catalog_crud
from app.utils.exceptions import NotFoundError, DuplicateEntryError, BusinessLogicError
from app.core.logging_config import logger

router = APIRouter()


# ==================== Language Endpoints ====================
@router.post("/languages", response_model=LanguageResponse, status_code=201)
async def create_language(
    name: str,
    code: str,
    db: Session = Depends(get_db)
):
    """
    Create a new language
    
    - **name**: Language name
    - **code**: Language code (e.g., 'en', 'es', 'fr')
    
    Returns: Created language
    """
    try:
        language = catalog_crud.create_language(db, name, code)
        return language
    except DuplicateEntryError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating language: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/languages", response_model=List[LanguageResponse])
async def list_languages(db: Session = Depends(get_db)):
    """Get all languages"""
    try:
        return catalog_crud.get_all_languages(db)
    except Exception as e:
        logger.error(f"Error listing languages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve languages"
        )


@router.delete("/languages/{language_id}", status_code=204)
async def delete_language(language_id: int, db: Session = Depends(get_db)):
    """Delete a language (only if not in use)"""
    try:
        catalog_crud.delete_language(db, language_id)
        logger.info(f"Language deleted: ID {language_id}")
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting language: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete language"
        )


# ==================== Genre Endpoints ====================
@router.post("/genres", response_model=GenreResponse, status_code=201)
async def create_genre(
    name: str,
    description: str = None,
    db: Session = Depends(get_db)
):
    """
    Create a new genre
    
    - **name**: Genre name
    - **description**: Genre description (optional)
    
    Returns: Created genre
    """
    try:
        genre = catalog_crud.create_genre(db, name, description)
        return genre
    except DuplicateEntryError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating genre: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/genres", response_model=List[GenreResponse])
async def list_genres(db: Session = Depends(get_db)):
    """Get all genres"""
    try:
        return catalog_crud.get_all_genres(db)
    except Exception as e:
        logger.error(f"Error listing genres: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve genres"
        )


@router.put("/genres/{genre_id}", response_model=GenreResponse)
async def update_genre(
    genre_id: int,
    name: str = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    """Update genre information"""
    try:
        genre = catalog_crud.update_genre(db, genre_id, name, description)
        return genre
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateEntryError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating genre: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/genres/{genre_id}", status_code=204)
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """Delete a genre (only if not in use)"""
    try:
        catalog_crud.delete_genre(db, genre_id)
        logger.info(f"Genre deleted: ID {genre_id}")
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting genre: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete genre"
        )


# ==================== Author Endpoints ====================
@router.post("/authors", response_model=AuthorResponse, status_code=201)
async def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new author
    
    - **full_name**: Author's full name
    - **biography**: Author biography (optional)
    
    Returns: Created author
    """
    try:
        created_author = catalog_crud.create_author(db, author.full_name, author.biography)
        return created_author
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/authors", response_model=List[AuthorResponse])
async def list_authors(db: Session = Depends(get_db)):
    """Get all authors"""
    try:
        return catalog_crud.get_all_authors(db)
    except Exception as e:
        logger.error(f"Error listing authors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve authors"
        )


@router.get("/authors/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get author by ID"""
    try:
        return catalog_crud.get_author_by_id(db, author_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve author"
        )


@router.put("/authors/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author: AuthorUpdate,
    db: Session = Depends(get_db)
):
    """Update author information"""
    try:
        updated_author = catalog_crud.update_author(
            db,
            author_id,
            author.full_name,
            author.biography
        )
        return updated_author
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/authors/{author_id}", status_code=204)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author (only if not linked to any books)"""
    try:
        catalog_crud.delete_author(db, author_id)
        logger.info(f"Author deleted: ID {author_id}")
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete author"
        )

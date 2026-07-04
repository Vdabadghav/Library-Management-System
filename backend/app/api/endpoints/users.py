"""
User management endpoints (Admin/Manager only)
- CRUD operations for staff users
- Role and permission management
- User status management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.schemas import UserCreate, UserUpdate, UserResponse
from app.crud import user as user_crud
from app.utils.exceptions import NotFoundError, DuplicateEntryError
from app.core.logging_config import logger

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all users with pagination
    
    - **skip**: Number of users to skip (pagination)
    - **limit**: Maximum number of users to return
    
    Returns: List of users
    """
    try:
        users = user_crud.get_all_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID
    
    - **user_id**: User ID
    
    Returns: User details
    """
    try:
        user = user_crud.get_user_by_id(db, user_id)
        return user
    except NotFoundError as e:
        logger.warning(f"User not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user (Admin/Manager only)
    
    - **username**: Unique username
    - **email**: Valid email address
    - **full_name**: User's full name
    - **password**: Password
    - **role**: User role (administrator, manager, librarian)
    
    Returns: Created user
    """
    try:
        user = user_crud.create_user(db, user_create)
        logger.info(f"User created: {user.username}")
        return user
    except DuplicateEntryError as e:
        logger.warning(f"User creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user information
    
    - **user_id**: User ID
    - **user_update**: Fields to update
    
    Returns: Updated user
    """
    try:
        user = user_crud.update_user(db, user_id, user_update)
        logger.info(f"User updated: {user.username}")
        return user
    except NotFoundError as e:
        logger.warning(f"User not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateEntryError as e:
        logger.warning(f"User update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user
    
    - **user_id**: User ID to delete
    
    Returns: No content (204)
    """
    try:
        user_crud.delete_user(db, user_id)
        logger.info(f"User deleted: ID {user_id}")
    except NotFoundError as e:
        logger.warning(f"User not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.patch("/{user_id}/status/{status}")
async def update_user_status(
    user_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Update user status (active, suspended, inactive)
    
    - **user_id**: User ID
    - **status**: New status (active, suspended, inactive)
    
    Returns: Updated user
    """
    try:
        if status not in ["active", "suspended", "inactive"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Must be 'active', 'suspended', or 'inactive'"
            )

        user = user_crud.update_user_status(db, user_id, status)
        logger.info(f"User status updated: {user.username} -> {status}")
        return user
    except NotFoundError as e:
        logger.warning(f"User not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user status"
        )

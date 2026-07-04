"""
Authentication endpoints
- User login
- Token management
- Registration approval (Admin only)
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import UserLogin, TokenResponse, UserCreate, UserResponse
from app.crud import user as user_crud
from app.core.security import create_access_token
from app.core.config import settings
from app.utils.exceptions import NotFoundError
from app.core.logging_config import logger

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=200)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    User login endpoint
    
    - **username**: Username
    - **password**: Password
    
    Returns: JWT access token and user information
    """
    try:
        # Authenticate user
        user = user_crud.authenticate_user(db, login_data.username, login_data.password)

        # Check if user is approved
        if user.status == "inactive":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is not approved yet"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except HTTPException:
        raise
    except NotFoundError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    except ValueError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    except Exception as e:
        logger.error(f"Login error: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    User self-registration
    New registrations are created with 'active' status and can login immediately
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **full_name**: User's full name
    - **password**: Password (min 8 chars)
    - **role**: User role (optional, defaults to 'librarian')
    
    Returns: Created user with 'active' status
    """
    try:
        # Override role to librarian for self-registration
        user_create.role = "librarian"
        
        user = user_crud.create_user(db, user_create)
        
        logger.info(f"New user registration: {user.username}")
        return user
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/verify-token")
async def verify_token(token: str):
    """
    Verify JWT token validity
    
    - **token**: JWT token to verify
    
    Returns: Token validity status and decoded data
    """
    try:
        from app.core.security import verify_token
        payload = verify_token(token)
        return {"valid": True, "data": payload}
    except Exception as e:
        logger.warning(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

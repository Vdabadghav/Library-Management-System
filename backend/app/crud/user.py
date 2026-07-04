"""
CRUD operations for User model
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password, pwd_context
from app.utils.exceptions import NotFoundError, DuplicateEntryError, DatabaseError
from app.core.logging_config import logger


def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a new user"""
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_create.username).first()
        if existing_user:
            raise DuplicateEntryError(f"Username '{user_create.username}' already exists")

        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_create.email).first()
        if existing_email:
            raise DuplicateEntryError(f"Email '{user_create.email}' already exists")

        # Hash password
        hashed_password = hash_password(user_create.password)

        # Create user - auto-approve (status = "active")
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            password_hash=hashed_password,
            role=user_create.role,
            status="active"  # Auto-approve new users
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created: {db_user.username}")
        return db_user
    except (DuplicateEntryError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError(f"User with ID {user_id} not found")
    return user


def get_user_by_username(db: Session, username: str) -> User:
    """Get user by username"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise NotFoundError(f"User '{username}' not found")
    return user


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise NotFoundError(f"User with email '{email}' not found")
    return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    """Update user information"""
    try:
        user = get_user_by_id(db, user_id)

        # Check if new email already exists
        if user_update.email and user_update.email != user.email:
            existing_email = db.query(User).filter(
                User.email == user_update.email,
                User.id != user_id
            ).first()
            if existing_email:
                raise DuplicateEntryError(f"Email '{user_update.email}' already exists")

        # Update fields
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        logger.info(f"User updated: {user.username}")
        return user
    except (NotFoundError, DuplicateEntryError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating user: {str(e)}")
        raise


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    try:
        user = get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        logger.info(f"User deleted: {user.username}")
        return True
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error deleting user: {str(e)}")
        raise


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Authenticate user by username and password"""
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise NotFoundError(f"User '{username}' not found")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid password")

        # Update last login
        user.last_login = datetime.utcnow()
        
        # Re-hash password if it's using deprecated bcrypt scheme (auto-upgrade to argon2)
        if pwd_context.needs_update(user.password_hash):
            user.password_hash = hash_password(password)
        
        db.commit()
        db.refresh(user)
        logger.info(f"User authenticated: {user.username}")
        return user
    except (NotFoundError, ValueError) as e:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error authenticating user: {str(e)}")
        raise


def update_user_status(db: Session, user_id: int, status: str) -> User:
    """Update user status"""
    try:
        user = get_user_by_id(db, user_id)
        user.status = status
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        logger.info(f"User status updated: {user.username} -> {status}")
        return user
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating user status: {str(e)}")
        raise


def get_users_by_role(db: Session, role: str) -> list[User]:
    """Get all users with a specific role"""
    return db.query(User).filter(User.role == role).all()

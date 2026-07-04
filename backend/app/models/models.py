"""
SQLAlchemy models for Library Management System
Defines all database tables and relationships
"""
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Date, Float, Boolean,
    ForeignKey, Table, Enum, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


# Many-to-many association tables
book_author_association = Table(
    'book_author',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id', ondelete='CASCADE'), primary_key=True),
    Column('author_id', Integer, ForeignKey('author.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_book_author_book_id', 'book_id'),
    Index('idx_book_author_author_id', 'author_id')
)

book_genre_association = Table(
    'book_genre',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_book_genre_book_id', 'book_id'),
    Index('idx_book_genre_genre_id', 'genre_id')
)


# Enums
class UserStatus(str, enum.Enum):
    """User account status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class MemberStatus(str, enum.Enum):
    """Member status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"


class IssueStatus(str, enum.Enum):
    """Book issue status"""
    ISSUED = "issued"
    RETURNED = "returned"


class FineStatus(str, enum.Enum):
    """Fine payment status"""
    OUTSTANDING = "outstanding"
    PAID = "paid"


class RoleEnum(str, enum.Enum):
    """User roles"""
    ADMINISTRATOR = "administrator"
    MANAGER = "manager"
    LIBRARIAN = "librarian"


# Models
class User(Base):
    """Staff users of the system"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=RoleEnum.LIBRARIAN)
    status = Column(String(20), default=UserStatus.INACTIVE)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    book_issues = relationship("BookIssue", back_populates="issued_by_user")

    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_status', 'status'),
    )


class Role(Base):
    """Roles and their permissions"""
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    permissions = relationship("Permission", back_populates="role", cascade="all, delete-orphan")


class Permission(Base):
    """Permissions assigned to roles"""
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'), nullable=False)
    feature_name = Column(String(100), nullable=False)
    can_view = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    can_approve = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    role = relationship("Role", back_populates="permissions")

    __table_args__ = (
        UniqueConstraint('role_id', 'feature_name', name='idx_role_feature_unique'),
    )


class Language(Base):
    """Languages for books"""
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    books = relationship("Book", back_populates="language")


class Genre(Base):
    """Book genres"""
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    books = relationship("Book", secondary=book_genre_association, back_populates="genres")


class Author(Base):
    """Book authors"""
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    biography = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    books = relationship("Book", secondary=book_author_association, back_populates="authors")


class Book(Base):
    """Books in the catalog"""
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    language_id = Column(Integer, ForeignKey('language.id'), nullable=False)
    publisher = Column(String(200), nullable=False)
    publication_year = Column(Integer, nullable=False)
    edition = Column(String(50), nullable=True)
    shelf_location = Column(String(100), nullable=False)
    total_copies = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    language = relationship("Language", back_populates="books")
    authors = relationship("Author", secondary=book_author_association, back_populates="books")
    genres = relationship("Genre", secondary=book_genre_association, back_populates="books")
    book_issues = relationship("BookIssue", back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_book_isbn', 'isbn'),
        Index('idx_book_title', 'title'),
        Index('idx_book_language_id', 'language_id'),
    )


class MembershipPlan(Base):
    """Membership plans for library members"""
    __tablename__ = "membership_plan"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    max_books_allowed = Column(Integer, nullable=False)
    max_days_allowed = Column(Integer, nullable=False)
    fine_per_day = Column(Float, nullable=False)
    membership_fee = Column(Float, nullable=False)
    validity_months = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    members = relationship("Member", back_populates="membership_plan")


class Member(Base):
    """Library members"""
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    member_code = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    email = Column(String(100), nullable=True, index=True)
    phone_number = Column(String(20), nullable=True)
    postal_address = Column(Text, nullable=False)
    membership_plan_id = Column(Integer, ForeignKey('membership_plan.id'), nullable=False)
    status = Column(String(20), default=MemberStatus.ACTIVE)
    registration_date = Column(Date, default=date.today)
    expiry_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    membership_plan = relationship("MembershipPlan", back_populates="members")
    book_issues = relationship("BookIssue", back_populates="member", cascade="all, delete-orphan")
    fines = relationship("Fine", back_populates="member", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_member_code', 'member_code'),
        Index('idx_member_status', 'status'),
        Index('idx_member_expiry_date', 'expiry_date'),
    )


class BookIssue(Base):
    """Book issue and return tracking"""
    __tablename__ = "book_issue"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    issued_by_user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), default=IssueStatus.ISSUED)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    book = relationship("Book", back_populates="book_issues")
    member = relationship("Member", back_populates="book_issues")
    issued_by_user = relationship("User", back_populates="book_issues")
    fine = relationship("Fine", uselist=False, back_populates="book_issue")

    __table_args__ = (
        Index('idx_book_issue_member_id', 'member_id'),
        Index('idx_book_issue_book_id', 'book_id'),
        Index('idx_book_issue_status', 'status'),
        Index('idx_book_issue_due_date', 'due_date'),
    )


class Fine(Base):
    """Fine records for overdue books"""
    __tablename__ = "fine"

    id = Column(Integer, primary_key=True, index=True)
    book_issue_id = Column(Integer, ForeignKey('book_issue.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), default=FineStatus.OUTSTANDING)
    date_raised = Column(Date, default=date.today)
    date_paid = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    book_issue = relationship("BookIssue", back_populates="fine")
    member = relationship("Member", back_populates="fines")

    __table_args__ = (
        Index('idx_fine_member_id', 'member_id'),
        Index('idx_fine_status', 'status'),
        Index('idx_fine_book_issue_id', 'book_issue_id'),
    )


class ActivityLog(Base):
    """Audit trail of all system activities"""
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    old_values = Column(Text, nullable=True)  # JSON string
    new_values = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")

    __table_args__ = (
        Index('idx_activity_log_user_id', 'user_id'),
        Index('idx_activity_log_action', 'action'),
        Index('idx_activity_log_created_at', 'created_at'),
    )

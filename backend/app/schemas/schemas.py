"""
Pydantic schemas for data validation and serialization
"""
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, validator, conint, confloat


# ==================== User Schemas ====================
class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default="librarian")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    status: str
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== Language Schemas ====================
class LanguageBase(BaseModel):
    """Base language schema"""
    name: str = Field(..., min_length=2, max_length=50)
    code: str = Field(..., min_length=2, max_length=10)


class LanguageCreate(LanguageBase):
    pass


class LanguageResponse(LanguageBase):
    """Language response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Genre Schemas ====================
class GenreBase(BaseModel):
    """Base genre schema"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    """Genre response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Author Schemas ====================
class AuthorBase(BaseModel):
    """Base author schema"""
    full_name: str = Field(..., min_length=2, max_length=200)
    biography: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    """Update author schema"""
    full_name: Optional[str] = None
    biography: Optional[str] = None


class AuthorResponse(AuthorBase):
    """Author response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Book Schemas ====================
class BookBase(BaseModel):
    """Base book schema"""
    isbn: str = Field(..., min_length=10, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    language_id: int
    publisher: str = Field(..., min_length=1, max_length=200)
    publication_year: conint(ge=1000, le=2100) = Field(...)
    edition: Optional[str] = None
    shelf_location: str = Field(..., min_length=1, max_length=100)
    total_copies: conint(ge=1) = Field(default=1)


class BookCreate(BookBase):
    """Schema for creating a book"""
    author_ids: List[int] = Field(default_factory=list)
    genre_ids: List[int] = Field(default_factory=list)


class BookUpdate(BaseModel):
    """Schema for updating a book"""
    title: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[conint(ge=1000, le=2100)] = None
    edition: Optional[str] = None
    shelf_location: Optional[str] = None
    total_copies: Optional[conint(ge=1)] = None
    author_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None


class BookResponse(BookBase):
    """Book response schema"""
    id: int
    authors: List[AuthorResponse] = []
    genres: List[GenreResponse] = []
    language: Optional[LanguageResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookDetailResponse(BookResponse):
    """Detailed book response with copy information"""
    copies_issued: int = 0
    copies_available: int


# ==================== Membership Plan Schemas ====================
class MembershipPlanBase(BaseModel):
    """Base membership plan schema"""
    name: str = Field(..., min_length=1, max_length=100)
    max_books_allowed: conint(ge=1) = Field(...)
    max_days_allowed: conint(ge=1) = Field(...)
    fine_per_day: confloat(ge=0) = Field(...)
    membership_fee: confloat(ge=0) = Field(...)
    validity_months: conint(ge=1) = Field(...)
    description: Optional[str] = None


class MembershipPlanCreate(MembershipPlanBase):
    pass


class MembershipPlanUpdate(BaseModel):
    """Update membership plan schema"""
    name: Optional[str] = None
    max_books_allowed: Optional[conint(ge=1)] = None
    max_days_allowed: Optional[conint(ge=1)] = None
    fine_per_day: Optional[confloat(ge=0)] = None
    membership_fee: Optional[confloat(ge=0)] = None
    validity_months: Optional[conint(ge=1)] = None
    description: Optional[str] = None


class MembershipPlanResponse(MembershipPlanBase):
    """Membership plan response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Member Schemas ====================
class MemberBase(BaseModel):
    """Base member schema"""
    member_code: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    postal_address: str = Field(..., min_length=1)
    membership_plan_id: int


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    """Update member schema"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    postal_address: Optional[str] = None
    membership_plan_id: Optional[int] = None
    status: Optional[str] = None


class MemberResponse(MemberBase):
    """Member response schema"""
    id: int
    status: str
    registration_date: date
    expiry_date: date
    membership_plan: Optional[MembershipPlanResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemberDetailResponse(MemberResponse):
    """Detailed member response with issued books count"""
    books_issued_count: int = 0
    outstanding_fines: float = 0


# ==================== Book Issue Schemas ====================
class BookIssueBase(BaseModel):
    """Base book issue schema"""
    book_id: int
    member_id: int


class BookIssueCreate(BookIssueBase):
    pass


class BookIssueReturn(BaseModel):
    """Schema for returning a book"""
    return_date: date = Field(default_factory=date.today)
    fine_paid: bool = False


class BookIssueResponse(BookIssueBase):
    """Book issue response schema"""
    id: int
    issued_by_user_id: int
    issue_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Fine Schemas ====================
class FineBase(BaseModel):
    """Base fine schema"""
    member_id: int
    amount: confloat(ge=0) = Field(...)


class FineResponse(FineBase):
    """Fine response schema"""
    id: int
    book_issue_id: int
    status: str
    date_raised: date
    date_paid: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True


class FineSummaryResponse(BaseModel):
    """Fine summary response"""
    total_outstanding: float
    total_collected: float
    period_start: date
    period_end: date


# ==================== Dashboard Schemas ====================
class DashboardResponse(BaseModel):
    """Dashboard summary response"""
    total_books: int
    total_active_members: int
    total_issued_books: int
    total_overdue_books: int
    total_outstanding_fines: float
    recent_activities: List[dict] = []


# ==================== Error Response Schemas ====================
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    status_code: int = 400
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ValidationErrorResponse(BaseModel):
    """Validation error response"""
    error: str = "Validation Error"
    details: List[dict]
    status_code: int = 422

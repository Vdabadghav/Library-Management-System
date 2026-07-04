"""Custom exceptions for the application"""


class LibraryException(Exception):
    """Base exception for Library Management System"""
    pass


class ValidationError(LibraryException):
    """Raised when input validation fails"""
    pass


class NotFoundError(LibraryException):
    """Raised when a requested resource is not found"""
    pass


class UnauthorizedError(LibraryException):
    """Raised when user is not authorized to perform action"""
    pass


class DatabaseError(LibraryException):
    """Raised when database operation fails"""
    pass


class DuplicateEntryError(LibraryException):
    """Raised when trying to create duplicate entry"""
    pass


class BusinessLogicError(LibraryException):
    """Raised when business logic constraints are violated"""
    pass

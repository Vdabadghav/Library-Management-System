"""
Book transaction endpoints
- Issue books to members
- Return books from members
- Fine management
- Overdue tracking
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.database import get_db
from app.schemas.schemas import BookIssueResponse, BookIssueReturn, FineResponse, FineSummaryResponse
from app.crud import transaction as transaction_crud
from app.utils.exceptions import NotFoundError, BusinessLogicError
from app.core.logging_config import logger

router = APIRouter()


# ==================== Book Issue Endpoints ====================
@router.post("/issue", response_model=BookIssueResponse, status_code=201)
async def issue_book(
    book_id: int,
    member_id: int,
    issued_by_user_id: int,
    db: Session = Depends(get_db)
):
    """
    Issue a book to a member
    
    Validates:
    - Member is active and membership is not expired
    - Member has not reached borrowing limit
    - Member has no outstanding fines
    - Book has available copies
    - Member doesn't already have this book issued
    
    - **book_id**: Book ID
    - **member_id**: Member ID
    - **issued_by_user_id**: User ID of staff issuing the book
    
    Returns: Issue record with due date
    """
    try:
        issue = transaction_crud.issue_book(db, book_id, member_id, issued_by_user_id)
        logger.info(f"Book issued: Book ID {book_id}, Member ID {member_id}")
        return issue
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
        logger.error(f"Error issuing book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to issue book"
        )


@router.post("/return/{issue_id}", response_model=BookIssueResponse)
async def return_book(
    issue_id: int,
    return_date: Optional[date] = None,
    fine_paid: bool = False,
    db: Session = Depends(get_db)
):
    """
    Return a book from a member
    
    - **issue_id**: Book issue ID
    - **return_date**: Return date (defaults to today)
    - **fine_paid**: Whether fine is paid immediately
    
    Returns: Updated issue record
    """
    try:
        issue = transaction_crud.return_book(db, issue_id, return_date, fine_paid)
        logger.info(f"Book returned: Issue ID {issue_id}")
        return issue
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
        logger.error(f"Error returning book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to return book"
        )


@router.get("/issues/{issue_id}", response_model=BookIssueResponse)
async def get_book_issue(issue_id: int, db: Session = Depends(get_db)):
    """Get book issue details by ID"""
    try:
        issue = transaction_crud.get_book_issue_by_id(db, issue_id)
        return issue
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving issue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve issue"
        )


@router.get("/member/{member_id}/issued", response_model=List[BookIssueResponse])
async def get_member_issued_books(member_id: int, db: Session = Depends(get_db)):
    """Get all books currently issued to a member"""
    try:
        issues = transaction_crud.get_member_issued_books(db, member_id)
        return issues
    except Exception as e:
        logger.error(f"Error retrieving issued books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve issued books"
        )


@router.get("/overdue", response_model=List[BookIssueResponse])
async def get_overdue_books(db: Session = Depends(get_db)):
    """Get all currently overdue books"""
    try:
        overdue = transaction_crud.get_overdue_books(db)
        return overdue
    except Exception as e:
        logger.error(f"Error retrieving overdue books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve overdue books"
        )


@router.get("/report/issued", response_model=List[BookIssueResponse])
async def issued_books_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get issued books report for a date range"""
    try:
        issues = transaction_crud.get_issued_books_report(
            db,
            start_date,
            end_date,
            skip=skip,
            limit=limit
        )
        return issues
    except Exception as e:
        logger.error(f"Error retrieving issued books report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve issued books report"
        )


# ==================== Fine Endpoints ====================
@router.get("/fines/{fine_id}", response_model=FineResponse)
async def get_fine(fine_id: int, db: Session = Depends(get_db)):
    """Get fine details by ID"""
    try:
        fine = transaction_crud.get_fine_by_id(db, fine_id)
        return fine
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving fine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fine"
        )


@router.get("/member/{member_id}/fines", response_model=List[FineResponse])
async def get_member_fines(member_id: int, db: Session = Depends(get_db)):
    """Get all fines for a member"""
    try:
        fines = transaction_crud.get_member_fines(db, member_id)
        return fines
    except Exception as e:
        logger.error(f"Error retrieving member fines: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve member fines"
        )


@router.get("/member/{member_id}/fines/outstanding", response_model=List[FineResponse])
async def get_member_outstanding_fines(member_id: int, db: Session = Depends(get_db)):
    """Get outstanding fines for a member"""
    try:
        fines = transaction_crud.get_outstanding_fines(db, member_id)
        return fines
    except Exception as e:
        logger.error(f"Error retrieving outstanding fines: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve outstanding fines"
        )


@router.post("/fines/{fine_id}/pay", response_model=FineResponse)
async def mark_fine_as_paid(fine_id: int, db: Session = Depends(get_db)):
    """
    Mark a fine as paid
    
    - **fine_id**: Fine ID
    
    Returns: Updated fine record
    """
    try:
        fine = transaction_crud.mark_fine_as_paid(db, fine_id)
        logger.info(f"Fine marked as paid: ID {fine_id}")
        return fine
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error marking fine as paid: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark fine as paid"
        )


@router.get("/report/fines", response_model=FineSummaryResponse)
async def fine_collection_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    """
    Get fine collection report for a period
    
    - **start_date**: Report start date
    - **end_date**: Report end date
    
    Returns: Fine summary with totals
    """
    try:
        summary = transaction_crud.get_fine_summary(db, start_date, end_date)
        return summary
    except Exception as e:
        logger.error(f"Error retrieving fine report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fine report"
        )


@router.get("/fines", response_model=List[FineResponse])
async def list_all_fines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all fines with pagination"""
    try:
        fines = transaction_crud.get_all_fines(db, skip=skip, limit=limit)
        return fines
    except Exception as e:
        logger.error(f"Error listing fines: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fines"
        )

"""
CRUD operations for BookIssue and Fine models
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import date, datetime, timedelta

from app.models.models import (
    BookIssue, Fine, Book, Member, User, MembershipPlan
)
from app.utils.exceptions import (
    NotFoundError, BusinessLogicError, DatabaseError
)
from app.core.logging_config import logger


# ==================== Book Issue CRUD ====================
def issue_book(
    db: Session,
    book_id: int,
    member_id: int,
    issued_by_user_id: int
) -> BookIssue:
    """Issue a book to a member"""
    try:
        # Get book
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise NotFoundError(f"Book with ID {book_id} not found")

        # Get member
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise NotFoundError(f"Member with ID {member_id} not found")

        # Get user
        user = db.query(User).filter(User.id == issued_by_user_id).first()
        if not user:
            raise NotFoundError(f"User with ID {issued_by_user_id} not found")

        # Validate member status
        if member.status != "active":
            raise BusinessLogicError(f"Member is {member.status} and cannot borrow books")

        # Check member's membership expiry
        if member.expiry_date < date.today():
            member.status = "expired"
            db.commit()
            raise BusinessLogicError("Member's membership has expired")

        # Check member's issued books limit
        issued_count = db.query(BookIssue).filter(
            BookIssue.member_id == member_id,
            BookIssue.status == "issued"
        ).count()

        membership_plan = db.query(MembershipPlan).filter(
            MembershipPlan.id == member.membership_plan_id
        ).first()

        if issued_count >= membership_plan.max_books_allowed:
            raise BusinessLogicError(
                f"Member has reached the maximum limit of {membership_plan.max_books_allowed} books"
            )

        # Check for unpaid fines
        unpaid_fines = db.query(Fine).filter(
            Fine.member_id == member_id,
            Fine.status == "outstanding"
        ).count()

        if unpaid_fines > 0:
            raise BusinessLogicError(f"Member has {unpaid_fines} unpaid fine(s)")

        # Check available copies
        available = book.total_copies - db.query(BookIssue).filter(
            BookIssue.book_id == book_id,
            BookIssue.status == "issued"
        ).count()

        if available <= 0:
            raise BusinessLogicError("No copies of this book are available")

        # Check if member already has this book issued
        existing = db.query(BookIssue).filter(
            BookIssue.member_id == member_id,
            BookIssue.book_id == book_id,
            BookIssue.status == "issued"
        ).first()

        if existing:
            raise BusinessLogicError("Member already has this book issued")

        # Calculate due date
        due_date = date.today() + timedelta(days=membership_plan.max_days_allowed)

        # Create issue record
        book_issue = BookIssue(
            book_id=book_id,
            member_id=member_id,
            issued_by_user_id=issued_by_user_id,
            issue_date=date.today(),
            due_date=due_date,
            status="issued"
        )

        db.add(book_issue)
        db.commit()
        db.refresh(book_issue)
        logger.info(f"Book issued: {book.title} to member {member.member_code}")
        return book_issue
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error issuing book: {str(e)}")
        raise


def return_book(
    db: Session,
    issue_id: int,
    return_date: date = None,
    fine_paid: bool = False
) -> BookIssue:
    """Return a book"""
    try:
        if return_date is None:
            return_date = date.today()

        # Get issue record
        issue = db.query(BookIssue).filter(BookIssue.id == issue_id).first()
        if not issue:
            raise NotFoundError(f"Book issue with ID {issue_id} not found")

        if issue.status == "returned":
            raise BusinessLogicError("This book has already been returned")

        # Update issue
        issue.return_date = return_date
        issue.status = "returned"

        # Check if book is overdue and create fine if necessary
        if return_date > issue.due_date:
            days_late = (return_date - issue.due_date).days
            
            # Get member's plan to get fine per day
            member = db.query(Member).filter(Member.id == issue.member_id).first()
            plan = db.query(MembershipPlan).filter(
                MembershipPlan.id == member.membership_plan_id
            ).first()

            fine_amount = days_late * plan.fine_per_day

            # Create fine record
            fine = Fine(
                book_issue_id=issue.id,
                member_id=issue.member_id,
                amount=fine_amount,
                status="paid" if fine_paid else "outstanding",
                date_raised=date.today(),
                date_paid=date.today() if fine_paid else None
            )

            db.add(fine)

        db.commit()
        db.refresh(issue)
        logger.info(f"Book returned: Issue ID {issue_id}")
        return issue
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error returning book: {str(e)}")
        raise


def get_book_issue_by_id(db: Session, issue_id: int) -> BookIssue:
    """Get book issue by ID"""
    issue = db.query(BookIssue).filter(BookIssue.id == issue_id).first()
    if not issue:
        raise NotFoundError(f"Book issue with ID {issue_id} not found")
    return issue


def get_member_issued_books(db: Session, member_id: int) -> List[BookIssue]:
    """Get all books currently issued to a member"""
    return db.query(BookIssue).filter(
        BookIssue.member_id == member_id,
        BookIssue.status == "issued"
    ).all()


def get_overdue_books(db: Session) -> List[BookIssue]:
    """Get all overdue books"""
    return db.query(BookIssue).filter(
        BookIssue.status == "issued",
        BookIssue.due_date < date.today()
    ).all()


def get_issued_books_report(
    db: Session,
    start_date: date,
    end_date: date,
    skip: int = 0,
    limit: int = 100
) -> List[BookIssue]:
    """Get issued books within a date range"""
    return db.query(BookIssue).filter(
        BookIssue.issue_date >= start_date,
        BookIssue.issue_date <= end_date
    ).offset(skip).limit(limit).all()


# ==================== Fine CRUD ====================
def get_fine_by_id(db: Session, fine_id: int) -> Fine:
    """Get fine by ID"""
    fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not fine:
        raise NotFoundError(f"Fine with ID {fine_id} not found")
    return fine


def get_member_fines(db: Session, member_id: int) -> List[Fine]:
    """Get all fines for a member"""
    return db.query(Fine).filter(Fine.member_id == member_id).all()


def get_outstanding_fines(db: Session, member_id: int) -> List[Fine]:
    """Get outstanding fines for a member"""
    return db.query(Fine).filter(
        Fine.member_id == member_id,
        Fine.status == "outstanding"
    ).all()


def mark_fine_as_paid(db: Session, fine_id: int) -> Fine:
    """Mark a fine as paid"""
    try:
        fine = get_fine_by_id(db, fine_id)
        fine.status = "paid"
        fine.date_paid = date.today()
        db.commit()
        db.refresh(fine)
        logger.info(f"Fine marked as paid: ID {fine_id}")
        return fine
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error marking fine as paid: {str(e)}")
        raise


def get_fine_summary(
    db: Session,
    start_date: date,
    end_date: date
) -> dict:
    """Get fine summary for a period"""
    outstanding = db.query(Fine).filter(
        Fine.status == "outstanding",
        Fine.date_raised >= start_date,
        Fine.date_raised <= end_date
    ).with_entities(db.func.sum(Fine.amount)).scalar() or 0

    collected = db.query(Fine).filter(
        Fine.status == "paid",
        Fine.date_paid >= start_date,
        Fine.date_paid <= end_date
    ).with_entities(db.func.sum(Fine.amount)).scalar() or 0

    return {
        "total_outstanding": float(outstanding),
        "total_collected": float(collected),
        "period_start": start_date,
        "period_end": end_date
    }


def get_all_fines(db: Session, skip: int = 0, limit: int = 100) -> List[Fine]:
    """Get all fines with pagination"""
    return db.query(Fine).offset(skip).limit(limit).all()

"""
CRUD operations for Member model
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date, timedelta
from typing import List, Optional
from app.models.models import Member, MembershipPlan, BookIssue, Fine
from app.schemas.schemas import MemberCreate, MemberUpdate
from app.utils.exceptions import NotFoundError, DuplicateEntryError, DatabaseError, BusinessLogicError
from app.core.logging_config import logger


def create_member(db: Session, member_create: MemberCreate) -> Member:
    """Create a new member"""
    try:
        # Check if member code already exists
        existing_member = db.query(Member).filter(
            Member.member_code == member_create.member_code
        ).first()
        if existing_member:
            raise DuplicateEntryError(f"Member code '{member_create.member_code}' already exists")

        # Verify membership plan exists
        plan = db.query(MembershipPlan).filter(
            MembershipPlan.id == member_create.membership_plan_id
        ).first()
        if not plan:
            raise NotFoundError(f"Membership plan with ID {member_create.membership_plan_id} not found")

        # Calculate expiry date
        expiry_date = date.today() + timedelta(days=30 * plan.validity_months)

        # Create member
        db_member = Member(
            member_code=member_create.member_code,
            full_name=member_create.full_name,
            email=member_create.email,
            phone_number=member_create.phone_number,
            postal_address=member_create.postal_address,
            membership_plan_id=member_create.membership_plan_id,
            registration_date=date.today(),
            expiry_date=expiry_date
        )

        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        logger.info(f"Member created: {db_member.member_code}")
        return db_member
    except (DuplicateEntryError, NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error creating member: {str(e)}")
        raise


def get_member_by_id(db: Session, member_id: int) -> Member:
    """Get member by ID"""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise NotFoundError(f"Member with ID {member_id} not found")
    return member


def get_member_by_code(db: Session, member_code: str) -> Member:
    """Get member by member code"""
    member = db.query(Member).filter(Member.member_code == member_code).first()
    if not member:
        raise NotFoundError(f"Member with code '{member_code}' not found")
    return member


def get_all_members(db: Session, skip: int = 0, limit: int = 100) -> List[Member]:
    """Get all members with pagination"""
    return (
        db.query(Member)
        .options(joinedload(Member.membership_plan))
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_members(
    db: Session,
    name: Optional[str] = None,
    member_code: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Member]:
    """Search members by various criteria"""
    query = db.query(Member)

    if name:
        query = query.filter(Member.full_name.ilike(f"%{name}%"))

    if member_code:
        query = query.filter(Member.member_code.ilike(f"%{member_code}%"))

    if phone:
        query = query.filter(Member.phone_number.like(f"%{phone}%"))

    if email:
        query = query.filter(Member.email.ilike(f"%{email}%"))

    return (
        query.options(joinedload(Member.membership_plan))
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_member(db: Session, member_id: int, member_update: MemberUpdate) -> Member:
    """Update member information"""
    try:
        member = get_member_by_id(db, member_id)

        # If changing membership plan, recalculate expiry date
        if member_update.membership_plan_id and member_update.membership_plan_id != member.membership_plan_id:
            plan = db.query(MembershipPlan).filter(
                MembershipPlan.id == member_update.membership_plan_id
            ).first()
            if not plan:
                raise NotFoundError(f"Membership plan with ID {member_update.membership_plan_id} not found")

            member.membership_plan_id = member_update.membership_plan_id
            member.expiry_date = date.today() + timedelta(days=30 * plan.validity_months)

        # Update other fields
        update_data = member_update.model_dump(
            exclude_unset=True,
            exclude={'membership_plan_id'}
        )
        for field, value in update_data.items():
            if value is not None:
                setattr(member, field, value)

        member.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(member)
        logger.info(f"Member updated: {member.member_code}")
        return member
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating member: {str(e)}")
        raise


def delete_member(db: Session, member_id: int) -> bool:
    """Delete a member (only if no issued books and no unpaid fines)"""
    try:
        member = get_member_by_id(db, member_id)

        # Check if member has issued books
        issued_books = db.query(BookIssue).filter(
            BookIssue.member_id == member_id,
            BookIssue.status == "issued"
        ).count()

        if issued_books > 0:
            raise BusinessLogicError(
                f"Cannot delete member with {issued_books} issued book(s)"
            )

        # Check if member has unpaid fines
        unpaid_fines = db.query(Fine).filter(
            Fine.member_id == member_id,
            Fine.status == "outstanding"
        ).count()

        if unpaid_fines > 0:
            raise BusinessLogicError(
                f"Cannot delete member with {unpaid_fines} unpaid fine(s)"
            )

        db.delete(member)
        db.commit()
        logger.info(f"Member deleted: {member.member_code}")
        return True
    except (NotFoundError, BusinessLogicError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error deleting member: {str(e)}")
        raise


def update_member_status(db: Session, member_id: int, status: str) -> Member:
    """Update member status (active, suspended, expired)"""
    try:
        member = get_member_by_id(db, member_id)
        member.status = status
        member.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(member)
        logger.info(f"Member status updated: {member.member_code} -> {status}")
        return member
    except (NotFoundError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"Error updating member status: {str(e)}")
        raise


def get_active_members(db: Session) -> List[Member]:
    """Get all active members"""
    return db.query(Member).filter(Member.status == "active").all()


def check_and_update_expired_memberships(db: Session) -> int:
    """Check and update expired memberships"""
    try:
        expired_count = db.query(Member).filter(
            Member.expiry_date < date.today(),
            Member.status == "active"
        ).update({"status": "expired"})

        db.commit()
        logger.info(f"Updated {expired_count} expired memberships")
        return expired_count
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating expired memberships: {str(e)}")
        raise

"""
Member management endpoints
- CRUD operations for library members
- Member status management
- Membership plan management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.database import get_db
from app.schemas.schemas import (
    MemberCreate, MemberUpdate, MemberResponse, MemberDetailResponse,
    MembershipPlanCreate, MembershipPlanUpdate, MembershipPlanResponse
)
from app.crud import member as member_crud
from app.models.models import MembershipPlan, Fine, BookIssue
from app.utils.exceptions import NotFoundError, DuplicateEntryError, BusinessLogicError
from app.core.logging_config import logger

router = APIRouter()


# ==================== Member Endpoints ====================
@router.post("/", response_model=MemberResponse, status_code=201)
async def create_member(
    member_create: MemberCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new library member
    
    - **member_code**: Unique member code
    - **full_name**: Member's full name
    - **email**: Email address (optional)
    - **phone_number**: Phone number (optional)
    - **postal_address**: Member's postal address
    - **membership_plan_id**: Selected membership plan ID
    
    Returns: Created member with calculated expiry date
    """
    try:
        member = member_crud.create_member(db, member_create)
        logger.info(f"Member created: {member.member_code}")
        return member
    except DuplicateEntryError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[MemberResponse])
async def list_members(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all members with pagination
    
    - **skip**: Number of members to skip
    - **limit**: Maximum number of members to return
    
    Returns: List of members
    """
    try:
        members = member_crud.get_all_members(db, skip=skip, limit=limit)
        return members
    except Exception as e:
        logger.error(f"Error listing members: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve members"
        )


@router.get("/search", response_model=List[MemberResponse])
async def search_members(
    name: Optional[str] = Query(None),
    member_code: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Search members by various criteria
    
    - **name**: Search by full name
    - **member_code**: Search by member code
    - **phone**: Search by phone number
    - **email**: Search by email
    
    Returns: List of matching members
    """
    try:
        members = member_crud.search_members(
            db,
            name=name,
            member_code=member_code,
            phone=phone,
            email=email,
            skip=skip,
            limit=limit
        )
        return members
    except Exception as e:
        logger.error(f"Error searching members: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search members"
        )


@router.get("/{member_id}", response_model=MemberDetailResponse)
async def get_member(member_id: int, db: Session = Depends(get_db)):
    """
    Get member details by ID
    
    - **member_id**: Member ID
    
    Returns: Member details with issued books count and fines
    """
    try:
        member = member_crud.get_member_by_id(db, member_id)
        
        # Get issued books count
        issued_count = db.query(BookIssue).filter(
            BookIssue.member_id == member_id,
            BookIssue.status == "issued"
        ).count()
        
        # Get outstanding fines
        outstanding_fines = db.query(Fine).filter(
            Fine.member_id == member_id,
            Fine.status == "outstanding"
        ).with_entities(db.func.sum(Fine.amount)).scalar() or 0
        
        return {
            **member.__dict__,
            "books_issued_count": issued_count,
            "outstanding_fines": float(outstanding_fines)
        }
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve member"
        )


@router.get("/code/{member_code}", response_model=MemberResponse)
async def get_member_by_code(member_code: str, db: Session = Depends(get_db)):
    """Get member by member code"""
    try:
        member = member_crud.get_member_by_code(db, member_code)
        return member
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve member"
        )


@router.put("/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: int,
    member_update: MemberUpdate,
    db: Session = Depends(get_db)
):
    """
    Update member information
    
    - **member_id**: Member ID
    - **member_update**: Fields to update
    
    Returns: Updated member
    """
    try:
        member = member_crud.update_member(db, member_id, member_update)
        logger.info(f"Member updated: {member.member_code}")
        return member
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{member_id}", status_code=204)
async def delete_member(member_id: int, db: Session = Depends(get_db)):
    """
    Delete a member (only if no issued books and no unpaid fines)
    
    - **member_id**: Member ID to delete
    
    Returns: No content (204)
    """
    try:
        member_crud.delete_member(db, member_id)
        logger.info(f"Member deleted: ID {member_id}")
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
        logger.error(f"Error deleting member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete member"
        )


@router.patch("/{member_id}/status/{new_status}")
async def update_member_status(
    member_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """
    Update member status (active, suspended, expired)
    
    - **member_id**: Member ID
    - **new_status**: New status
    
    Returns: Updated member
    """
    try:
        if new_status not in ["active", "suspended", "expired"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Must be 'active', 'suspended', or 'expired'"
            )
        
        member = member_crud.update_member_status(db, member_id, new_status)
        return member
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating member status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update member status"
        )


# ==================== Membership Plan Endpoints ====================
@router.post("/plans", response_model=MembershipPlanResponse, status_code=201)
async def create_membership_plan(
    plan: MembershipPlanCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new membership plan
    
    - **name**: Plan name
    - **max_books_allowed**: Maximum books member can borrow
    - **max_days_allowed**: Maximum days before book is overdue
    - **fine_per_day**: Fine charged per day late
    - **membership_fee**: One-time membership fee
    - **validity_months**: Membership validity in months
    - **description**: Plan description (optional)
    
    Returns: Created membership plan
    """
    try:
        db_plan = MembershipPlan(**plan.model_dump())
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        logger.info(f"Membership plan created: {db_plan.name}")
        return db_plan
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating membership plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/plans", response_model=List[MembershipPlanResponse])
async def list_membership_plans(db: Session = Depends(get_db)):
    """Get all membership plans"""
    try:
        plans = db.query(MembershipPlan).all()
        return plans
    except Exception as e:
        logger.error(f"Error listing membership plans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve membership plans"
        )


@router.get("/plans/{plan_id}", response_model=MembershipPlanResponse)
async def get_membership_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get membership plan by ID"""
    try:
        plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()
        if not plan:
            raise NotFoundError(f"Membership plan with ID {plan_id} not found")
        return plan
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving membership plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve membership plan"
        )


@router.put("/plans/{plan_id}", response_model=MembershipPlanResponse)
async def update_membership_plan(
    plan_id: int,
    plan_update: MembershipPlanUpdate,
    db: Session = Depends(get_db)
):
    """Update membership plan"""
    try:
        plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()
        if not plan:
            raise NotFoundError(f"Membership plan with ID {plan_id} not found")
        
        update_data = plan_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        db.commit()
        db.refresh(plan)
        logger.info(f"Membership plan updated: {plan.name}")
        return plan
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating membership plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/plans/{plan_id}", status_code=204)
async def delete_membership_plan(plan_id: int, db: Session = Depends(get_db)):
    """Delete membership plan (only if not assigned to members)"""
    try:
        plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()
        if not plan:
            raise NotFoundError(f"Membership plan with ID {plan_id} not found")
        
        # Check if plan is assigned to any members
        member_count = db.query(member_crud.Member).filter(
            member_crud.Member.membership_plan_id == plan_id
        ).count()
        
        if member_count > 0:
            raise BusinessLogicError(
                f"Cannot delete plan. {member_count} member(s) are using this plan."
            )
        
        db.delete(plan)
        db.commit()
        logger.info(f"Membership plan deleted: ID {plan_id}")
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
        db.rollback()
        logger.error(f"Error deleting membership plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete membership plan"
        )

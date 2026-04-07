from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerWithPayments
from app.crud import (
    create_customer, get_customer, get_customers, update_customer,
    delete_customer, search_customers, get_customer_payments
)
from app.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_new_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new customer with automatic payment schedule generation
    
    Note: Multiple customers can have the same phone number (e.g., family members)
    """
    try:
        db_customer = create_customer(db, customer)
        return db_customer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating customer: {str(e)}"
        )


@router.get("", response_model=List[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all customers"""
    customers = get_customers(db, skip=skip, limit=limit, active_only=active_only)
    return customers


@router.get("/search", response_model=List[CustomerResponse])
def search_for_customers(
    q: str = Query(..., min_length=2, description="Search query"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search customers by name or phone"""
    customers = search_customers(db, q)
    return customers


@router.get("/{customer_id}", response_model=CustomerWithPayments)
def get_customer_details(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get customer details with payment information"""
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Calculate totals
    payments = get_customer_payments(db, customer_id)
    total_paid = sum(p.amount for p in payments if p.is_paid)
    total_pending = sum(p.amount for p in payments if not p.is_paid)
    
    # Convert to response model
    customer_dict = {
        **customer.__dict__,
        "payments": payments,
        "total_paid": total_paid,
        "total_pending": total_pending
    }
    
    return customer_dict


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_details(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update customer information"""
    db_customer = update_customer(db, customer_id, customer_update)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_record(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete (deactivate) a customer"""
    success = delete_customer(db, customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return None

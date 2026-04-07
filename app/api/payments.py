from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.schemas import PaymentResponse, PaymentUpdate, PaymentWithCustomer
from app.crud import (
    get_payment, get_customer_payments, mark_payment_as_paid,
    update_payment, get_pending_payments, get_payments_by_month
)
from app.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("", response_model=List[PaymentWithCustomer])
def list_payments(
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month"),
    year: Optional[int] = Query(None, ge=2020, description="Filter by year"),
    pending_only: bool = Query(False, description="Show only pending payments"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all payments with optional filters"""
    if month and year:
        payments = get_payments_by_month(db, month, year)
        if pending_only:
            payments = [p for p in payments if not p.is_paid]
    elif pending_only:
        payments = get_pending_payments(db)
    else:
        # Get current month payments by default
        today = date.today()
        payments = get_payments_by_month(db, today.month, today.year)
    
    return payments


@router.get("/pending", response_model=List[PaymentWithCustomer])
def list_pending_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all pending payments"""
    payments = get_pending_payments(db)
    return payments


@router.get("/customer/{customer_id}", response_model=List[PaymentResponse])
def get_payments_for_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all payments for a specific customer"""
    payments = get_customer_payments(db, customer_id)
    return payments


@router.get("/{payment_id}", response_model=PaymentWithCustomer)
def get_payment_details(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get payment details"""
    payment = get_payment(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment


@router.post("/{payment_id}/mark-paid", response_model=PaymentResponse)
def mark_as_paid(
    payment_id: int,
    paid_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark a payment as paid"""
    payment = mark_payment_as_paid(db, payment_id, paid_date)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment_details(
    payment_id: int,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update payment information"""
    payment = update_payment(db, payment_id, payment_update)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

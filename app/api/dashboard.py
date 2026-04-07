from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from typing import List
from app.database import get_db
from app.schemas import DashboardStats, PendingCustomerInfo
from app.models import Customer, Payment
from app.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics"""
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    # Total customers (only active)
    total_customers = db.query(Customer).filter(Customer.is_active == True).count()
    
    # Active customers
    active_customers = db.query(Customer).filter(Customer.is_active == True).count()
    
    # This month's payments
    month_payments = db.query(Payment).filter(
        Payment.payment_month == current_month,
        Payment.payment_year == current_year
    ).all()
    
    paid_this_month = sum(1 for p in month_payments if p.is_paid)
    pending_this_month = sum(1 for p in month_payments if not p.is_paid)
    
    # Collection amounts
    total_collection_this_month = sum(p.amount for p in month_payments if p.is_paid)
    pending_amount_this_month = sum(p.amount for p in month_payments if not p.is_paid)
    
    # Total collection overall
    total_collection_overall = db.query(func.sum(Payment.amount)).filter(
        Payment.is_paid == True
    ).scalar() or 0
    
    return DashboardStats(
        total_customers=total_customers,
        active_customers=active_customers,
        paid_this_month=paid_this_month,
        pending_this_month=pending_this_month,
        total_collection_this_month=total_collection_this_month,
        pending_amount_this_month=pending_amount_this_month,
        total_collection_overall=total_collection_overall
    )


@router.get("/pending-today", response_model=List[PendingCustomerInfo])
def get_pending_customers_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of customers with pending payments for follow-up"""
    today = date.today()
    
    # Get all pending payments up to today
    pending_payments = db.query(Payment).join(Customer).filter(
        Payment.is_paid == False,
        Payment.due_date <= today,
        Customer.is_active == True
    ).order_by(Payment.due_date).all()
    
    # Convert to response format
    pending_customers = []
    for payment in pending_payments:
        days_overdue = (today - payment.due_date).days
        pending_customers.append(PendingCustomerInfo(
            customer_id=payment.customer_id,
            customer_name=payment.customer.name,
            phone=payment.customer.phone,
            amount=payment.amount,
            due_date=payment.due_date,
            days_overdue=days_overdue
        ))
    
    return pending_customers


@router.get("/upcoming-dues", response_model=List[PendingCustomerInfo])
def get_upcoming_dues(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get customers with payments due in the next N days"""
    today = date.today()
    end_date = today + timedelta(days=days)
    
    # Get payments due in the next N days
    upcoming_payments = db.query(Payment).join(Customer).filter(
        Payment.is_paid == False,
        Payment.due_date >= today,
        Payment.due_date <= end_date,
        Customer.is_active == True
    ).order_by(Payment.due_date).all()
    
    # Convert to response format
    upcoming = []
    for payment in upcoming_payments:
        days_until_due = (payment.due_date - today).days
        upcoming.append(PendingCustomerInfo(
            customer_id=payment.customer_id,
            customer_name=payment.customer.name,
            phone=payment.customer.phone,
            amount=payment.amount,
            due_date=payment.due_date,
            days_overdue=-days_until_due  # Negative means days until due
        ))
    
    return upcoming


@router.get("/monthly-collections")
def get_monthly_collections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get monthly collection statistics for all months"""
    from datetime import datetime
    from collections import defaultdict
    
    # Get all paid payments
    paid_payments = db.query(Payment).filter(
        Payment.is_paid == True
    ).order_by(Payment.payment_year.desc(), Payment.payment_month.desc()).all()
    
    # Group by month
    monthly_data = defaultdict(lambda: {"total": 0, "count": 0, "customers": set()})
    
    for payment in paid_payments:
        month_key = f"{payment.payment_year}-{payment.payment_month:02d}"
        monthly_data[month_key]["total"] += payment.amount
        monthly_data[month_key]["count"] += 1
        monthly_data[month_key]["customers"].add(payment.customer_id)
    
    # Convert to list format
    result = []
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for month_key in sorted(monthly_data.keys(), reverse=True):
        year, month = month_key.split("-")
        month_num = int(month)
        result.append({
            "month": month_names[month_num],
            "year": int(year),
            "month_year": f"{month_names[month_num]} {year}",
            "total_amount": monthly_data[month_key]["total"],
            "payment_count": monthly_data[month_key]["count"],
            "customer_count": len(monthly_data[month_key]["customers"])
        })
    
    # Calculate grand total
    grand_total = sum(item["total_amount"] for item in result)
    
    return {
        "collections": result,
        "grand_total": grand_total
    }

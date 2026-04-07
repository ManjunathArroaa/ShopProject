from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.reminders import send_manual_reminder, reminder_service
from app.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/send/{customer_id}")
def send_reminder_to_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Send a manual reminder to a specific customer"""
    result = send_manual_reminder(customer_id)
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.get("/preview/{customer_id}")
def preview_reminder_message(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Preview the reminder message that would be sent to a customer"""
    from datetime import date
    from app.models import Payment
    
    # Get pending payment for customer
    today = date.today()
    pending_payment = db.query(Payment).filter(
        Payment.customer_id == customer_id,
        Payment.is_paid == False,
        Payment.due_date <= today
    ).first()
    
    if not pending_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending payments found for this customer"
        )
    
    customer = pending_payment.customer
    days_overdue = (today - pending_payment.due_date).days
    
    reminder = {
        'customer_name': customer.name,
        'phone': customer.phone,
        'amount': pending_payment.amount,
        'due_date': pending_payment.due_date,
        'days_overdue': days_overdue,
        'reminder_level': 'manual',
        'payment_id': pending_payment.id
    }
    
    message = reminder_service.create_reminder_message(reminder)
    
    return {
        "customer_name": customer.name,
        "phone": customer.phone,
        "message": message,
        "days_overdue": days_overdue
    }

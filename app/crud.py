from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Optional
from app.models import Customer, Payment, User
from app.schemas import CustomerCreate, CustomerUpdate, PaymentCreate, PaymentUpdate
from app.auth import get_password_hash


# Customer CRUD operations
def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """Create a new customer and generate payment schedule"""
    db_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        monthly_amount=customer.monthly_amount,
        start_date=customer.start_date,
        duration_months=customer.duration_months
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    # Generate payment schedule
    generate_payment_schedule(db, db_customer)
    
    return db_customer


def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    """Get a customer by ID"""
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Customer]:
    """Get all customers"""
    query = db.query(Customer)
    if active_only:
        query = query.filter(Customer.is_active == True)
    return query.offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, customer_update: CustomerUpdate) -> Optional[Customer]:
    """Update a customer"""
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    
    update_data = customer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db_customer.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int) -> bool:
    """Delete a customer (soft delete by setting is_active to False)"""
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    
    db_customer.is_active = False
    db_customer.updated_at = datetime.utcnow()
    db.commit()
    return True


def search_customers(db: Session, query: str) -> List[Customer]:
    """Search customers by name or phone"""
    return db.query(Customer).filter(
        (Customer.name.ilike(f"%{query}%")) | (Customer.phone.ilike(f"%{query}%"))
    ).filter(Customer.is_active == True).all()


# Payment CRUD operations
def generate_payment_schedule(db: Session, customer: Customer) -> List[Payment]:
    """Generate payment schedule for a customer"""
    payments = []
    current_date = customer.start_date
    
    for month in range(1, customer.duration_months + 1):
        # First payment is always for the registration month
        # Due date is 5th of the month, or registration date if after 5th
        if month == 1:
            # First payment - use current month
            if current_date.day <= 5:
                due_date = current_date.replace(day=5)
            else:
                # If registered after 5th, set due date as registration date for first payment
                due_date = current_date
        else:
            # Subsequent payments - always 5th of the month
            due_date = (customer.start_date + relativedelta(months=month-1)).replace(day=5)
        
        payment = Payment(
            customer_id=customer.id,
            due_date=due_date,
            amount=customer.monthly_amount,
            payment_month=due_date.month,
            payment_year=due_date.year,
            is_paid=False
        )
        db.add(payment)
        payments.append(payment)
    
    db.commit()
    return payments


def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
    """Get a payment by ID"""
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_customer_payments(db: Session, customer_id: int) -> List[Payment]:
    """Get all payments for a customer"""
    return db.query(Payment).filter(Payment.customer_id == customer_id).order_by(Payment.due_date).all()


def mark_payment_as_paid(db: Session, payment_id: int, paid_date: Optional[date] = None) -> Optional[Payment]:
    """Mark a payment as paid"""
    payment = get_payment(db, payment_id)
    if not payment:
        return None
    
    payment.is_paid = True
    payment.paid_date = paid_date or date.today()
    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


def update_payment(db: Session, payment_id: int, payment_update: PaymentUpdate) -> Optional[Payment]:
    """Update a payment"""
    payment = get_payment(db, payment_id)
    if not payment:
        return None
    
    update_data = payment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


def get_pending_payments(db: Session, as_of_date: Optional[date] = None) -> List[Payment]:
    """Get all pending payments"""
    if not as_of_date:
        as_of_date = date.today()
    
    return db.query(Payment).join(Customer).filter(
        Payment.is_paid == False,
        Payment.due_date <= as_of_date,
        Customer.is_active == True
    ).order_by(Payment.due_date).all()


def get_payments_by_month(db: Session, month: int, year: int) -> List[Payment]:
    """Get all payments for a specific month"""
    return db.query(Payment).filter(
        Payment.payment_month == month,
        Payment.payment_year == year
    ).all()


# User CRUD operations
def create_user(db: Session, username: str, email: str, password: str, shop_name: Optional[str] = None) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        shop_name=shop_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Customer(Base):
    """Customer model for storing customer information"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)  # Removed unique=True to allow multiple customers with same phone
    monthly_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    duration_months = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with payments
    payments = relationship("Payment", back_populates="customer", cascade="all, delete-orphan")


class Payment(Base):
    """Payment model for tracking monthly payments"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    is_paid = Column(Boolean, default=False)
    paid_date = Column(Date, nullable=True)
    payment_month = Column(Integer, nullable=False)  # 1-12
    payment_year = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with customer
    customer = relationship("Customer", back_populates="payments")


class User(Base):
    """User model for shop owner authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    shop_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

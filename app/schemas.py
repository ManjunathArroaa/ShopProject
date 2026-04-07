from __future__ import annotations
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List


# Customer Schemas
class CustomerBase(BaseModel):
    """Base customer schema"""
    name: str = Field(..., min_length=2, max_length=100, description="Customer name")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    monthly_amount: float = Field(..., gt=0, description="Monthly payment amount")
    start_date: date = Field(..., description="Scheme start date")
    duration_months: int = Field(..., ge=1, le=120, description="Duration in months")


class CustomerCreate(CustomerBase):
    """Schema for creating a customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    monthly_amount: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Payment Schemas
class PaymentBase(BaseModel):
    """Base payment schema"""
    due_date: date
    amount: float = Field(..., gt=0)
    payment_month: int = Field(..., ge=1, le=12)
    payment_year: int = Field(..., ge=2020)


class PaymentCreate(PaymentBase):
    """Schema for creating a payment"""
    customer_id: int


class PaymentUpdate(BaseModel):
    """Schema for updating a payment"""
    is_paid: bool
    paid_date: Optional[date] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Schema for payment response"""
    id: int
    customer_id: int
    is_paid: bool
    paid_date: Optional[date]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentWithCustomer(PaymentResponse):
    """Payment with customer details"""
    customer: CustomerResponse
    
    class Config:
        from_attributes = True


# Customer with Payments (must be after PaymentResponse)
class CustomerWithPayments(CustomerResponse):
    """Customer with payment details"""
    payments: List[PaymentResponse] = []
    total_paid: float = 0
    total_pending: float = 0
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_customers: int
    active_customers: int
    paid_this_month: int
    pending_this_month: int
    total_collection_this_month: float
    pending_amount_this_month: float
    total_collection_overall: float


class PendingCustomerInfo(BaseModel):
    """Pending customer information for follow-ups"""
    customer_id: int
    customer_name: str
    phone: str
    amount: float
    due_date: date
    days_overdue: int
    
    class Config:
        from_attributes = True


# User/Auth Schemas
class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="Email address")
    shop_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6, description="Password")


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str

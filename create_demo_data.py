"""
Demo Data Script - Creates sample customers and payments for testing

This script helps you quickly test the application with demo data.
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from app.database import SessionLocal, init_db
from app.crud import create_user, create_customer
from app.schemas import CustomerCreate
from app.models import Payment
import random


def create_demo_data():
    """Create demo data for testing"""
    print("🚀 Creating demo data...")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Create demo user if not exists
        from app.crud import get_user_by_username
        if not get_user_by_username(db, "demo"):
            user = create_user(
                db=db,
                username="demo",
                email="demo@example.com",
                password="demo123",
                shop_name="Demo Saree Shop"
            )
            print(f"✅ Created demo user: demo / demo123")
        else:
            print("ℹ️  Demo user already exists")
        
        # Create sample customers
        customers_data = [
            {
                "name": "Rajesh Kumar",
                "phone": "9876543210",
                "monthly_amount": 1000,
                "start_date": date.today() - relativedelta(months=3),
                "duration_months": 12
            },
            {
                "name": "Priya Sharma",
                "phone": "9876543211",
                "monthly_amount": 1500,
                "start_date": date.today() - relativedelta(months=2),
                "duration_months": 12
            },
            {
                "name": "Amit Patel",
                "phone": "9876543212",
                "monthly_amount": 2000,
                "start_date": date.today() - relativedelta(months=4),
                "duration_months": 10
            },
            {
                "name": "Sneha Reddy",
                "phone": "9876543213",
                "monthly_amount": 1200,
                "start_date": date.today() - relativedelta(months=1),
                "duration_months": 12
            },
            {
                "name": "Vikram Singh",
                "phone": "7676661444",
                "monthly_amount": 1800,
                "start_date": date.today() - relativedelta(months=5),
                "duration_months": 12
            }
        ]
        
        created_customers = []
        for customer_data in customers_data:
            customer = CustomerCreate(**customer_data)
            db_customer = create_customer(db, customer)
            created_customers.append(db_customer)
            print(f"✅ Created customer: {db_customer.name}")
        
        # Mark some payments as paid randomly
        for customer in created_customers:
            payments = customer.payments
            
            # Mark past payments as paid (80% probability)
            for payment in payments:
                if payment.due_date < date.today():
                    if random.random() < 0.8:  # 80% chance of being paid
                        payment.is_paid = True
                        payment.paid_date = payment.due_date + timedelta(days=random.randint(0, 7))
        
        db.commit()
        print(f"✅ Updated payment statuses")
        
        print("\n" + "="*50)
        print("🎉 Demo data created successfully!")
        print("="*50)
        print("\nLogin credentials:")
        print("  Username: demo")
        print("  Password: demo123")
        print("\nYou can now start the application and login with these credentials.")
        print("\n")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()

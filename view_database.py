"""
Quick Database Viewer
Run this to see your data in the terminal
"""

from app.database import SessionLocal
from app.models import Customer, Payment, User
from datetime import date


def view_database():
    """View all data in the database"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("📊 PAYMENT REMINDER DATABASE VIEWER")
        print("="*60)
        
        # Users
        print("\n👤 USERS:")
        print("-" * 60)
        users = db.query(User).all()
        for user in users:
            print(f"  ID: {user.id} | Username: {user.username} | Email: {user.email}")
            print(f"  Shop: {user.shop_name or 'N/A'} | Active: {user.is_active}")
            print()
        
        # Customers
        print("\n👥 CUSTOMERS:")
        print("-" * 60)
        customers = db.query(Customer).all()
        for customer in customers:
            print(f"  ID: {customer.id} | Name: {customer.name}")
            print(f"  Phone: {customer.phone}")
            print(f"  Amount: ₹{customer.monthly_amount}/month | Duration: {customer.duration_months} months")
            print(f"  Start: {customer.start_date} | Active: {customer.is_active}")
            
            # Count payments
            paid = sum(1 for p in customer.payments if p.is_paid)
            pending = sum(1 for p in customer.payments if not p.is_paid)
            print(f"  Payments: {paid} paid, {pending} pending")
            print()
        
        # Payments Summary
        print("\n💳 PAYMENTS SUMMARY:")
        print("-" * 60)
        all_payments = db.query(Payment).all()
        total_payments = len(all_payments)
        paid_payments = sum(1 for p in all_payments if p.is_paid)
        pending_payments = sum(1 for p in all_payments if not p.is_paid)
        
        total_paid_amount = sum(p.amount for p in all_payments if p.is_paid)
        total_pending_amount = sum(p.amount for p in all_payments if not p.is_paid)
        
        print(f"  Total Payments: {total_payments}")
        print(f"  Paid: {paid_payments} (₹{total_paid_amount:,.2f})")
        print(f"  Pending: {pending_payments} (₹{total_pending_amount:,.2f})")
        
        # Recent Payments
        print("\n📅 RECENT PAYMENTS (Last 10):")
        print("-" * 60)
        recent = db.query(Payment).order_by(Payment.created_at.desc()).limit(10).all()
        for payment in recent:
            status = "✅ PAID" if payment.is_paid else "❌ PENDING"
            print(f"  {payment.customer.name}: ₹{payment.amount} - Due: {payment.due_date} - {status}")
        
        # Overdue Payments
        print("\n⚠️ OVERDUE PAYMENTS:")
        print("-" * 60)
        today = date.today()
        overdue = db.query(Payment).filter(
            Payment.is_paid == False,
            Payment.due_date < today
        ).all()
        
        if overdue:
            for payment in overdue:
                days_overdue = (today - payment.due_date).days
                print(f"  {payment.customer.name}: ₹{payment.amount}")
                print(f"    Due: {payment.due_date} ({days_overdue} days overdue)")
                print(f"    Phone: {payment.customer.phone}")
                print()
        else:
            print("  No overdue payments! 🎉")
        
        print("\n" + "="*60)
        print("✅ Database view complete!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


def view_customer_details(customer_id):
    """View detailed information for a specific customer"""
    db = SessionLocal()
    
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            print(f"❌ Customer ID {customer_id} not found")
            return
        
        print("\n" + "="*60)
        print(f"👤 CUSTOMER DETAILS - {customer.name}")
        print("="*60)
        
        print(f"\n📞 Contact: {customer.phone}")
        print(f"💰 Monthly Amount: ₹{customer.monthly_amount}")
        print(f"📅 Start Date: {customer.start_date}")
        print(f"⏱️ Duration: {customer.duration_months} months")
        print(f"✅ Status: {'Active' if customer.is_active else 'Inactive'}")
        
        print(f"\n💳 PAYMENT HISTORY:")
        print("-" * 60)
        
        for payment in customer.payments:
            status = "✅ PAID" if payment.is_paid else "❌ PENDING"
            paid_info = f" (Paid: {payment.paid_date})" if payment.is_paid else ""
            print(f"  {payment.payment_month:02d}/{payment.payment_year} - ₹{payment.amount}")
            print(f"    Due: {payment.due_date} | {status}{paid_info}")
        
        # Summary
        total_paid = sum(p.amount for p in customer.payments if p.is_paid)
        total_pending = sum(p.amount for p in customer.payments if not p.is_paid)
        
        print(f"\n📊 SUMMARY:")
        print(f"  Total Paid: ₹{total_paid:,.2f}")
        print(f"  Total Pending: ₹{total_pending:,.2f}")
        print(f"  Total Expected: ₹{customer.monthly_amount * customer.duration_months:,.2f}")
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # View specific customer
        try:
            customer_id = int(sys.argv[1])
            view_customer_details(customer_id)
        except ValueError:
            print("Usage: python view_database.py [customer_id]")
    else:
        # View all data
        view_database()

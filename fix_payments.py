"""
Fix payment schedule for a customer - regenerate payments
"""

from app.database import SessionLocal
from app.models import Customer, Payment
from app.crud import generate_payment_schedule


def fix_customer_payments(customer_id):
    """Delete and regenerate payment schedule for a customer"""
    db = SessionLocal()
    
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            print(f"❌ Customer ID {customer_id} not found")
            return False
        
        print(f"\n📋 Customer: {customer.name}")
        print(f"   Phone: {customer.phone}")
        print(f"   Start Date: {customer.start_date}")
        print(f"   Duration: {customer.duration_months} months")
        
        # Delete existing payments
        existing_payments = db.query(Payment).filter(Payment.customer_id == customer_id).all()
        print(f"\n🗑️  Deleting {len(existing_payments)} existing payments...")
        
        for payment in existing_payments:
            db.delete(payment)
        db.commit()
        
        # Generate new payment schedule
        print(f"🔄 Generating new payment schedule...")
        new_payments = generate_payment_schedule(db, customer)
        
        print(f"\n✅ Created {len(new_payments)} new payments:")
        for i, payment in enumerate(new_payments, 1):
            status = "✅ Paid" if payment.is_paid else "❌ Pending"
            print(f"   {i}. {payment.payment_month:02d}/{payment.payment_year} - Due: {payment.due_date} - {status}")
        
        print(f"\n🎉 Payment schedule fixed successfully!\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def fix_all_customers():
    """Regenerate payment schedule for all customers"""
    db = SessionLocal()
    
    try:
        customers = db.query(Customer).filter(Customer.is_active == True).all()
        
        print(f"\n{'='*60}")
        print(f"🔄 REGENERATING PAYMENT SCHEDULES FOR ALL CUSTOMERS")
        print(f"{'='*60}\n")
        print(f"Found {len(customers)} active customers\n")
        
        confirm = input("This will delete and recreate all payment schedules. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.")
            return
        
        for customer in customers:
            print(f"\n{'─'*60}")
            fix_customer_payments(customer.id)
        
        print(f"\n{'='*60}")
        print(f"✅ ALL PAYMENT SCHEDULES REGENERATED!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


def fix_by_phone(phone):
    """Find customer by phone and fix their payments"""
    db = SessionLocal()
    
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        
        if not customer:
            print(f"\n❌ No customer found with phone: {phone}\n")
            return False
        
        print(f"\n✅ Found customer:")
        print(f"   ID: {customer.id}")
        print(f"   Name: {customer.name}")
        
        db.close()  # Close before calling fix function
        return fix_customer_payments(customer.id)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if not db.is_active:
            db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "all":
            fix_all_customers()
        elif arg.startswith("phone:"):
            # Usage: python fix_payments.py phone:7676661444
            phone = arg.split(":", 1)[1]
            fix_by_phone(phone)
        elif len(arg) == 10 and arg.isdigit():
            # Phone number without prefix
            fix_by_phone(arg)
        else:
            try:
                customer_id = int(arg)
                fix_customer_payments(customer_id)
            except ValueError:
                print(f"\n❌ Invalid argument: {arg}")
                print("\nUsage:")
                print("  python fix_payments.py <customer_id>  # Fix by customer ID")
                print("  python fix_payments.py 7676661444     # Fix by phone number")
                print("  python fix_payments.py phone:7676661444")
                print("  python fix_payments.py all            # Fix all customers")
    else:
        print("\nUsage:")
        print("  python fix_payments.py <customer_id>  # Fix by customer ID") 
        print("  python fix_payments.py 7676661444     # Fix by phone number")
        print("  python fix_payments.py all            # Fix all customers")
        print("\nExample:")
        print("  python fix_payments.py 7676661444     # Fix manju's payments")

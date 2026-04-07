"""
Quick script to find customer by phone and fix their payments
"""

from app.database import SessionLocal
from app.models import Customer
import subprocess
import sys


def find_and_fix_by_phone(phone):
    """Find customer by phone and regenerate their payment schedule"""
    db = SessionLocal()
    
    try:
        customer = db.query(Customer).filter(Customer.phone == phone).first()
        
        if not customer:
            print(f"\n❌ No customer found with phone: {phone}\n")
            return False
        
        print(f"\n✅ Found customer:")
        print(f"   ID: {customer.id}")
        print(f"   Name: {customer.name}")
        print(f"   Phone: {customer.phone}")
        print(f"   Start Date: {customer.start_date}")
        print(f"   Duration: {customer.duration_months} months")
        
        # Ask for confirmation
        confirm = input(f"\nRegenerate payment schedule for {customer.name}? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.")
            return False
        
        # Run fix_payments.py with customer ID
        print(f"\n🔄 Running payment schedule fix...\n")
        result = subprocess.run([sys.executable, "fix_payments.py", str(customer.id)], 
                              capture_output=False, text=True)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        phone = sys.argv[1]
        find_and_fix_by_phone(phone)
    else:
        # Default to the phone number mentioned
        find_and_fix_by_phone("7676661444")

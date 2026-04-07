"""
Check if a phone number exists in the database
"""

from app.database import SessionLocal
from app.models import Customer


def check_phone(phone_number):
    """Check if a phone number is already registered"""
    db = SessionLocal()
    
    try:
        existing = db.query(Customer).filter(Customer.phone == phone_number).first()
        
        if existing:
            print(f"\n❌ Phone number {phone_number} is ALREADY REGISTERED!")
            print(f"   Customer: {existing.name}")
            print(f"   ID: {existing.id}")
            print(f"   Monthly Amount: ₹{existing.monthly_amount}")
            print(f"   Status: {'Active' if existing.is_active else 'Inactive'}")
            print(f"\n💡 Use a different phone number or update this customer.\n")
            return False
        else:
            print(f"\n✅ Phone number {phone_number} is AVAILABLE!")
            print(f"   You can use this number to create a new customer.\n")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()


def list_all_phones():
    """List all registered phone numbers"""
    db = SessionLocal()
    
    try:
        customers = db.query(Customer).filter(Customer.is_active == True).all()
        
        print("\n" + "="*60)
        print("📞 ALL REGISTERED PHONE NUMBERS")
        print("="*60)
        
        for customer in customers:
            print(f"  {customer.phone} - {customer.name} (ID: {customer.id})")
        
        print(f"\nTotal: {len(customers)} active customers")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


def find_by_name(name_search):
    """Find customers by name"""
    db = SessionLocal()
    
    try:
        customers = db.query(Customer).filter(
            Customer.name.ilike(f"%{name_search}%")
        ).all()
        
        if customers:
            print(f"\n🔍 Found {len(customers)} customer(s) matching '{name_search}':")
            print("-" * 60)
            for customer in customers:
                print(f"\n  Name: {customer.name}")
                print(f"  Phone: {customer.phone}")
                print(f"  ID: {customer.id}")
                print(f"  Amount: ₹{customer.monthly_amount}/month")
                print(f"  Status: {'Active' if customer.is_active else 'Inactive'}")
        else:
            print(f"\n❌ No customers found matching '{name_search}'")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_all_phones()
        elif command == "check" and len(sys.argv) > 2:
            check_phone(sys.argv[2])
        elif command == "find" and len(sys.argv) > 2:
            find_by_name(sys.argv[2])
        else:
            print("\nUsage:")
            print("  python check_customer.py list              # List all phones")
            print("  python check_customer.py check 9876543210  # Check if phone exists")
            print("  python check_customer.py find Rajesh       # Find by name")
    else:
        list_all_phones()

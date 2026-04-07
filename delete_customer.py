"""
Delete or deactivate a customer by ID or phone number
"""

from app.database import SessionLocal
from app.models import Customer


def delete_customer_by_phone(phone_number, soft_delete=True):
    """Delete or deactivate a customer by phone number
    
    Args:
        phone_number: Phone number to search for
        soft_delete: If True, deactivate instead of delete (recommended)
    """
    db = SessionLocal()
    
    try:
        customer = db.query(Customer).filter(Customer.phone == phone_number).first()
        
        if not customer:
            print(f"\n❌ No customer found with phone number: {phone_number}\n")
            return False
        
        print(f"\n📋 Found customer:")
        print(f"   Name: {customer.name}")
        print(f"   Phone: {customer.phone}")
        print(f"   ID: {customer.id}")
        print(f"   Monthly Amount: ₹{customer.monthly_amount}")
        
        # Count payments
        paid = sum(1 for p in customer.payments if p.is_paid)
        pending = sum(1 for p in customer.payments if not p.is_paid)
        print(f"   Payments: {paid} paid, {pending} pending")
        
        # Ask for confirmation
        if soft_delete:
            confirm = input(f"\n⚠️  Deactivate this customer? (yes/no): ")
        else:
            confirm = input(f"\n⚠️  PERMANENTLY DELETE this customer and all payments? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.\n")
            return False
        
        if soft_delete:
            customer.is_active = False
            db.commit()
            print(f"✅ Customer '{customer.name}' has been deactivated.\n")
        else:
            db.delete(customer)
            db.commit()
            print(f"✅ Customer '{customer.name}' has been permanently deleted.\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def delete_customer_by_id(customer_id, soft_delete=True):
    """Delete or deactivate a customer by ID"""
    db = SessionLocal()
    
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            print(f"\n❌ No customer found with ID: {customer_id}\n")
            return False
        
        print(f"\n📋 Found customer:")
        print(f"   Name: {customer.name}")
        print(f"   Phone: {customer.phone}")
        print(f"   ID: {customer.id}")
        
        if soft_delete:
            confirm = input(f"\n⚠️  Deactivate this customer? (yes/no): ")
        else:
            confirm = input(f"\n⚠️  PERMANENTLY DELETE this customer? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.\n")
            return False
        
        if soft_delete:
            customer.is_active = False
            db.commit()
            print(f"✅ Customer deactivated successfully.\n")
        else:
            db.delete(customer)
            db.commit()
            print(f"✅ Customer deleted successfully.\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def reactivate_customer(phone_or_id):
    """Reactivate a deactivated customer"""
    db = SessionLocal()
    
    try:
        # Try phone first
        if phone_or_id.isdigit() and len(phone_or_id) >= 10:
            customer = db.query(Customer).filter(Customer.phone == phone_or_id).first()
        else:
            # Try ID
            try:
                customer_id = int(phone_or_id)
                customer = db.query(Customer).filter(Customer.id == customer_id).first()
            except ValueError:
                print(f"❌ Invalid input: {phone_or_id}\n")
                return False
        
        if not customer:
            print(f"\n❌ No customer found\n")
            return False
        
        if customer.is_active:
            print(f"\nℹ️  Customer '{customer.name}' is already active.\n")
            return False
        
        customer.is_active = True
        db.commit()
        print(f"\n✅ Customer '{customer.name}' has been reactivated.\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python delete_customer.py phone 7676661444        # Deactivate by phone")
        print("  python delete_customer.py id 1                    # Deactivate by ID")
        print("  python delete_customer.py delete-phone 7676661444 # Permanently delete by phone")
        print("  python delete_customer.py delete-id 1             # Permanently delete by ID")
        print("  python delete_customer.py reactivate 7676661444   # Reactivate customer")
        print()
    else:
        command = sys.argv[1]
        
        if command == "phone" and len(sys.argv) > 2:
            delete_customer_by_phone(sys.argv[2], soft_delete=True)
        elif command == "id" and len(sys.argv) > 2:
            delete_customer_by_id(int(sys.argv[2]), soft_delete=True)
        elif command == "delete-phone" and len(sys.argv) > 2:
            delete_customer_by_phone(sys.argv[2], soft_delete=False)
        elif command == "delete-id" and len(sys.argv) > 2:
            delete_customer_by_id(int(sys.argv[2]), soft_delete=False)
        elif command == "reactivate" and len(sys.argv) > 2:
            reactivate_customer(sys.argv[2])
        else:
            print("Invalid command. Use --help for usage.")

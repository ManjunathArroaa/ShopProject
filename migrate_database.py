"""
Recreate database with updated schema (allows duplicate phone numbers)

This will:
1. Backup existing database
2. Create new database with updated schema
3. Preserve your data if possible
"""

import shutil
import os
from datetime import datetime
from app.database import engine, Base, SessionLocal
from app.models import Customer, Payment, User

def recreate_database():
    """Recreate database with new schema"""
    
    db_file = "payment_reminder.db"
    
    # Backup existing database
    if os.path.exists(db_file):
        backup_name = f"payment_reminder_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy(db_file, backup_name)
        print(f"✅ Backed up existing database to: {backup_name}")
    
    # Get existing data before dropping
    existing_data = None
    if os.path.exists(db_file):
        try:
            db = SessionLocal()
            existing_data = {
                'users': db.query(User).all(),
                'customers': db.query(Customer).all(),
                'payments': db.query(Payment).all()
            }
            db.close()
            print(f"✅ Exported {len(existing_data['users'])} users, {len(existing_data['customers'])} customers, {len(existing_data['payments'])} payments")
        except Exception as e:
            print(f"⚠️  Could not export existing data: {e}")
    
    # Drop all tables and recreate
    print("\n🔄 Recreating database with new schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database recreated with updated schema (phone numbers can now be duplicated)")
    
    # Restore data if available
    if existing_data:
        print("\n🔄 Restoring existing data...")
        db = SessionLocal()
        try:
            # Restore users
            for user in existing_data['users']:
                db.add(User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    hashed_password=user.hashed_password,
                    shop_name=user.shop_name,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ))
            db.commit()
            print(f"✅ Restored {len(existing_data['users'])} users")
            
            # Restore customers
            for customer in existing_data['customers']:
                db.add(Customer(
                    id=customer.id,
                    name=customer.name,
                    phone=customer.phone,
                    monthly_amount=customer.monthly_amount,
                    start_date=customer.start_date,
                    duration_months=customer.duration_months,
                    is_active=customer.is_active,
                    created_at=customer.created_at,
                    updated_at=customer.updated_at
                ))
            db.commit()
            print(f"✅ Restored {len(existing_data['customers'])} customers")
            
            # Restore payments
            for payment in existing_data['payments']:
                db.add(Payment(
                    id=payment.id,
                    customer_id=payment.customer_id,
                    due_date=payment.due_date,
                    amount=payment.amount,
                    is_paid=payment.is_paid,
                    paid_date=payment.paid_date,
                    payment_month=payment.payment_month,
                    payment_year=payment.payment_year,
                    notes=payment.notes,
                    created_at=payment.created_at,
                    updated_at=payment.updated_at
                ))
            db.commit()
            print(f"✅ Restored {len(existing_data['payments'])} payments")
            
            print("\n🎉 All data restored successfully!")
            
        except Exception as e:
            print(f"❌ Error restoring data: {e}")
            db.rollback()
        finally:
            db.close()
    else:
        print("\n⚠️  No existing data to restore. Database is empty.")
        print("Run 'python create_demo_data.py' to create demo data.")
    
    print("\n" + "="*60)
    print("✅ Database migration complete!")
    print("="*60)
    print("\nYou can now:")
    print("1. Add customers with duplicate phone numbers")
    print("2. Restart your application server")
    print()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📦 DATABASE MIGRATION TOOL")
    print("="*60)
    print("\nThis will recreate the database to allow duplicate phone numbers.")
    print("Your existing data will be preserved.\n")
    
    confirm = input("Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        recreate_database()
    else:
        print("❌ Migration cancelled.")

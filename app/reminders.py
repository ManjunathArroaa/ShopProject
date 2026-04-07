from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
from sqlalchemy.orm import Session
from typing import List
import logging
from app.database import SessionLocal
from app.models import Payment, Customer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReminderService:
    """Service for sending payment reminders"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        
    def start(self):
        """Start the reminder scheduler"""
        # Schedule reminders to run daily at 9 AM
        self.scheduler.add_job(
            self.send_daily_reminders,
            'cron',
            hour=9,
            minute=0,
            id='daily_reminders'
        )
        
        self.scheduler.start()
        logger.info("✅ Reminder scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("❌ Reminder scheduler stopped")
    
    def get_customers_to_remind(self, db: Session) -> List[dict]:
        """Get list of customers who need reminders"""
        today = date.today()
        
        # Get pending payments that are due or overdue
        pending_payments = db.query(Payment).join(Customer).filter(
            Payment.is_paid == False,
            Payment.due_date <= today,
            Customer.is_active == True
        ).all()
        
        reminders = []
        for payment in pending_payments:
            days_overdue = (today - payment.due_date).days
            
            # Determine reminder level based on days overdue
            reminder_level = None
            if days_overdue == 0:
                reminder_level = "due_today"
            elif days_overdue == 5:
                reminder_level = "first_reminder"
            elif days_overdue == 10:
                reminder_level = "second_reminder"
            elif days_overdue == 15:
                reminder_level = "final_reminder"
            elif days_overdue > 15 and days_overdue % 7 == 0:
                reminder_level = "overdue"
            
            if reminder_level:
                reminders.append({
                    'customer_name': payment.customer.name,
                    'phone': payment.customer.phone,
                    'amount': payment.amount,
                    'due_date': payment.due_date,
                    'days_overdue': days_overdue,
                    'reminder_level': reminder_level,
                    'payment_id': payment.id
                })
        
        return reminders
    
    def send_daily_reminders(self):
        """Send daily reminders to customers with pending payments"""
        logger.info("📧 Running daily reminder check...")
        
        db = SessionLocal()
        try:
            reminders = self.get_customers_to_remind(db)
            
            if not reminders:
                logger.info("No reminders to send today")
                return
            
            logger.info(f"Found {len(reminders)} customers to remind")
            
            for reminder in reminders:
                message = self.create_reminder_message(reminder)
                self.send_reminder(
                    phone=reminder['phone'],
                    message=message,
                    customer_name=reminder['customer_name'],
                    amount=reminder['amount'],
                    due_date=reminder['due_date'].strftime('%d-%b-%Y'),
                    days_overdue=reminder['days_overdue']
                )
                logger.info(f"Sent {reminder['reminder_level']} to {reminder['customer_name']}")
        
        except Exception as e:
            logger.error(f"Error in daily reminders: {e}")
        finally:
            db.close()
    
    def create_reminder_message(self, reminder: dict) -> str:
        """Create reminder message text"""
        customer_name = reminder['customer_name']
        amount = reminder['amount']
        due_date = reminder['due_date'].strftime('%d-%b-%Y')
        days_overdue = reminder['days_overdue']
        
        messages = {
            'due_today': f"Hello {customer_name}, this is a reminder that your payment of ₹{amount} is due today. Please make the payment at your earliest convenience. Thank you!",
            
            'first_reminder': f"Dear {customer_name}, your payment of ₹{amount} was due on {due_date}. It has been {days_overdue} days overdue. Kindly clear the payment soon. Thank you!",
            
            'second_reminder': f"Hello {customer_name}, your payment of ₹{amount} is now {days_overdue} days overdue (due date: {due_date}). Please clear the payment urgently. Thank you!",
            
            'final_reminder': f"Dear {customer_name}, FINAL REMINDER: Your payment of ₹{amount} is {days_overdue} days overdue. Please clear the payment immediately to avoid any inconvenience. Thank you!",
            
            'overdue': f"Hello {customer_name}, your payment of ₹{amount} is significantly overdue ({days_overdue} days). Please contact us to clear the payment. Thank you!"
        }
        
        return messages.get(reminder['reminder_level'], f"Payment reminder for ₹{amount}")
    
    def send_reminder(self, phone: str, message: str, customer_name: str = "", amount: float = 0, due_date: str = "", days_overdue: int = 0):
        """
        Send reminder via WhatsApp using Twilio
        
        Args:
            phone: Customer phone number
            message: Message text (fallback)
            customer_name: Customer name
            amount: Payment amount
            due_date: Due date string
            days_overdue: Days overdue
        """
        try:
            from app.twilio_service import twilio_service
            
            # Use Twilio service to send WhatsApp message
            result = twilio_service.send_payment_reminder(
                customer_name=customer_name,
                phone=phone,
                amount=amount,
                due_date=due_date,
                days_overdue=days_overdue
            )
            
            if result["success"]:
                logger.info(f"✅ Reminder sent to {phone} | Status: {result['status']}")
            else:
                logger.error(f"❌ Failed to send reminder to {phone}: {result['message']}")
            
            return result["success"]
        
        except Exception as e:
            logger.error(f"❌ Error sending reminder: {e}")
            # Fallback to logging
            logger.info(f"[REMINDER] To: {phone} | Message: {message}")
            return False


# Global reminder service instance
reminder_service = ReminderService()


def start_reminder_service():
    """Start the reminder service"""
    reminder_service.start()


def stop_reminder_service():
    """Stop the reminder service"""
    reminder_service.stop()


def send_manual_reminder(customer_id: int):
    """Send a manual reminder to a specific customer"""
    db = SessionLocal()
    try:
        # Get pending payments for this customer
        today = date.today()
        pending_payment = db.query(Payment).filter(
            Payment.customer_id == customer_id,
            Payment.is_paid == False,
            Payment.due_date <= today
        ).first()
        
        if not pending_payment:
            return {"status": "error", "message": "No pending payments found"}
        
        customer = pending_payment.customer
        days_overdue = (today - pending_payment.due_date).days
        
        reminder = {
            'customer_name': customer.name,
            'phone': customer.phone,
            'amount': pending_payment.amount,
            'due_date': pending_payment.due_date,
            'days_overdue': days_overdue,
            'reminder_level': 'manual',
            'payment_id': pending_payment.id
        }
        
        message = reminder_service.create_reminder_message(reminder)
        reminder_service.send_reminder(
            phone=customer.phone,
            message=message,
            customer_name=customer.name,
            amount=pending_payment.amount,
            due_date=pending_payment.due_date.strftime('%d-%b-%Y'),
            days_overdue=days_overdue
        )
        
        return {"status": "success", "message": f"Reminder sent to {customer.name}"}
    
    except Exception as e:
        logger.error(f"Error sending manual reminder: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

"""
Twilio WhatsApp Integration Service

This module handles sending WhatsApp messages via Twilio API.
"""

import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class TwilioWhatsAppService:
    """Service for sending WhatsApp messages via Twilio"""
    
    def __init__(self):
        self.enabled = settings.ENABLE_WHATSAPP
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_WHATSAPP_FROM
        self.client = None
        
        if self.enabled:
            if not all([self.account_sid, self.auth_token, self.from_number]):
                logger.warning("⚠️  Twilio WhatsApp is enabled but credentials are missing!")
                self.enabled = False
            else:
                try:
                    from twilio.rest import Client
                    self.client = Client(self.account_sid, self.auth_token)
                    logger.info("✅ Twilio WhatsApp service initialized")
                except ImportError:
                    logger.error("❌ Twilio library not installed. Run: pip install twilio")
                    self.enabled = False
                except Exception as e:
                    logger.error(f"❌ Error initializing Twilio client: {e}")
                    self.enabled = False
    
    def format_phone_number(self, phone: str) -> str:
        """
        Format phone number for WhatsApp
        
        Args:
            phone: Phone number (e.g., "9876543210" or "+919876543210")
        
        Returns:
            Formatted WhatsApp number (e.g., "whatsapp:+919876543210")
        """
        # Remove any spaces, dashes, or parentheses
        phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Add country code if not present (assuming India +91)
        if not phone.startswith("+"):
            if not phone.startswith("91"):
                phone = "91" + phone
            phone = "+" + phone
        
        # Add whatsapp: prefix
        if not phone.startswith("whatsapp:"):
            phone = f"whatsapp:{phone}"
        
        return phone
    
    def send_message(self, to_phone: str, message: str) -> dict:
        """
        Send WhatsApp message via Twilio
        
        Args:
            to_phone: Recipient phone number
            message: Message text to send
        
        Returns:
            dict with status and details
        """
        if not self.enabled:
            logger.info(f"[DRY RUN] Would send to {to_phone}: {message}")
            return {
                "success": True,
                "status": "dry_run",
                "message": "WhatsApp not enabled - message logged only",
                "sid": None
            }
        
        try:
            # Format phone numbers
            to_number = self.format_phone_number(to_phone)
            
            # Send message via Twilio
            twilio_message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"✅ WhatsApp sent to {to_phone} | SID: {twilio_message.sid}")
            
            return {
                "success": True,
                "status": "sent",
                "message": "WhatsApp message sent successfully",
                "sid": twilio_message.sid,
                "to": to_number
            }
        
        except Exception as e:
            logger.error(f"❌ Error sending WhatsApp to {to_phone}: {e}")
            return {
                "success": False,
                "status": "error",
                "message": str(e),
                "sid": None
            }
    
    def send_payment_reminder(
        self,
        customer_name: str,
        phone: str,
        amount: float,
        due_date: str,
        days_overdue: int = 0
    ) -> dict:
        """
        Send payment reminder message
        
        Args:
            customer_name: Name of the customer
            phone: Customer phone number
            amount: Payment amount
            due_date: Due date string
            days_overdue: Number of days overdue
        
        Returns:
            dict with status and details
        """
        business_name = settings.BUSINESS_NAME
        
        if days_overdue == 0:
            message = (
                f"Dear {customer_name},\n\n"
                f"This is a reminder that your payment of ₹{amount} is due today.\n\n"
                f"Please make the payment at your earliest convenience.\n\n"
                f"Thank you,\n{business_name}"
            )
        elif days_overdue <= 5:
            message = (
                f"Dear {customer_name},\n\n"
                f"Your Installment of ₹{amount} was due on {due_date}.\n"
                f"It is now {days_overdue} day(s) overdue.\n\n"
                f"Kindly clear the payment to following UPI Id : 7676661444@ybl \n\n"
                f"Thank you,\n{business_name}"
            )
        elif days_overdue <= 10:
            message = (
                f"Dear {customer_name},\n\n"
                f"REMINDER: Your payment of ₹{amount} is {days_overdue} days overdue (due: {due_date}).\n\n"
                f"Please clear the payment urgently.\n\n"
                f"Thank you,\n{business_name}"
            )
        else:
            message = (
                f"Dear {customer_name},\n\n"
                f"FINAL REMINDER: Your payment of ₹{amount} is {days_overdue} days overdue.\n\n"
                f"Please clear the payment immediately to avoid any inconvenience.\n\n"
                f"For any queries, please contact us.\n\n"
                f"Thank you,\n{business_name}"
            )
        
        return self.send_message(phone, message)


# Global instance
twilio_service = TwilioWhatsAppService()

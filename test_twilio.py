"""
Test Twilio WhatsApp Integration

Run this script to test your Twilio WhatsApp setup:
    python test_twilio.py
"""

import sys
from app.config import settings
from app.twilio_service import twilio_service


def test_configuration():
    """Test if Twilio is properly configured"""
    print("\n" + "="*60)
    print("TWILIO WHATSAPP CONFIGURATION TEST")
    print("="*60 + "\n")
    
    print("📋 Configuration Status:")
    print(f"   • WhatsApp Enabled: {settings.ENABLE_WHATSAPP}")
    print(f"   • Account SID: {settings.TWILIO_ACCOUNT_SID[:10] + '...' if settings.TWILIO_ACCOUNT_SID else 'NOT SET'}")
    print(f"   • Auth Token: {'***' + settings.TWILIO_AUTH_TOKEN[-4:] if settings.TWILIO_AUTH_TOKEN else 'NOT SET'}")
    print(f"   • From Number: {settings.TWILIO_WHATSAPP_FROM or 'NOT SET'}")
    print(f"   • Business Name: {settings.BUSINESS_NAME}\n")
    
    if not settings.ENABLE_WHATSAPP:
        print("⚠️  WhatsApp is DISABLED")
        print("   Messages will be logged only (not sent)")
        print("   To enable, set ENABLE_WHATSAPP=true in .env file\n")
        return False
    
    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_WHATSAPP_FROM]):
        print("❌ ERROR: Twilio credentials not configured!")
        print("   Please set the following in your .env file:")
        print("   - TWILIO_ACCOUNT_SID")
        print("   - TWILIO_AUTH_TOKEN")
        print("   - TWILIO_WHATSAPP_FROM\n")
        return False
    
    print("✅ Configuration looks good!\n")
    return True


def test_send_message():
    """Test sending a WhatsApp message"""
    print("="*60)
    print("SEND TEST MESSAGE")
    print("="*60 + "\n")
    
    # Get phone number from user
    phone = input("Enter your phone number to test (e.g., 9876543210): ").strip()
    
    if not phone:
        print("❌ No phone number provided. Test cancelled.")
        return
    
    print(f"\n📱 Sending test message to {phone}...")
    print("   (Make sure you've joined the Twilio WhatsApp sandbox!)\n")
    
    # Send test message
    result = twilio_service.send_payment_reminder(
        customer_name="Test Customer",
        phone=phone,
        amount=1000,
        due_date="07-Apr-2026",
        days_overdue=2
    )
    
    print("\n📊 Result:")
    print(f"   • Success: {result['success']}")
    print(f"   • Status: {result['status']}")
    print(f"   • Message: {result['message']}")
    if result.get('sid'):
        print(f"   • Twilio SID: {result['sid']}")
    if result.get('to'):
        print(f"   • Sent To: {result['to']}")
    
    if result['success']:
        print("\n✅ Message sent successfully!")
        print("   Check your WhatsApp for the message.\n")
    else:
        print("\n❌ Message failed to send!")
        print("   Check the error message above.\n")


def test_phone_formatting():
    """Test phone number formatting"""
    print("="*60)
    print("PHONE NUMBER FORMATTING TEST")
    print("="*60 + "\n")
    
    test_numbers = [
        "9876543210",
        "+919876543210",
        "919876543210",
        "+91 98765 43210",
        "98765-43210"
    ]
    
    print("Testing phone number formatting:\n")
    for phone in test_numbers:
        formatted = twilio_service.format_phone_number(phone)
        print(f"   {phone:<20} → {formatted}")
    
    print("\n✅ All phone numbers formatted correctly!\n")


def main():
    """Main test function"""
    print("\n🚀 Starting Twilio WhatsApp Integration Tests...\n")
    
    # Test 1: Configuration
    if not test_configuration():
        print("⚠️  Please fix configuration issues before proceeding.\n")
        if not settings.ENABLE_WHATSAPP:
            print("💡 Tip: You can still test in DRY RUN mode (messages logged only)")
            print("   Set ENABLE_WHATSAPP=false to test without sending actual messages\n")
    
    # Test 2: Phone formatting
    test_phone_formatting()
    
    # Test 3: Send message (only if user wants to)
    if settings.ENABLE_WHATSAPP:
        send_test = input("Do you want to send a test WhatsApp message? (yes/no): ").strip().lower()
        if send_test in ['yes', 'y']:
            test_send_message()
        else:
            print("\n⏭️  Skipping message send test.\n")
    else:
        print("💡 To send actual test messages:")
        print("   1. Set ENABLE_WHATSAPP=true in .env")
        print("   2. Configure your Twilio credentials")
        print("   3. Run this test again\n")
    
    print("="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")
    
    print("📚 Next Steps:")
    print("   1. Review the TWILIO_SETUP_GUIDE.md for detailed setup")
    print("   2. Test with a customer from your dashboard")
    print("   3. Monitor messages in Twilio Console")
    print("\n✨ Happy messaging!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user.\n")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}\n")
        import traceback
        traceback.print_exc()

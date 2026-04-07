"""
Quick Twilio Diagnostic - Check if everything is ready
"""

from app.config import settings
from app.twilio_service import twilio_service

print("\n" + "="*60)
print("TWILIO WHATSAPP DIAGNOSTIC")
print("="*60)

print("\n1️⃣ Configuration Check:")
print(f"   ✓ WhatsApp Enabled: {settings.ENABLE_WHATSAPP}")
print(f"   ✓ Account SID: {settings.TWILIO_ACCOUNT_SID[:15]}...")
print(f"   ✓ From Number: {settings.TWILIO_WHATSAPP_FROM}")

print("\n2️⃣ Twilio Service Status:")
print(f"   ✓ Service Enabled: {twilio_service.enabled}")
print(f"   ✓ Client Initialized: {twilio_service.client is not None}")

if twilio_service.enabled and twilio_service.client:
    print("\n✅ TWILIO IS READY TO SEND MESSAGES!")
    print("\n3️⃣ Next Steps:")
    print("   1. Make sure YOU have joined the WhatsApp sandbox")
    print("      Send 'join <code>' to +1 415 523 8886")
    print("   2. Make sure your CUSTOMER has joined the sandbox")
    print("   3. Click the 🔔 Reminder button in your app")
    print("   4. Check this terminal for logs when you click")
    
    print("\n💡 To check if you've joined the sandbox:")
    print("   - Check your WhatsApp messages")
    print("   - Look for a message from Twilio Sandbox")
    print("   - It should say 'Sandbox: Joined...'")
    
else:
    print("\n❌ TWILIO IS NOT READY")
    if not settings.ENABLE_WHATSAPP:
        print("   ⚠️  ENABLE_WHATSAPP is set to false")
    else:
        print("   ⚠️  Twilio client failed to initialize")
        print("   Check the server logs for errors")

print("\n" + "="*60 + "\n")

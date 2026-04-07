"""
Generate a secure SECRET_KEY for production use
Run this before deploying to Render
"""
import secrets

# Generate a cryptographically secure random key
secret_key = secrets.token_urlsafe(32)

print("=" * 60)
print("🔐 Your SECRET_KEY for Render deployment:")
print("=" * 60)
print(f"\n{secret_key}\n")
print("=" * 60)
print("\n📋 Copy this key and add it to Render environment variables:")
print("   Variable name: SECRET_KEY")
print(f"   Value: {secret_key}")
print("\n⚠️  Keep this key secure! Don't share it publicly.")
print("=" * 60)

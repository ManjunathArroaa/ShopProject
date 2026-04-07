from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./payment_reminder.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Twilio Configuration for WhatsApp
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_FROM: Optional[str] = None  # e.g., "whatsapp:+14155238886"
    
    # Enable/Disable actual message sending
    ENABLE_WHATSAPP: bool = False
    
    # Business Info
    BUSINESS_NAME: str = "Vaishnavi Silks Kanapuraka"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

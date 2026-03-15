import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///calloutcome.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREFERRED_URL_SCHEME = "https"

    # Fix Supabase/Railway postgres:// vs postgresql:// issue
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    # Twilio (bootstrap credentials — per-account creds stored in DB)
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

    # Supabase Storage (for manual uploads)
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # Resend (transactional email)
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

    # Stripe
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
    STRIPE_PRICE_STARTER = os.environ.get("STRIPE_PRICE_STARTER")
    STRIPE_PRICE_PRO = os.environ.get("STRIPE_PRICE_PRO")
    STRIPE_PRICE_AGENCY = os.environ.get("STRIPE_PRICE_AGENCY")

    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    # Admin emails (auto-flagged as is_admin on signup)
    ADMIN_EMAILS = [
        e.strip().lower()
        for e in os.environ.get("ADMIN_EMAILS", "lovell.ryan22@gmail.com").split(",")
        if e.strip()
    ]

    # Max upload size: 200MB (supports ~100 call recordings)
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024

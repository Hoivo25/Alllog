from dotenv import load_dotenv
import os

load_dotenv()  # Reads .env file

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    LOCAL = os.getenv("LOCAL", "1")
    # Other configs
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")

    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///tele1.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Telegram bot token
    TELEGRAM_BOT_TOKEN = os.environ.get("7610790669:AAFv2FD305N7hhrPcwy7ORDxl_xx89oAXrs", "")
    
    # Shop configuration
    SHOP_NAME = os.environ.get("SHOP_NAME", "TripleLog Shop")
    
    # Webhook configuration
    WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "dev-webhook-secret-123")
    
    # Admin configuration (add your Telegram user ID here)
    ADMIN_TELEGRAM_IDS = [int(x) for x in os.environ.get("ADMIN_TELEGRAM_IDS", "").split(",") if x.strip()]
    
    # NowPayments configuration
    NOWPAYMENTS_API_KEY = os.environ.get("NOWPAYMENTS_API_KEY", "")
    NOWPAYMENTS_BASE_URL = os.environ.get("NOWPAYMENTS_BASE_URL", "https://api.nowpayments.io/v1")
    NOWPAYMENTS_IPN_SECRET = os.environ.get("NOWPAYMENTS_IPN_SECRET", "")
    
    # Admin password for web interface
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

import os
import logging
import threading
import asyncio
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")

if database_url:
    # Normalize URL for SQLAlchemy
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # ✅ Fallback to SQLite locally
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tele1.db"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# --- Telegram webhook setup ---
from config import Config

BOT_TOKEN = getattr(Config, "TELEGRAM_BOT_TOKEN", None)
APP_URL = getattr(Config, "APP_URL", None)  # must be set in config.py or env
WEBHOOK_URL = f"{APP_URL}/telegram-webhook" if APP_URL else None

def set_webhook():
    """Register webhook with Telegram"""
    if not BOT_TOKEN or not WEBHOOK_URL:
        logger.warning("BOT_TOKEN or APP_URL not configured, skipping webhook setup")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    
    if response.status_code == 200:
        logger.info(f"✅ Webhook set successfully: {response.json()}")
    else:
        logger.error(f"❌ Failed to set webhook: {response.text}")

@app.before_first_request
def init_webhook():
    set_webhook()

# Webhook route
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    logger.debug(f"📩 Update received: {update}")
    # TODO: forward update to dispatcher if needed
    return "ok", 200

# Optional manual reset route
@app.route("/reset-webhook")
def reset_webhook():
    set_webhook()
    return "Webhook reset triggered!", 200

# Bot startup flag to prevent multiple instances
bot_started = False

def start_telegram_bot():
    """Start the Telegram bot in a separate thread"""
    global bot_started
    if bot_started:
        return
    
    bot_started = True
    
    try:
        if not BOT_TOKEN:
            logger.warning("No Telegram bot token configured - bot will not start")
            return
            
        # Create new event loop for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        from working_bot import TelegramBot
        bot = TelegramBot()
        
        logger.info("Starting Telegram bot...")
        loop.run_until_complete(bot.run_bot())
    except Exception as e:
        logger.error(f"Telegram bot failed to start: {e}")
        import traceback
        traceback.print_exc()

# Import models and routes
from models import *
from simple_routes import *

with app.app_context():
    db.create_all()  # ✅ Creates tele1.db if fallback
    # Start the bot in a daemon thread
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    logger.info("Telegram bot thread started")

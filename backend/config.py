"""
Backend Configuration for AI-Assisted Telemedicine Kiosk.
Handles environment variables, SQLite/MySQL DB connections, and API secrets.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "telemedicine-secret-key-2026")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'telemedicine.db')}")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    STUN_SERVER = os.getenv("STUN_SERVER", "stun:stun.l.google.com:19302")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

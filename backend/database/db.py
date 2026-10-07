"""
Database session and connection engine for SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.config import Config
from backend.database.schema import Base

engine = create_engine(Config.DATABASE_URL, echo=False)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """Create all database tables using SQLAlchemy metadata."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Database session generator for dependency injection or context manager."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

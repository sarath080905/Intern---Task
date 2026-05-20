# ==============================
# Database configuration
# ==============================
# Load environment variables and configure SQLAlchemy engine.
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

def _normalize_database_url(url: str) -> str:
    # Render/Railway/Heroku often provide postgres:// — SQLAlchemy 2 needs postgresql://
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


# Use DATABASE_URL from environment or fall back to local SQLite.
DATABASE_URL = _normalize_database_url(
    os.getenv("DATABASE_URL", "sqlite:///./task_manager.db")
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a session factory used throughout the application.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models.
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Import models before calling so metadata is populated."""
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

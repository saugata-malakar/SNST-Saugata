"""
Database session setup for FastAPI.

Provides SQLAlchemy engine, session factory, and dependency for FastAPI endpoints.

Owner: Sahil Kumar Gupta (with Saugata for privacy model integration)
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

# Load DATABASE_URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://diabetescare:diabetescare@localhost:5432/diabetescare"
)

# SQLAlchemy engine
# Use NullPool in dev for easier teardown; use QueuePool in prod
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool if "sqlite" in DATABASE_URL else None,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",  # Debug logging
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    FastAPI dependency for database session injection.
    
    Usage in routers:
        @router.get("/patients/me")
        async def get_patient(db: Session = Depends(get_db)):
            patient = db.query(Patient).filter(...).first()
            return patient
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database: create all tables defined in models.Base.
    
    Call once on app startup or manually for dev setup.
    """
    from backend.database.models import Base
    
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all tables (dev only).
    WARNING: Irreversible. Use only in development.
    """
    from backend.database.models import Base
    
    Base.metadata.drop_all(bind=engine)

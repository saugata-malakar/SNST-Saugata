import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./diabetescare.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _migrate_sqlite_users_table():
    """Ensure existing SQLite `users` table has v4.0 columns and nullable email."""
    if "sqlite" not in DATABASE_URL:
        return
    with engine.begin() as conn:
        cols = conn.execute(text("PRAGMA table_info(users)")).fetchall()
        if not cols:
            return
        col_names = {row[1] for row in cols}
        email_notnull = any(row[1] == "email" and row[3] == 1 for row in cols)
        expected = {"phone", "full_name", "worker_type", "district", "username", "worker_id"}
        if email_notnull or not expected.issubset(col_names):
            # Rebuild users table cleanly preserving existing rows
            conn.execute(text("ALTER TABLE users RENAME TO _users_old"))
            Base.metadata.tables["users"].create(bind=conn)
            common = [c for c in ["user_id", "email", "phone", "username", "worker_id",
                                  "full_name", "hashed_password", "role", "worker_type",
                                  "district", "is_active", "created_at"] if c in col_names]
            cols_sql = ", ".join(common)
            conn.execute(text(f"INSERT INTO users ({cols_sql}) SELECT {cols_sql} FROM _users_old"))
            conn.execute(text("DROP TABLE _users_old"))


def create_tables():
    Base.metadata.create_all(bind=engine)
    _migrate_sqlite_users_table()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

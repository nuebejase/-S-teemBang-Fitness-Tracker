import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB = BASE_DIR / "steambang.db"
DATABASE_URL = os.getenv("STEAMBANG_DATABASE_URL", f"sqlite:///{DEFAULT_DB}")
UPLOADS_DIR = BASE_DIR / "uploads"
AVATARS_DIR = UPLOADS_DIR / "avatars"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def migrate_schema() -> None:
    """Lightweight SQLite migrations for dev databases."""
    if not DATABASE_URL.startswith("sqlite"):
        return
    AVATARS_DIR.mkdir(parents=True, exist_ok=True)
    with engine.connect() as conn:
        tables = {
            row[0]
            for row in conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).fetchall()
        }
        if "user_profiles" not in tables:
            return
        cols = {row[1] for row in conn.execute(text("PRAGMA table_info(user_profiles)")).fetchall()}
        if "avatar_url" not in cols:
            conn.execute(text("ALTER TABLE user_profiles ADD COLUMN avatar_url VARCHAR(512)"))
        if "daily_calorie_target" not in cols:
            conn.execute(text("ALTER TABLE user_profiles ADD COLUMN daily_calorie_target FLOAT DEFAULT 500"))
        if "daily_workout_target" not in cols:
            conn.execute(text("ALTER TABLE user_profiles ADD COLUMN daily_workout_target INTEGER DEFAULT 1"))
        conn.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

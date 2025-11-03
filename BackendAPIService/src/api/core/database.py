from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from src.api.core.config import get_settings

settings = get_settings()

# Create engine with pool_pre_ping for reliability
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy DB session and ensure it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

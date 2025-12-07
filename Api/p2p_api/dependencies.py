from typing import Generator
from functools import lru_cache
from fastapi import Request # Import Request
from sqlalchemy.orm import Session

from .config import Settings

@lru_cache()
def get_settings():
    return Settings()

def get_db(request: Request) -> Generator[Session, None, None]: # Add request: Request
    """
    FastAPI dependency to get a database session from the application state.
    """
    # Retrieve SessionLocal from app.state
    if not hasattr(request.app.state, 'SessionLocal') or request.app.state.SessionLocal is None:
        raise RuntimeError("Database session factory has not been initialized on app.state.")

    db = request.app.state.SessionLocal()
    try:
        yield db
    finally:
        db.close()

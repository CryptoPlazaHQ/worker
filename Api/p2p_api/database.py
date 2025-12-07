import datetime
import os

from sqlalchemy import (
    create_engine,
    event,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# --- IMPORTANT: Import Base and ALL Models from worker/models.py ---
# This makes worker/models.py the single source of truth for ORM models
from worker.models import (
    Base,
    DimCryptocurrencies,
    DimFiatCurrencies,
    DimPaymentMethods,
    DimAdvertisers,
    FactOffers,
    FactOfferPaymentMethods,
    User, # Now imported from worker/models
    APIKey, # Now imported from worker/models
    Run, # Now imported from worker/models
)


def init_db(database_url: str):
    """
    Initialize database engine and session factory for PostgreSQL.
    This function now returns a new engine and sessionmaker instance.
    """
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set.")

    # Always target PostgreSQL now, remove SQLite specifics
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
    )

    return engine, SessionLocal

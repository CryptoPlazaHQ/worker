import logging
import datetime
from typing import List, Optional, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, func
from uuid import UUID # Import UUID for batch_id

# Import ALL ORM models from the shared worker/models.py
from worker.models import (
    User, APIKey, Run,
    DimCryptocurrencies, DimFiatCurrencies, DimPaymentMethods, DimAdvertisers,
    FactOffers, FactOfferPaymentMethods # Import FactOfferPaymentMethods for joins
)

# Import new MCP-aligned schemas
from . import schemas

logger = logging.getLogger(__name__)

# --- Run CRUD (Adapted for API internal run tracking, no longer for scraping ingestion) ---
# Assuming Run model is now in worker/models.py
def create_run(db: Session, exchange: str) -> Run:
    """Creates a new run record."""
    run = Run(exchange=exchange)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def finalize_run(db: Session, run_id: int, total_offers: Optional[int] = None, error_message: Optional[str] = None) -> Optional[Run]:
    """Finalizes a run record with total offers or an error message."""
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        return None
    if total_offers is not None:
        run.total_offers = total_offers
    if error_message is not None:
        run.error_message = error_message
    db.commit()
    db.refresh(run)
    return run

# --- User CRUD (Retained) ---
# Assuming User model is now in worker/models.py
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieves a user by their username."""
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str) -> User:
    """Creates a new user in the database."""
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- API Key CRUD (Retained) ---
# Assuming APIKey model is now in worker/models.py
def get_api_key_by_prefix(db: Session, prefix: str) -> Optional[APIKey]:
    """Retrieves an API key by its prefix."""
    return db.query(APIKey).filter(APIKey.prefix == prefix).first()

def get_user_api_keys(db: Session, user_id: int) -> List[APIKey]:
    """Retrieves all API keys for a given user ID."""
    return db.query(APIKey).filter(APIKey.user_id == user_id).all()

def create_api_key(
    db: Session, key: schemas.APIKeyCreate, user_id: int, prefix: str, hashed_key: str
) -> APIKey:
    """Creates and stores an API key record in the database."""
    db_key = APIKey(
        prefix=prefix,
        hashed_key=hashed_key,
        name=key.name,
        user_id=user_id,
    )
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key

def deactivate_api_key(db: Session, prefix: str, user_id: int) -> Optional[APIKey]:
    """Deactivates an API key for a specific user."""
    db_key = (
        db.query(APIKey)
        .filter(APIKey.prefix == prefix, APIKey.user_id == user_id)
        .first()
    )
    if db_key:
        db_key.is_active = False
        db.commit()
        db.refresh(db_key)
    return db_key

# --- New Read-Only CRUD for Dimensional Models ---

def get_cryptocurrencies(db: Session, skip: int = 0, limit: int = 100) -> List[DimCryptocurrencies]:
    """Retrieves a list of cryptocurrencies."""
    return db.query(DimCryptocurrencies).offset(skip).limit(limit).all()

def get_fiat_currencies(db: Session, skip: int = 0, limit: int = 100) -> List[DimFiatCurrencies]:
    """Retrieves a list of fiat currencies."""
    return db.query(DimFiatCurrencies).offset(skip).limit(limit).all()

def get_payment_methods(db: Session, skip: int = 0, limit: int = 100) -> List[DimPaymentMethods]:
    """Retrieves a list of payment methods."""
    return db.query(DimPaymentMethods).offset(skip).limit(limit).all()

def get_advertisers(db: Session, skip: int = 0, limit: int = 100) -> List[DimAdvertisers]:
    """Retrieves a list of current advertisers."""
    # Assuming 'is_current=True' is the way to get current advertisers in SCD Type 2
    return db.query(DimAdvertisers).filter(DimAdvertisers.is_current == True).offset(skip).limit(limit).all()

def get_advertiser_by_id(db: Session, advertiser_id: str) -> Optional[DimAdvertisers]:
    """Retrieves a current advertiser by their external ID."""
    return db.query(DimAdvertisers).filter(
        DimAdvertisers.advertiser_id == advertiser_id,
        DimAdvertisers.is_current == True
    ).first()

def get_offers(
    db: Session,
    fiat_code: Optional[str] = None,
    crypto_symbol: Optional[str] = None,
    trade_type: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    advertiser_id: Optional[str] = None,
    payment_method_code: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "extraction_timestamp",
    sort_order: str = "desc"
) -> List[FactOffers]:
    """Retrieves a paginated and filterable list of rich offers."""
    query = db.query(FactOffers).options(
        joinedload(FactOffers.cryptocurrency),
        joinedload(FactOffers.fiat_currency),
        joinedload(FactOffers.advertiser),
        # joinedload(FactOffers.payment_methods) # This join is more complex due to FactOfferPaymentMethods
    )

    if fiat_code:
        query = query.join(FactOffers.fiat_currency).filter(DimFiatCurrencies.currency_code == fiat_code)
    if crypto_symbol:
        query = query.join(FactOffers.cryptocurrency).filter(DimCryptocurrencies.symbol == crypto_symbol)
    if trade_type:
        query = query.filter(FactOffers.trade_type == trade_type)
    if min_price is not None:
        query = query.filter(FactOffers.price >= min_price)
    if max_price is not None:
        query = query.filter(FactOffers.price <= max_price)
    if advertiser_id:
        query = query.join(FactOffers.advertiser).filter(DimAdvertisers.advertiser_id == advertiser_id)
    
    # Filtering by payment method requires a join through FactOfferPaymentMethods
    if payment_method_code:
        query = query.join(FactOfferPaymentMethods, FactOffers.offer_id == FactOfferPaymentMethods.offer_id).join(
            DimPaymentMethods, FactOfferPaymentMethods.payment_method_id == DimPaymentMethods.payment_method_id
        ).filter(DimPaymentMethods.method_code == payment_method_code)
        
    # Apply sorting
    if sort_by:
        sort_column = getattr(FactOffers, sort_by, None)
        if sort_column:
            if sort_order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        # Handle sorting by joined columns later if needed

    return query.offset(skip).limit(limit).all()

def get_offer_by_external_id(db: Session, offer_external_id: str) -> Optional[FactOffers]:
    """Retrieves a single offer by its external Binance ID."""
    return db.query(FactOffers).options(
        joinedload(FactOffers.cryptocurrency),
        joinedload(FactOffers.fiat_currency),
        joinedload(FactOffers.advertiser),
        # joinedload(FactOffers.payment_methods)
    ).filter(FactOffers.offer_external_id == offer_external_id).first()

# Helper to get payment methods for an offer
def get_payment_methods_for_offer(db: Session, offer_id: int, extraction_timestamp: datetime.datetime) -> List[DimPaymentMethods]:
    return db.query(DimPaymentMethods).join(
        FactOfferPaymentMethods, DimPaymentMethods.payment_method_id == FactOfferPaymentMethods.payment_method_id
    ).filter(
        FactOfferPaymentMethods.offer_id == offer_id,
        FactOfferPaymentMethods.extraction_timestamp == extraction_timestamp
    ).all()
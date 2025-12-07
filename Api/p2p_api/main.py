import logging
import uuid
from contextlib import asynccontextmanager
from typing import List, Literal, Dict, Optional
from decimal import Decimal # Import Decimal for price filters

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, HTTPBearer # Import HTTPBearer
from sqlalchemy.orm import Session

from . import (
    crud,
    database as models, # models now refers to worker.models
    schemas,
    # services, # services.py (process_binance_offers) will be removed or repurposed
)
# --- REMOVE SCRAPER IMPORTS ---
# from .binance_scraper import get_binance_offers, get_binance_pairs
from .config import Settings
from .database import Base, init_db # Base is now from worker.models
# from .exceptions import ScraperError # ScraperError will be removed or repurposed
from .logging_config import setup_logging
from .dependencies import get_db, set_session_local
from .auth import pwd_context

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key")
bearer_scheme = HTTPBearer() # Define the HTTPBearer scheme

_engine = None
_SessionLocal = None

def configure_database(db_url: str, engine_override=None, session_override=None):
    global _engine, _SessionLocal
    if engine_override and session_override:
        _engine = engine_override
        _SessionLocal = session_override
    else:
        _engine, _SessionLocal = init_db(db_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _engine, _SessionLocal, global_settings
    setup_logging()
    logger.info("Starting P2P Dashboard API...")
    global_settings = Settings() # Settings from Api/p2p_api/config.py
    if not global_settings.testing:
        configure_database(global_settings.database_url)
        set_session_local(_SessionLocal)
        # --- Base.metadata.create_all (removed for API, as worker manages schema) ---
        # The worker is responsible for creating/managing the database schema.
        # This API is read-only from that database. If API specific tables (users/api_keys/runs)
        # are needed, they should be managed via alembic migrations for this API project.
        # For now, we assume Base.metadata.create_all is not needed here if worker manages everything.
        # If API-specific tables (users, api_keys, runs) are part of the worker's Base,
        # then create_all might implicitly create them if they don't exist.
        # However, the worker is meant to initialize the DB. The API should just connect.
        # If the API needs its own migrations for User/APIKey/Run, that's a separate task.
        # For now, remove this line.
        # Base.metadata.create_all(bind=_engine)
        
        # Include the admin router
        from .routers import admin
        app.include_router(admin.router)
    yield

    logger.info("Shutting down P2P Dashboard API...")
    if not global_settings.testing and _engine:
        _engine.dispose()

tags_metadata = [
    {
        "name": "Offers",
        "description": "Endpoints for querying P2P offers data from the dimensional database.",
    },
    {
        "name": "Advertisers",
        "description": "Endpoints for querying P2P advertiser data from the dimensional database.",
    },
    {
        "name": "Dimensions",
        "description": "Endpoints for querying P2P dimension data (cryptocurrencies, fiat currencies, payment methods).",
    },
    {
        "name": "System",
        "description": "System health and status endpoints.",
    },
    {
        "name": "Admin",
        "description": "Endpoints for user and API key management.",
    },
]

app = FastAPI(
    title="P2P Dashboard Data API", # Renamed to reflect data focus
    description="A unified, high-performance API for querying P2P cryptocurrency trading data from the worker-populated dimensional database.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    contact={
        "name": "P2P Dashboard Support",
        "url": "https://api.bolivarparalelo.org",
        "email": "info@api.bolivarparalelo.org",
    },
    license_info={"name": "Usage License"},
    openapi_extra={
        "components": {
            "securitySchemes": {
                "Bearer Auth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                },
                "X-API-Key": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            }
        },
        "security": [
            {"Bearer Auth": []},
            {"X-API-Key": []}
        ]
    }
)




async def get_api_key(
    api_key: str = Depends(api_key_header), db: Session = Depends(get_db)
):
    """Dependency to validate API Key. Key format should be 'prefix_secret'."""
    if "_" not in api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key format"
        )

    prefix, _, secret = api_key.rpartition("_")
    db_key = crud.get_api_key_by_prefix(db, prefix=prefix)

    if not db_key or not db_key.is_active or not pwd_context.verify(secret, db_key.hashed_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key"
        )
    return db_key

@app.get("/", tags=["System"])
async def read_root():
    return {"message": "P2P Dashboard Data API is running!"}

# --- NEW OFFERS ENDPOINTS ---
@app.get(
    "/api/v1/offers",
    response_model=List[schemas.Offer],
    dependencies=[Depends(get_api_key)],
    summary="Retrieve P2P Offers",
    description="Retrieves a paginated and filterable list of P2P offers from the dimensional database.",
    tags=["Offers"],
)
async def get_offers_endpoint(
    fiat_code: Optional[str] = Query(None, description="Filter by fiat currency code (e.g., ARS)."),
    crypto_symbol: Optional[str] = Query(None, description="Filter by cryptocurrency symbol (e.g., USDT)."),
    trade_type: Optional[Literal["BUY", "SELL"]] = Query(None, description="Filter by trade type (BUY or SELL)."),
    min_price: Optional[Decimal] = Query(None, description="Filter offers with price greater than or equal to this value."),
    max_price: Optional[Decimal] = Query(None, description="Filter offers with price less than or equal to this value."),
    advertiser_id: Optional[str] = Query(None, description="Filter by external Binance advertiser ID."),
    payment_method_code: Optional[str] = Query(None, description="Filter by payment method code (e.g., Mercadopago)."),
    page: int = Query(1, ge=1, description="Page number for pagination, starting from 1."),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page (1-1000)."),
    sort_by: str = Query("extraction_timestamp", description="Field to sort by (e.g., price, extraction_timestamp)."),
    sort_order: Literal["asc", "desc"] = Query("desc", description="Sort order (asc or desc)."),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    offers_data = crud.get_offers(
        db,
        fiat_code=fiat_code,
        crypto_symbol=crypto_symbol,
        trade_type=trade_type,
        min_price=min_price,
        max_price=max_price,
        advertiser_id=advertiser_id,
        payment_method_code=payment_method_code,
        skip=skip,
        limit=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    # The CRUD function returns ORM models directly, FastAPI will convert to Pydantic schemas
    return offers_data

@app.get(
    "/api/v1/offers/{offer_external_id}",
    response_model=schemas.Offer,
    dependencies=[Depends(get_api_key)],
    summary="Retrieve a single P2P Offer by External ID",
    description="Retrieves a specific P2P offer by its external Binance ID from the dimensional database.",
    tags=["Offers"],
)
async def get_offer_by_id_endpoint(
    offer_external_id: str,
    db: Session = Depends(get_db),
):
    db_offer = crud.get_offer_by_external_id(db, offer_external_id=offer_external_id)
    if not db_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    return db_offer


# --- NEW ADVERTISERS ENDPOINTS ---
@app.get(
    "/api/v1/advertisers",
    response_model=List[schemas.Advertiser],
    dependencies=[Depends(get_api_key)],
    summary="Retrieve P2P Advertisers",
    description="Retrieves a paginated and filterable list of current P2P advertisers from the dimensional database.",
    tags=["Advertisers"],
)
async def get_advertisers_endpoint(
    nickname: Optional[str] = Query(None, description="Filter by advertiser nickname (partial match)."),
    is_merchant: Optional[bool] = Query(None, description="Filter by merchant status."),
    page: int = Query(1, ge=1, description="Page number for pagination, starting from 1."),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page (1-1000)."),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    advertisers_data = crud.get_advertisers(
        db,
        # nickname=nickname, # CRUD needs to implement nickname filtering
        # is_merchant=is_merchant, # CRUD needs to implement is_merchant filtering
        skip=skip,
        limit=page_size
    )
    return advertisers_data

@app.get(
    "/api/v1/advertisers/{advertiser_id}",
    response_model=schemas.Advertiser,
    dependencies=[Depends(get_api_key)],
    summary="Retrieve a single P2P Advertiser by External ID",
    description="Retrieves a specific current P2P advertiser by their external Binance ID from the dimensional database.",
    tags=["Advertisers"],
)
async def get_advertiser_by_id_endpoint(
    advertiser_id: str,
    db: Session = Depends(get_db),
):
    db_advertiser = crud.get_advertiser_by_id(db, advertiser_id=advertiser_id)
    if not db_advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    return db_advertiser

# --- NEW DIMENSION ENDPOINTS ---
@app.get(
    "/api/v1/cryptocurrencies",
    response_model=List[schemas.Cryptocurrency],
    dependencies=[Depends(get_api_key)],
    summary="Retrieve Cryptocurrencies",
    description="Retrieves a list of supported cryptocurrencies.",
    tags=["Dimensions"],
)
async def get_cryptocurrencies_endpoint(
    page: int = Query(1, ge=1, description="Page number for pagination, starting from 1."),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page (1-1000)."),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    cryptos_data = crud.get_cryptocurrencies(db, skip=skip, limit=page_size)
    return cryptos_data

@app.get(
    "/api/v1/fiat_currencies",
    response_model=List[schemas.FiatCurrency],
    dependencies=[Depends(get_api_key)],
    summary="Retrieve Fiat Currencies",
    description="Retrieves a list of supported fiat currencies.",
    tags=["Dimensions"],
)
async def get_fiat_currencies_endpoint(
    page: int = Query(1, ge=1, description="Page number for pagination, starting from 1."),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page (1-1000)."),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    fiats_data = crud.get_fiat_currencies(db, skip=skip, limit=page_size)
    return fiats_data

@app.get(
    "/api/v1/payment_methods",
    response_model=List[schemas.PaymentMethod],
    dependencies=[Depends(get_api_key)],
    summary="Retrieve Payment Methods",
    description="Retrieves a list of supported payment methods.",
    tags=["Dimensions"],
)
async def get_payment_methods_endpoint(
    page: int = Query(1, ge=1, description="Page number for pagination, starting from 1."),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page (1-1000)."),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    payment_methods_data = crud.get_payment_methods(db, skip=skip, limit=page_size)
    return payment_methods_data

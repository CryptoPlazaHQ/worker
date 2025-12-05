import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

# --- MCP-aligned Dimensional Models ---

class Cryptocurrency(BaseModel):
    # Maps to DimCryptocurrencies
    crypto_id: int
    symbol: str
    name: str
    binance_asset_code: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class FiatCurrency(BaseModel):
    # Maps to DimFiatCurrencies
    fiat_id: int
    currency_code: str
    currency_name: str
    country_code: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class PaymentMethod(BaseModel):
    # Maps to DimPaymentMethods
    payment_method_id: int
    method_code: str
    method_name: str
    category: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Advertiser(BaseModel):
    # Maps to DimAdvertisers (current record)
    advertiser_sk: int # Surrogate Key
    advertiser_id: str # Natural Key from Binance
    nickname: str
    is_merchant: Optional[bool] = False
    registration_days: Optional[int] = None
    # effective_date: datetime.datetime # Not exposing internal SCD fields directly unless needed
    # is_current: bool # Assumed to be True for this view

    model_config = ConfigDict(from_attributes=True)


class Offer(BaseModel):
    # Maps to FactOffers with joined dimensions
    offer_id: int # Primary Key of the snapshot
    offer_external_id: str # Binance's advNo
    batch_id: str # UUID will be string
    extraction_timestamp: datetime.datetime
    trade_type: str # "BUY" or "SELL"
    price: Decimal
    available_amount: Decimal
    min_limit: Decimal
    max_limit: Decimal
    tradable_quantity: Optional[Decimal] = None
    completion_rate: Optional[Decimal] = None
    total_orders_count: Optional[int] = None
    avg_response_time_seconds: Optional[int] = None
    avg_completion_time_minutes: Optional[int] = None
    terms_conditions: Optional[str] = None
    is_available: bool

    # Nested dimensional models
    cryptocurrency: Cryptocurrency
    fiat_currency: FiatCurrency
    advertiser: Advertiser
    # Note: payment_methods will be fetched via a separate join or relationship in CRUD

    model_config = ConfigDict(from_attributes=True)


# --- API Management Schemas (Retained and Adapted) ---

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    api_keys: List["APIKey"] = [] # Forward reference

    model_config = ConfigDict(from_attributes=True)


# API Key schemas
class APIKeyBase(BaseModel):
    name: str

class APIKeyCreate(APIKeyBase):
    pass

class APIKey(APIKeyBase):
    id: int # Add ID for clarity, as it's a primary key in DB
    prefix: str
    is_active: bool
    # user_id: int # Exclude user_id from direct exposure
    # hashed_key: str # Exclude hashed_key from direct exposure

    model_config = ConfigDict(from_attributes=True)

class APIKeyCreateResponse(BaseModel):
    name: str
    key: str # This key is the *full* generated key (prefix_secret)

# Run schemas (Adapted for tracking worker runs/API events)
class RunBase(BaseModel):
    # Assuming this maps to the consolidated Run model in worker/models.py
    exchange: str
    fetched_at: Optional[datetime.datetime] = None
    total_offers: Optional[int] = None
    error_message: Optional[str] = None

class RunCreate(RunBase):
    pass

class Run(RunBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Token schemas (If JWT/OAuth is planned later, keep for reference)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
import pandas as pd
from decimal import Decimal
from typing import Tuple, List, Dict

def calculate_vwap(offers: pd.DataFrame) -> Decimal:
    """Calculate Volume-Weighted Average Price."""
    if offers.empty:
        return Decimal('0')
    
    # Ensure columns are numeric, converting non-numeric to NaN and then to 0
    offers['price'] = pd.to_numeric(offers['price'], errors='coerce').fillna(0)
    offers['available_amount'] = pd.to_numeric(offers['available_amount'], errors='coerce').fillna(0)
    
    total_volume = offers['available_amount'].sum()
    if total_volume == 0:
        return Decimal('0')
    
    weighted_sum = (offers['price'] * offers['available_amount']).sum()
    return Decimal(str(weighted_sum / total_volume))

def calculate_spread(buy_vwap: Decimal, sell_vwap: Decimal) -> Decimal:
    """Calculate spread percentage between buy and sell sides."""
    if buy_vwap == 0 or sell_vwap == 0:
        return Decimal('0')
    
    spread = ((sell_vwap - buy_vwap) / buy_vwap) * 100
    return Decimal(str(spread))

def prepare_order_book_data(
    offers: List[Dict], 
    trade_type: str
) -> pd.DataFrame:
    """Transform raw offers into structured DataFrame."""
    if not offers:
        return pd.DataFrame()
        
    df = pd.DataFrame(offers)
    
    # Extract nested data
    if 'cryptocurrency' in df.columns and not df['cryptocurrency'].isnull().all():
        df['crypto_symbol'] = df['cryptocurrency'].apply(lambda x: x['symbol'] if isinstance(x, dict) else None)
    if 'fiat_currency' in df.columns and not df['fiat_currency'].isnull().all():
        df['fiat_code'] = df['fiat_currency'].apply(lambda x: x['currency_code'] if isinstance(x, dict) else None)
    if 'advertiser' in df.columns and not df['advertiser'].isnull().all():
        df['advertiser_name'] = df['advertiser'].apply(lambda x: x['nickname'] if isinstance(x, dict) else None)
    
    # Filter by trade type
    df = df[df['trade_type'] == trade_type]
    
    # Convert price to Decimal for accurate sorting
    df['price'] = df['price'].apply(Decimal)
    
    # Sort: Buy orders descending, Sell orders ascending
    ascending = (trade_type == 'SELL')
    df = df.sort_values('price', ascending=ascending)
    
    return df

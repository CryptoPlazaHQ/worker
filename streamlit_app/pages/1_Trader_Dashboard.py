import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decimal import Decimal
import logging

# Adjust the import path based on your project structure
from utils.api import P2PAPIClient
from utils.calculations import (
    calculate_vwap, 
    calculate_spread,
    prepare_order_book_data
)

# Set up logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(page_title="Trader's Dashboard", layout="wide")

st.title("📊 Live Order Book Dashboard")
st.markdown("""
    This dashboard provides a real-time view of the P2P market for a selected trading pair,
    calculating key metrics like Volume-Weighted Average Price (VWAP) to give a clear sense of the market's center.
    """)

# --- API Key and Client Initialization ---
if 'api_key' not in st.session_state or not st.session_state['api_key']:
    st.warning("Please enter your API Key on the main page sidebar to use this tool.")
    st.stop()

try:
    client = P2PAPIClient(api_key=st.session_state['api_key'])
except ValueError as e:
    st.error(e)
    st.stop()

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔍 Filters")
    
    # Fetch available pairs for dropdowns
    with st.spinner("Loading filter options..."):
        fiats = client.get_fiat_currencies()
        cryptos = client.get_cryptocurrencies()

    # Default to ARS and USDT if available
    fiat_options = [f['currency_code'] for f in fiats]
    crypto_options = [c['symbol'] for c in cryptos]
    
    default_fiat_index = fiat_options.index("ARS") if "ARS" in fiat_options else 0
    default_crypto_index = crypto_options.index("USDT") if "USDT" in crypto_options else 0
    
    selected_fiat = st.selectbox(
        "Fiat Currency",
        options=fiat_options,
        index=default_fiat_index
    )
    
    selected_crypto = st.selectbox(
        "Cryptocurrency",
        options=crypto_options,
        index=default_crypto_index
    )
    
    # Advanced filters
    with st.expander("⚙️ Advanced Filters"):
        payment_methods = client.get_payment_methods()
        pm_options = [pm['method_code'] for pm in payment_methods]
        selected_methods = st.multiselect(
            "Payment Methods",
            options=pm_options,
            help="Filter offers by specific payment methods."
        )
        
        min_price = st.number_input("Min Price", min_value=0.0, value=0.0, format="%.2f")
        max_price = st.number_input("Max Price", min_value=0.0, value=0.0, format="%.2f")

# --- Data Fetching ---
with st.spinner(f"Loading order book for {selected_crypto}/{selected_fiat}..."):
    # Build filter dictionary
    filters = {
        "fiat_code": selected_fiat,
        "crypto_symbol": selected_crypto,
        "payment_methods": selected_methods if selected_methods else None,
        "min_price": min_price if min_price > 0 else None,
        "max_price": max_price if max_price > 0 else None
    }
    
    logger.info(f"Fetching BUY offers with filters: {filters}")
    buy_offers = client.get_offers(trade_type="BUY", **filters)
    logger.info(f"Received {len(buy_offers)} BUY offers.")
    
    logger.info(f"Fetching SELL offers with filters: {filters}")
    sell_offers = client.get_offers(trade_type="SELL", **filters)
    logger.info(f"Received {len(sell_offers)} SELL offers.")

# --- Data Processing and Metrics Calculation ---
buy_df = prepare_order_book_data(buy_offers, "BUY")
sell_df = prepare_order_book_data(sell_offers, "SELL")

buy_vwap = calculate_vwap(buy_df)
sell_vwap = calculate_vwap(sell_df)
spread = calculate_spread(buy_vwap, sell_vwap)
total_buy_volume = buy_df['available_amount'].sum() if not buy_df.empty else 0
total_sell_volume = sell_df['available_amount'].sum() if not sell_df.empty else 0

# --- Metrics Display ---
st.header("Market Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Buy VWAP", f"{buy_vwap:.2f} {selected_fiat}")
col2.metric("Sell VWAP", f"{sell_vwap:.2f} {selected_fiat}")
col3.metric("Spread", f"{spread:.2f}%")
col4.metric("Total Buy Volume", f"{total_buy_volume:.2f} {selected_crypto}")


# --- Order Book Display ---
st.header("Live Order Book")
col_buy, col_sell = st.columns(2)

with col_buy:
    st.subheader("🟢 Buy Orders")
    if not buy_df.empty:
        st.dataframe(
            buy_df[['price', 'available_amount', 'min_limit', 'max_limit', 'advertiser_name']],
            width='stretch',
            height=400,
            column_config={
                "price": st.column_config.NumberColumn(format="%.2f"),
                "available_amount": st.column_config.NumberColumn(format="%.2f"),
            }
        )
    else:
        st.info(f"No buy offers found for {selected_crypto}/{selected_fiat}.")

with col_sell:
    st.subheader("🔴 Sell Orders")
    if not sell_df.empty:
        st.dataframe(
            sell_df[['price', 'available_amount', 'min_limit', 'max_limit', 'advertiser_name']],
            width='stretch',
            height=400,
            column_config={
                "price": st.column_config.NumberColumn(format="%.2f"),
                "available_amount": st.column_config.NumberColumn(format="%.2f"),
            }
        )
    else:
        st.info(f"No sell offers found for {selected_crypto}/{selected_fiat}.")

# --- Market Depth Chart ---
st.header("📈 Market Depth")

if buy_df.empty and sell_df.empty:
    st.info("No data available to display market depth chart.")
else:
    # Calculate cumulative volume
    buy_df_sorted = buy_df.sort_values('price', ascending=False)
    buy_df_sorted['cumulative_volume'] = buy_df_sorted['available_amount'].cumsum()

    sell_df_sorted = sell_df.sort_values('price', ascending=True)
    sell_df_sorted['cumulative_volume'] = sell_df_sorted['available_amount'].cumsum()

    # Create Plotly figure
    fig = go.Figure()

    # Add buy side (bids)
    fig.add_trace(go.Scatter(
        x=buy_df_sorted['price'],
        y=buy_df_sorted['cumulative_volume'],
        mode='lines',
        fill='tozeroy',
        name='Buy Depth (Bids)',
        line=dict(color='#26A69A', width=2),
        hovertemplate='Price: %{x:.2f}<br>Volume: %{y:.2f}<extra></extra>'
    ))

    # Add sell side (asks)
    fig.add_trace(go.Scatter(
        x=sell_df_sorted['price'],
        y=sell_df_sorted['cumulative_volume'],
        mode='lines',
        fill='tozeroy',
        name='Sell Depth (Asks)',
        line=dict(color='#EF5350', width=2),
        hovertemplate='Price: %{x:.2f}<br>Volume: %{y:.2f}<extra></extra>'
    ))

    # Update layout for a financial chart look
    fig.update_layout(
        title=f'Market Depth for {selected_crypto}/{selected_fiat}',
        xaxis_title='Price',
        yaxis_title='Cumulative Volume',
        template='plotly_dark',
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(x=0.01, y=0.99),
    )
    
    st.plotly_chart(fig, width='stretch')

import streamlit as st
import pandas as pd
from streamlit_app.utils.api import P2PAPIClient # Import the API client

st.set_page_config(page_title="Trader's Dashboard", layout="wide")

st.title("📈 Trader's Order Book Dashboard")

st.markdown("""
This dashboard provides a real-time view of the P2P market for a selected trading pair,
calculating the Volume-Weighted Average Price (VWAP) to give a clear sense of the market's center.
""")

if 'api_key' not in st.session_state or not st.session_state['api_key']:
    st.warning("Please enter your API Key in the main page sidebar to use this tool.")
    st.stop()

# Instantiate the API client with the API key from session state
api_key = st.session_state['api_key']
client = P2PAPIClient(api_key=api_key)

# Placeholder for dashboard implementation
st.info("Dashboard implementation is pending. Below is a demonstration of API interaction.")

# Example of how the UI could look
st.subheader("Select Trading Pair")
col1, col2 = st.columns(2)
with col1:
    fiat = st.selectbox("Select Fiat Currency", ["ARS", "USD", "EUR"], index=0) # Default to ARS
with col2:
    crypto = st.selectbox("Select Crypto", ["USDT", "BTC", "ETH"], index=0) # Default to USDT

if st.button("Fetch Market Data"):
    st.success(f"Fetching data for {crypto}/{fiat}...")
    with st.spinner("Loading data..."):
        try:
            # Make an actual API call
            offers_data = client.get_offers(fiat=fiat, crypto=crypto, trade_type="BUY")
            st.success("Successfully fetched data from the API!")
            
            if offers_data:
                st.subheader(f"Latest Buy Offers for {crypto}/{fiat}")
                # Convert to DataFrame for better display if needed, or display raw JSON
                st.json(offers_data[:5]) # Display first 5 offers
            else:
                st.info("No offers found for the selected criteria.")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.warning("Please ensure your API server is running and the API key is valid.")

    # Example of metrics display (placeholders for now)
    st.header("Market Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Buy VWAP", "1,005.50 ARS", "2.5%")
    col2.metric("Sell VWAP", "1,010.00 ARS", "-1.2%")
    col3.metric("Spread", "0.45%", "0.1%")

    # Example of dataframe display (placeholders for now)
    st.subheader("Buy Orders (Placeholder)")
    buy_data = {'Price': [1005.00, 1004.90, 1004.80], 'Available': [500, 1200, 300], 'Min Limit': [10000, 50000, 20000]}
    st.dataframe(pd.DataFrame(buy_data), use_container_width=True)

    st.subheader("Sell Orders (Placeholder)")
    sell_data = {'Price': [1010.00, 1010.10, 1010.20], 'Available': [800, 1500, 200], 'Min Limit': [10000, 25000, 15000]}
    st.dataframe(pd.DataFrame(sell_data), use_container_width=True)



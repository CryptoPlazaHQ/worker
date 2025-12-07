import streamlit as st

st.set_page_config(page_title="API Explorer", layout="wide")

st.title("🔬 Interactive API Explorer")

st.markdown("""
This tool allows you to interactively build and execute queries against the P2P API.
Select an endpoint, fill in the parameters, and see the live request and response.
""")

if 'api_key' not in st.session_state or not st.session_state['api_key']:
    st.warning("Please enter your API Key in the main page sidebar to use this tool.")
    st.stop()

# Placeholder for API Explorer implementation
st.info("API Explorer implementation is pending.")

# Example of how the UI could look
endpoint = st.selectbox("Select API Endpoint", ["/api/v1/offers", "/api/v1/advertisers", "/api/v1/cryptocurrencies"])

if endpoint == "/api/v1/offers":
    st.subheader("Parameters for `/api/v1/offers`")
    col1, col2 = st.columns(2)
    with col1:
        fiat = st.text_input("fiat_code")
        trade_type = st.selectbox("trade_type", ["BUY", "SELL"])
    with col2:
        crypto = st.text_input("crypto_symbol")
        page_size = st.number_input("page_size", 1, 1000, 100)

    if st.button("Execute Query"):
        st.success("Executing query...")
        # Here we would call the API and display the request/response.
        # This will be implemented in the next phase.

        # Example of request/response display
        st.subheader("Request")
        st.code(f"""
import requests

headers = {{
    "X-API-Key": "{st.session_state['api_key'][:5]}..."
}}
params = {{
    "fiat_code": "{fiat}",
    "crypto_symbol": "{crypto}",
    "trade_type": "{trade_type}",
    "page_size": {page_size}
}}
response = requests.get("http://127.0.0.1:8000/api/v1/offers", headers=headers, params=params)
print(response.json())
        """, language="python")

        st.subheader("Response")
        st.json({
            "status": "example",
            "data": [
                {"price": 1005.00, "available_amount": 500},
                {"price": 1004.90, "available_amount": 1200}
            ]
        })

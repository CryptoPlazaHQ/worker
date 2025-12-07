import streamlit as st

st.set_page_config(
    page_title="P2P API Handbook",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("P2P API Live Handbook & Trader's Dashboard")

st.markdown("""
Welcome to the interactive handbook for the P2P Dashboard API.

This application serves as a live demonstration, testing ground, and educational tool for the API.

**Use the sidebar to navigate between the different sections:**

- **Trader's Dashboard**: A live order book dashboard showcasing the API's potential for financial analysis.
- **API Explorer**: An interactive tool to build and test API queries.

### 🔑 API Key

Please enter your API key in the sidebar to begin.
""")

# Sidebar for API key input
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter your API Key", type="password")

if api_key:
    st.session_state['api_key'] = api_key
    st.sidebar.success("API Key saved for this session.")
else:
    st.sidebar.warning("API Key is required to use the tools.")


# 📄 PRD: P2P API Live Handbook & Trader's Dashboard

## 1. Vision & Overview

This document outlines the Product Requirements for a Streamlit application that serves a dual purpose:

1.  **A Live API Handbook**: An interactive, educational, and beautiful interface for developers and stakeholders to understand, test, and integrate with the P2P Dashboard API.
2.  **A Trader's Dashboard**: A functional MVP that showcases the analytical power of the API's enriched data through a professional, trader-focused "Order Book" dashboard.

The application will be designed with a "show, don't just tell" philosophy. Every feature will not only provide value but also educate the user on how to achieve the same result independently using the API.

---

## 2. Target Audience

| Persona | Role | Primary Goal |
| :--- | :--- | :--- |
| 👩‍💻 **Developer** | Integrator | Quickly understand API endpoints, test requests/responses, and copy-paste functional Python code to accelerate their own development. |
| 📈 **Trader** | End-User | Gain immediate market insights, understand P2P market depth, and identify opportunities through clean, actionable data visualizations. |
| 👔 **Stakeholder** | Evaluator | Clearly perceive the commercial value, technical maturity, and future potential of the P2P data platform in a polished, interactive demo. |
| 🎓 **Student/Newcomer**| Learner | Visually grasp complex P2P market concepts through an intuitive, hands-on tool. |

---

## 3. Core Features & Use Cases

### Feature 1: Secure API Connection
- **User Story**: As any user, I want to securely enter my API key once so that I can access all the application's features for my entire session.
- **Implementation**: A password-style text input in the sidebar (`st.text_input(type="password")`) that stores the key in `st.session_state`.

### Feature 2: Trader's Dashboard (MVP Use Case)
- **User Story**: As a trader, I want to select a trading pair (e.g., USDT/ARS) and instantly see a summary of the order book so that I can gauge the current market sentiment.
- **Implementation**:
    - UI selectors for `fiat` and `crypto`.
    - Fetches data from the `/api/v1/offers` endpoint.
    - Calculates and displays key metrics:
        - **Buy-Side VWAP (Volume-Weighted Average Price)**
        - **Sell-Side VWAP**
        - **Total Buy/Sell Volume**
        - **Live Spread (%)**
    - Uses `st.metric` for high-impact display of these numbers.
    - Shows the raw, sorted offers in an `st.dataframe`.

### Feature 3: Interactive API Explorer
- **User Story**: As a developer, I want to visually build an API query for any endpoint, execute it, and see both the JSON response and the Python code needed to make that exact call.
- **Implementation**:
    - A dropdown to select an API endpoint (e.g., `/offers`, `/advertisers`).
    - Dynamically generated `st.text_input`, `st.slider`, etc., for the endpoint's parameters.
    - An "Execute" button that triggers the API call.
    - Displays the full `requests` code snippet and the formatted JSON response in `st.code`.

---

## 4. Design & UI/UX Principles

-   **Theme**: Professional, clean, and modern dark mode.
-   **Color Palette**:
    -   Background: `#0F1117`
    -   Primary Text: `#FFFFFF`
    -   Accent/Success (Green): `#00FF41`
    -   Emphasis/Warning (Orange): `#FF9100`
-   **Layout**: Multi-page app using Streamlit's native page structure. A persistent sidebar for navigation and authentication. Judicious use of `st.columns`, `st.tabs`, and `st.expander` to organize information without clutter.
-   **Components**: Full utilization of modern Streamlit components, including `st.metric`, `st.dataframe` (with column configuration), and `st.plotly_chart` for future financial charts.

---

## 5. Technical Architecture & Implementation Plan

This project will be developed in a new top-level directory named `streamlit_app/` to maintain clear separation from the API and worker code.

### 🗺️ Staged Implementation Roadmap (Gemini CLI)

#### Phase 0: Project Scaffolding
1.  **Create Directories**: `streamlit_app/`, `streamlit_app/pages/`, `streamlit_app/utils/`.
2.  **Initialize Files**:
    - `streamlit_app/requirements.txt` (streamlit, requests, pandas, plotly).
    - `streamlit_app/app.py` (Main "Home" page).
    - `streamlit_app/utils/api.py` (Placeholder for API client).
    - `streamlit_app/pages/1_Trader_Dashboard.py` (Page for the MVP use case).
    - `streamlit_app/pages/2_API_Explorer.py` (Page for the interactive explorer).

#### Phase 1: Core App & API Connectivity
1.  **`app.py`**:
    -   Implement the dark mode theme and general layout.
    -   Create the sidebar for API key input and store it in `st.session_state`.
2.  **`utils/api.py`**:
    -   Build a Python class `P2PAPIClient`.
    -   The constructor will take the API key.
    -   Methods will correspond to API endpoints (e.g., `get_offers(fiat, crypto)`).
    -   Incorporate error handling for API and network issues.

#### Phase 2: MVP Use Case - Trader's Dashboard
1.  **`pages/1_Trader_Dashboard.py`**:
    -   Add `st.selectbox` widgets for `fiat` and `crypto` selection.
    -   Instantiate `P2PAPIClient` from `utils.api` with the key from `st.session_state`.
    -   On selection, call the `get_offers` method.
    -   Use Pandas to calculate VWAP and other metrics from the returned data.
    -   Display results using `st.columns` and `st.metric`.
    -   Display the full offer list in `st.dataframe`.

#### Phase 3: Interactive API Explorer
1.  **`pages/2_API_Explorer.py`**:
    -   Define the available API endpoints and their parameters in a dictionary.
    -   Use a selectbox to choose an endpoint.
    -   Based on the selection, render the appropriate input widgets for parameters.
    -   On "Execute", build the request, call the relevant method in `P2PAPIClient`.
    -   Display the generated code snippet and JSON response.

---

## 6. Future Enhancements

-   **Historical Charting**: Add a "History" page with `st.plotly_chart` to visualize how VWAP and spread have evolved over time (requires historical data to be stored).
-   **Advertiser Deep-Dive**: A page to analyze a specific advertiser's offers and behavior.
-   **User Accounts**: Integrate user login to save preferences and API keys.

This refined PRD provides a clear and actionable roadmap. Once you approve this plan, I will begin **Phase 0: Project Scaffolding**.

# Annex 

# PRD: P2P Data Explorer - Streamlit Dashboard

## Executive Summary

This PRD defines a production-ready Streamlit application that serves as the primary interface for exploring P2P cryptocurrency trading data. Building on your robust data pipeline (worker → PostgreSQL → FastAPI), this dashboard transforms raw market data into actionable insights through interactive order book analysis, market depth visualization, and comprehensive filtering capabilities.

**Core Value Proposition:** Enable traders, analysts, and stakeholders to make data-driven decisions by providing real-time visibility into P2P market structure across multiple fiat/crypto pairs.

---

## 1. Architecture Context

Your ecosystem follows a clean separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│ DATA COLLECTION (worker/)                               │
│ Binance P2P → PostgreSQL (dimensional model)            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ DATA ACCESS (Api/)                                       │
│ FastAPI with authentication, MCP-aligned models          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ DATA EXPLORATION (streamlit_app/) ← THIS PRD            │
│ Interactive dashboards, order book analysis              │
└─────────────────────────────────────────────────────────┘
```

**Key Insight:** Your dimensional model (fact_offers + dims) enables sophisticated filtering by fiat, crypto, payment method, advertiser, and time—leverage this richness.

---

## 2. Enhanced Feature Set

### 2.1 Core Features (MVP+)

#### Feature 1: Live Order Book Dashboard ⭐ PRIMARY FEATURE
**User Story:** As a trader, I want to see aggregated buy/sell offers for a specific pair so I can identify market depth and best execution prices.

**Components:**
- **Pair Selector:** Dual dropdowns (Fiat + Crypto) with trade type toggle (BUY/SELL/BOTH)
- **Key Metrics Panel:**
  - Buy-side VWAP (Volume-Weighted Average Price)
  - Sell-side VWAP
  - Live Spread (%)
  - Total Available Volume
  - Active Advertisers Count
- **Order Book Table:**
  - Split-view: Buy orders (left) | Sell orders (right)
  - Columns: Price, Available Amount, Min/Max Limits, Payment Methods, Advertiser
  - Color-coded: Green for buy-side, Red for sell-side
  - Sortable by any column
- **Market Depth Chart:**
  - Plotly cumulative volume chart showing depth on both sides
  - Interactive hover showing exact volumes at price levels

**Implementation Tip:** Use `st.columns()` for split buy/sell view, `st.metric()` for KPIs with delta indicators, `st.plotly_chart()` for depth visualization.

---

#### Feature 2: Advanced Filtering & Analysis
**User Story:** As an analyst, I want to filter offers by multiple criteria to find arbitrage opportunities or analyze specific market segments.

**Filter Dimensions:**
- **Payment Methods:** Multi-select from available methods (Mercadopago, Zelle, Bank Transfer, etc.)
- **Advertiser Type:** Merchant vs. Individual
- **Price Range:** Slider with min/max price bounds
- **Volume Range:** Filter by available amount
- **Completion Rate:** Only show advertisers above X% completion
- **Time Window:** Select extraction timestamp range (if historical data available)

**Advanced Analysis Modes:**
1. **Spread Analyzer:** Show pairs ranked by spread size (arbitrage opportunities)
2. **Payment Method Comparison:** Compare average prices across different payment methods
3. **Advertiser Leaderboard:** Top advertisers by volume, completion rate, response time

**Implementation Tip:** Use `st.sidebar` for filters to keep main view clean. Use `st.expander()` for advanced filters to avoid overwhelming new users.

---

#### Feature 3: Interactive API Explorer
**User Story:** As a developer, I want to test API calls and see the exact code needed to replicate them.

**Components:**
- **Endpoint Selector:** Dropdown with all API endpoints
- **Dynamic Parameter Builder:** Forms that adapt based on selected endpoint
- **Code Generator:** Shows exact `requests` or `curl` command
- **Response Viewer:** Formatted JSON with syntax highlighting
- **Copy-to-Clipboard:** One-click code copying

**Implementation Tip:** Use `st.tabs()` to separate Request, Response, and Code views. Use `st.code()` with language="python" or "bash".

---

### 2.2 Enhanced Features (Phase 2)

#### Feature 4: Market Trends & Insights
- Historical price charts (if worker stores multiple snapshots)
- Volatility indicators
- Time-of-day patterns

#### Feature 5: Export & Reporting
- Download filtered data as CSV/Excel
- Generate PDF reports with key metrics
- Share dashboard snapshots via link

---

## 3. UI/UX Design Principles

### 3.1 Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│ HEADER: Logo + Title + API Key Status                   │
├─────────────────────────────────────────────────────────┤
│ SIDEBAR:                     │ MAIN CONTENT:            │
│ - Navigation                 │                          │
│ - Global Filters             │ [Dynamic Page Content]   │
│ - API Key Input              │                          │
│ - Quick Stats                │                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Page Navigation
Use Streamlit's native multi-page structure:
- `app.py`: Landing page with overview + API key setup
- `pages/1_📊_Order_Book.py`: Primary order book dashboard
- `pages/2_🔍_Market_Explorer.py`: Advanced filtering & analysis
- `pages/3_⚙️_API_Playground.py`: Interactive API testing
- `pages/4_📈_Analytics.py`: Trends & insights (Phase 2)

### 3.3 Color Scheme (Financial Dashboard)
- **Background:** `#0E1117` (Streamlit dark default)
- **Primary (Buy):** `#26A69A` (Teal green)
- **Secondary (Sell):** `#EF5350` (Red)
- **Accent:** `#FFA726` (Orange for highlights)
- **Text:** `#FAFAFA` (High contrast white)

---

## 4. Technical Implementation

### 4.1 Enhanced API Client (`utils/api.py`)

```python
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

class P2PAPIClient:
    """Enhanced API client with caching and error handling."""
    
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": self.api_key}
    
    def get_offers(
        self,
        fiat_code: Optional[str] = None,
        crypto_symbol: Optional[str] = None,
        trade_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        payment_method: Optional[str] = None,
        page: int = 1,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch offers with comprehensive filtering."""
        params = {k: v for k, v in locals().items() 
                  if v is not None and k not in ['self', 'params']}
        
        response = requests.get(
            f"{self.base_url}/api/v1/offers",
            headers=self.headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_cryptocurrencies(self) -> List[Dict[str, Any]]:
        """Fetch available cryptocurrencies."""
        response = requests.get(
            f"{self.base_url}/api/v1/cryptocurrencies",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_fiat_currencies(self) -> List[Dict[str, Any]]:
        """Fetch available fiat currencies."""
        response = requests.get(
            f"{self.base_url}/api/v1/fiat_currencies",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_payment_methods(self) -> List[Dict[str, Any]]:
        """Fetch available payment methods."""
        response = requests.get(
            f"{self.base_url}/api/v1/payment_methods",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
```

### 4.2 Order Book Calculations (`utils/calculations.py`)

```python
import pandas as pd
from decimal import Decimal
from typing import Tuple

def calculate_vwap(offers: pd.DataFrame) -> Decimal:
    """Calculate Volume-Weighted Average Price."""
    if offers.empty:
        return Decimal('0')
    
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
    df = pd.DataFrame(offers)
    
    # Extract nested data
    if 'cryptocurrency' in df.columns:
        df['crypto_symbol'] = df['cryptocurrency'].apply(lambda x: x['symbol'])
    if 'fiat_currency' in df.columns:
        df['fiat_code'] = df['fiat_currency'].apply(lambda x: x['currency_code'])
    if 'advertiser' in df.columns:
        df['advertiser_name'] = df['advertiser'].apply(lambda x: x['nickname'])
    
    # Filter by trade type
    df = df[df['trade_type'] == trade_type]
    
    # Sort: Buy orders descending, Sell orders ascending
    ascending = (trade_type == 'SELL')
    df = df.sort_values('price', ascending=ascending)
    
    return df
```

---

## 5. Implementation Roadmap

### Phase 1: Core Order Book (Week 1-2)
- [ ] Enhanced API client with all endpoints
- [ ] Order book dashboard with split buy/sell view
- [ ] VWAP calculations and spread analysis
- [ ] Basic filtering (fiat, crypto, trade type)
- [ ] Market depth visualization

### Phase 2: Advanced Filtering (Week 3)
- [ ] Payment method filtering
- [ ] Advertiser filtering (merchant vs. individual)
- [ ] Price/volume range sliders
- [ ] Completion rate filter
- [ ] Multi-criteria search

### Phase 3: Interactive API Explorer (Week 4)
- [ ] Dynamic endpoint selector
- [ ] Parameter builder
- [ ] Code generation
- [ ] Response viewer

### Phase 4: Analytics & Export (Week 5)
- [ ] Historical trends (if data available)
- [ ] Export to CSV/Excel
- [ ] Dashboard sharing

---

## 6. Sample Page Structure

### `pages/1_📊_Order_Book.py` (Detailed Wireframe)

```python
import streamlit as st
import pandas as pd
from streamlit_app.utils.api import P2PAPIClient
from streamlit_app.utils.calculations import (
    calculate_vwap, 
    calculate_spread,
    prepare_order_book_data
)

st.set_page_config(page_title="Order Book", layout="wide")

# Check API key
if 'api_key' not in st.session_state:
    st.error("Please enter your API key on the home page.")
    st.stop()

client = P2PAPIClient(st.session_state['api_key'])

# Header
st.title("📊 Live Order Book Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    # Fetch available pairs
    fiats = client.get_fiat_currencies()
    cryptos = client.get_cryptocurrencies()
    
    selected_fiat = st.selectbox(
        "Fiat Currency",
        options=[f['currency_code'] for f in fiats],
        index=0
    )
    
    selected_crypto = st.selectbox(
        "Cryptocurrency",
        options=[c['symbol'] for c in cryptos],
        index=0
    )
    
    view_mode = st.radio(
        "View Mode",
        options=["Split (Buy & Sell)", "Buy Only", "Sell Only"],
        index=0
    )
    
    # Advanced filters (in expander)
    with st.expander("⚙️ Advanced Filters"):
        payment_methods = client.get_payment_methods()
        selected_methods = st.multiselect(
            "Payment Methods",
            options=[pm['method_code'] for pm in payment_methods]
        )
        
        min_price = st.number_input("Min Price", min_value=0.0, value=0.0)
        max_price = st.number_input("Max Price", min_value=0.0, value=0.0)

# Fetch data
with st.spinner("Loading order book..."):
    buy_offers = client.get_offers(
        fiat_code=selected_fiat,
        crypto_symbol=selected_crypto,
        trade_type="BUY",
        min_price=min_price if min_price > 0 else None,
        max_price=max_price if max_price > 0 else None
    )
    
    sell_offers = client.get_offers(
        fiat_code=selected_fiat,
        crypto_symbol=selected_crypto,
        trade_type="SELL",
        min_price=min_price if min_price > 0 else None,
        max_price=max_price if max_price > 0 else None
    )

# Prepare DataFrames
buy_df = prepare_order_book_data(buy_offers, "BUY")
sell_df = prepare_order_book_data(sell_offers, "SELL")

# Calculate metrics
buy_vwap = calculate_vwap(buy_df)
sell_vwap = calculate_vwap(sell_df)
spread = calculate_spread(buy_vwap, sell_vwap)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Buy VWAP", f"{buy_vwap:.2f} {selected_fiat}", 
            delta=None, delta_color="normal")
col2.metric("Sell VWAP", f"{sell_vwap:.2f} {selected_fiat}", 
            delta=None, delta_color="inverse")
col3.metric("Spread", f"{spread:.2f}%", 
            delta=None, delta_color="off")
col4.metric("Total Volume", 
            f"{buy_df['available_amount'].sum() + sell_df['available_amount'].sum():.2f} {selected_crypto}")

# Order Book View
if view_mode == "Split (Buy & Sell)":
    col_buy, col_sell = st.columns(2)
    
    with col_buy:
        st.subheader("🟢 Buy Orders")
        st.dataframe(
            buy_df[['price', 'available_amount', 'min_limit', 'max_limit', 'advertiser_name']],
            use_container_width=True,
            height=400
        )
    
    with col_sell:
        st.subheader("🔴 Sell Orders")
        st.dataframe(
            sell_df[['price', 'available_amount', 'min_limit', 'max_limit', 'advertiser_name']],
            use_container_width=True,
            height=400
        )

elif view_mode == "Buy Only":
    st.subheader("🟢 Buy Orders")
    st.dataframe(buy_df, use_container_width=True)

else:  # Sell Only
    st.subheader("🔴 Sell Orders")
    st.dataframe(sell_df, use_container_width=True)

# Market Depth Chart
st.subheader("📈 Market Depth")
# (Plotly cumulative volume chart implementation here)
```

---

## 7. Success Metrics

**User Engagement:**
- Daily active users
- Average session duration
- Pages per session

**Feature Adoption:**
- % of users using advanced filters
- API Explorer usage rate
- Export feature utilization

**Performance:**
- Page load time < 2s
- API response time < 500ms
- Error rate < 1%

---

## 8. Next Steps

1. **Review & Approve** this PRD
2. **Prioritize Features** based on your immediate needs
3. **Begin Phase 1** with order book core functionality
4. **Iterate** based on user feedback

Would you like me to:
1. Create the complete implementation for the Order Book page?
2. Design the market depth visualization logic?
3. Build the advanced filtering system?
4. Develop the API Explorer interface?

This dashboard will transform your dimensional P2P data into a powerful analytical tool—think of it as giving traders "X-ray vision" into the P2P market structure across all your configured pairs.
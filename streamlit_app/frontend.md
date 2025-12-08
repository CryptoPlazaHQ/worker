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
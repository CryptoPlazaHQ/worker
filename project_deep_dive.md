# Project Structure and Data Interaction Deep Dive

This document provides a comprehensive overview of the project's structure, focusing on the Phase 1: Data Ingestion workflow and its foundational role for the subsequent Phase 2: Data Access via FastAPI and the Model Context Protocol (MCP).

## 1. Overall Project Goal

The primary goal is to establish a robust and scalable pipeline for extracting Binance P2P trading data, storing it in a PostgreSQL database, and subsequently exposing this data through a FastAPI for analysis, dashboards, and AI tooling (MCP).

## 2. Phase 1: Data Ingestion (Current Focus)

The current phase is dedicated to building and stabilizing the data collection pipeline. As per `P2P_worker_refactor.md` and `report.md`, this phase is now largely complete and operational.

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 1: DATA INGESTION │
│ │
│ 📚 Worker ─────→ 🏪 Binance P2P ─────→ 🗄️ PostgreSQL │
│ (Your code) (Public API) (Your warehouse)│
│ │
└─────────────────────────────────────────────────────────┘
```

### 2.1 Key Components and Their Roles

The `worker/` directory houses the core components of the data ingestion pipeline:

*   **`worker/main.py`**: The entry point for the data ingestion worker. It orchestrates the extraction and loading process, typically scheduling these tasks at defined intervals.
*   **`worker/config.py`**: Manages all configuration settings for the worker. This includes sensitive information (like database URLs via environment variables) and dynamic configurations (like trading pairs from `p2p_config.json`).
    *   **`p2p_config.json`**: A critical configuration file that defines the fiat currencies, cryptocurrencies, and other parameters (e.g., `binance_p2p_until_page`) for which the worker should extract data. This provides flexibility without code changes.
*   **`worker/extractor.py`**: Responsible for interacting with the Binance P2P API.
    *   It mimics browser requests (`_get_headers`) to avoid detection/blocking.
    *   It dynamically generates trading pairs based on `p2p_config.json`.
    *   It uses a `requests.Session` with retry logic for robustness.
    *   It features `extract_pair_offers` to fetch offers for specific pairs and `extract_all_offers` to parallelize extraction across all configured pairs using a `ThreadPoolExecutor`.
    *   The `_parse_offer` method cleans and normalizes the raw JSON response from Binance into a structured dictionary format, ready for the loader. This includes extracting `advertiser.get("userNo")` as the `advertiser_id` and `adv.get("advNo")` as the external `offer_id`.
*   **`worker/loader.py`**: Handles the transformation and loading of the extracted data into the PostgreSQL database.
    *   It utilizes SQLAlchemy ORM models (`worker/models.py`) to interact with the database.
    *   It implements a "get-or-create" logic (`_get_or_create_crypto`, `_get_or_create_fiat`, etc.) for dimension tables (`dim_cryptocurrencies`, `dim_fiat_currencies`, `dim_payment_methods`, `dim_advertisers`). This prevents duplicate entries and ensures referential integrity, while also leveraging caching for performance.
    *   It populates the `fact_offers` and `fact_offer_payment_methods` tables, linking them to the appropriate dimensions via foreign keys.
    *   Handles the `NotNullViolation` fix for `advertiser_id` as detailed in `report.md`.
*   **`worker/db.py`**: Manages the SQLAlchemy database engine and session creation.
    *   Provides a `DatabaseManager` class for connection pooling and robust session management.
    *   Offers a `get_session` context manager, ensuring proper session lifecycle (commit on success, rollback on error, close always).
    *   Configures connection events and tests connectivity on startup.
*   **`worker/models.py`**: Defines the SQLAlchemy ORM (Object Relational Mapping) models that directly correspond to the database schema (`schema.sql`). This provides a Pythonic interface for interacting with the database tables.
*   **`rate_limiter.py`**: Implements a mechanism to control the rate of requests to external APIs (e.g., Binance P2P) to avoid hitting rate limits.

### 2.2 Data Ingestion Workflow

1.  **Configuration Loading**: `worker/main.py` initializes `config.py`, loading settings from environment variables and `p2p_config.json`.
2.  **Pair Generation**: `extractor.py`'s `get_all_trading_pairs()` method reads `p2p_config.json` to identify all fiat/crypto/trade\_type combinations for data extraction.
3.  **Parallel Extraction**: `extractor.py`'s `extract_all_offers()` method uses a `ThreadPoolExecutor` to concurrently call `extract_pair_offers()` for each trading pair.
    *   Each `extract_pair_offers()` call sends POST requests to the Binance P2P API, applying rate limiting (`rate_limiter.acquire()`) and mimicking browser headers.
    *   Raw responses are processed by `_parse_offer()`, which extracts relevant fields, performs basic validation, and formats the data.
4.  **Batch Loading**: The list of parsed offers is passed to `loader.py`'s `load_offers()` method along with a unique `batch_id`.
5.  **Dimension Management**: `loader.py` uses `_get_or_create` methods to ensure that dimension records (cryptocurrencies, fiat currencies, advertisers, payment methods) exist in their respective `dim_` tables. If a record doesn't exist, it's created; otherwise, its existing ID is retrieved.
    *   For `dim_advertisers`, an SCD Type 2 approach is partially implemented to track changes in advertiser details (though `loader.py` currently focuses on getting the `is_current=True` record).
6.  **Fact Insertion**: Once dimension IDs are resolved, `loader.py` inserts new records into `fact_offers` and `fact_offer_payment_methods`, linking them to the dimensions using foreign keys.

## 3. Phase 2: Data Access with FastAPI and MCP (Next Steps)

With the data ingestion pipeline established and populating the PostgreSQL database, the project is ready to proceed with Phase 2: exposing this valuable data.

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 2: DATA ACCESS (Later) │
│ │
│ 👥 Streamlit ───→ 🏢 FastAPI ───→ 🗄️ PostgreSQL │
│ (Customers) (Your Store) (Your data) │
│ │
└─────────────────────────────────────────────────────────┘
```

### 3.1 Role of FastAPI

FastAPI will serve as the primary interface for applications (e.g., Streamlit dashboards, AI tooling) to interact with the P2P data. It will provide:

*   **Structured Endpoints**: RESTful APIs for querying offers, advertisers, cryptocurrencies, etc.
*   **Data Validation and Serialization**: Automatically handled by Pydantic models (which integrate well with MCP).
*   **Authentication/Authorization**: To control access to the data.
*   **Performance**: High-performance asynchronous processing suitable for data serving.

### 3.2 Role of MCP (Model Context Protocol)

The MCP is crucial for ensuring consistency and interoperability of data models across different parts of the system and with external tools.

*   **Standardized Data Representation**: MCP models will define the exact structure of data exposed by the FastAPI.
*   **Abstraction over Database Schema**: While the FastAPI will query the PostgreSQL database, the MCP models will provide a cleaner, API-centric view of the data, abstracting away internal database specifics (like surrogate keys vs. natural keys, or SCD implementation details).
*   **Facilitating AI Tooling**: By adhering to a defined MCP, AI models and data scientists can easily understand and consume the data without needing deep knowledge of the underlying database schema.

### 3.3 Mapping Database Schema to FastAPI/MCP

As detailed in the updated `schema.md`, the database schema directly informs the design of FastAPI endpoints and MCP models:

*   **`dim_cryptocurrencies` -> `Cryptocurrency` MCP Model**: Simple 1:1 mapping.
*   **`dim_fiat_currencies` -> `FiatCurrency` MCP Model**: Simple 1:1 mapping.
*   **`dim_payment_methods` -> `PaymentMethod` MCP Model**: Simple 1:1 mapping.
*   **`dim_advertisers` -> `Advertiser` MCP Model**: The API will likely expose the *current* state of an advertiser (filtered `is_current=TRUE`), using `advertiser_id` as the primary identifier. Historical data will be available for analytical queries if required.
*   **`fact_offers` and `fact_offer_payment_methods` -> `Offer` MCP Model**: This will be a rich model combining fields from `fact_offers` with nested or joined information from its related dimension tables (Cryptocurrency, FiatCurrency, Advertiser, PaymentMethods). This will provide a comprehensive view of an offer through a single API call.

## Conclusion

The project's current data ingestion pipeline is a robust foundation. With a clear, well-defined database schema and a strategic plan for FastAPI and MCP integration, the path forward for data access, analysis, and AI tooling is well-defined. The next step is to begin implementing the FastAPI application, leveraging the existing data models and the detailed `schema.md` as the authoritative source for data structure.

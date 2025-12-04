# PRD: Binance P2P Data Interaction FastAPI - Phase II Implementation

## 1. Executive Summary

This document outlines the detailed plan for implementing the Phase II FastAPI application, utilizing the provided "Api" folder as a foundational framework. The core objective is to evolve this existing FastAPI to interact with and expose the rich dimensional data populated by the Phase I data ingestion worker (located in the root `worker/` directory) into the primary PostgreSQL database. This PRD details the necessary adaptations, refactorings, and new feature implementations to align the "Api" framework with the strategic goal of providing structured, queryable access to the worker's ingested data, adhering to best practices and professional enhancement.

## 2. Goals

The primary goals for this implementation phase are to:

*   **Integrate with Worker's Database:** Establish a connection and interaction mechanism between the "Api" FastAPI and the primary PostgreSQL database populated by the `worker/` application.
*   **Expose Dimensional Data:** Provide read-only API endpoints for querying data from the `dim_cryptocurrencies`, `dim_fiat_currencies`, `dim_advertisers`, `dim_payment_methods`, `fact_offers`, and `fact_offer_payment_methods` tables.
*   **Align Data Models (MCP):** Redefine the FastAPI's internal ORM models and Pydantic schemas to accurately reflect and expose the dimensional model, serving as the Model Context Protocol (MCP) for downstream AI/ML tooling and analysis.
*   **Leverage Existing Framework:** Utilize the existing robust FastAPI setup, authentication, and core architectural patterns present in the provided "Api" folder.
*   **Ensure Data Consistency:** Guarantee that the data exposed by the API is consistent with the output of the data ingestion worker.
*   **Maintain Performance and Scalability:** Design endpoints for efficient querying of potentially large datasets.

## 3. Current State of the "Api" Framework (Analysis of `Api` folder)

The provided "Api" folder contains a functional FastAPI application with the following characteristics:

*   **Self-Contained Database:** It currently defines and operates on its own simplified database schema (ORM models in `Api/p2p_api/database.py`, Pydantic schemas in `Api/p2p_api/schemas.py`) which primarily includes `Offer`, `Run`, `PaymentMethod`, `User`, `APIKey`.
*   **Internal Scrapers:** It contains its own scraping logic (`Api/p2p_api/binance_scraper.py`, `Api/p2p_api/bybit_scraper.py`) and exposes endpoints (`/api/v1/binance/offers`) to *trigger new data ingestion directly into its own database*.
*   **Simplified Offer Model:** Its `Offer` model stores fiat, asset, advertiser as direct strings and price/limits as floats/numerics, and directly embeds payment methods as a list of strings. This is a denormalized view compared to the worker's dimensional model.
*   **Existing Components:** It includes robust FastAPI setup (`main.py`), API Key authentication (`auth.py`, `dependencies.py`), CRUD operations (`crud.py`), configuration (`config.py`), logging (`logging_config.py`), and a testing suite (`tests/`).

## 4. Desired State (Phase II Alignment)

The "Api" FastAPI will be transformed to:

*   Connect to the *same PostgreSQL database* as the `worker/` application.
*   Expose query endpoints that retrieve data from the `worker/`'s dimensional schema.
*   Maintain its existing features like authentication and system management.

## 5. Gap Analysis (Mismatch between Current and Desired State)

The primary gap is the **database and schema divergence**:

*   The `Api` framework currently connects to and operates on its own dedicated database and simplified schema.
*   The `worker/` application populates a separate database with a rich dimensional schema (using `dim_` and `fact_` tables).

To bridge this gap, the `Api` framework needs to be refactored to interact with the *worker's* database and adopt its dimensional model.

## 6. Proposed Solution / Implementation Tasks

### 6.1. Database Configuration and Connection Refactoring

*   **Task 1.1: Update `Api/p2p_api/config.py`**
    *   Modify `WorkerSettings` (or rename/create new settings class) to retrieve `DATABASE_URL` for the primary dimensional database (the one the worker feeds). Ensure it correctly uses environment variables (e.g., `WORKER_DATABASE_URL` or a new API-specific `API_DATABASE_URL`).
    *   (Consider removing `p2p_config_path` if the FastAPI will not be directly using `p2p_config.json` for its data access logic, or clarify its role.)

*   **Task 1.2: Refactor `Api/p2p_api/database.py`**
    *   Remove or comment out the existing `Base` and ORM model definitions (`Offer`, `PaymentMethod`, `Run`, `User`, `APIKey`).
    *   Import the ORM models directly from the main project's `worker/models.py` (or create symbolic links/shared module if `worker/models.py` is to be strictly decoupled). The goal is for the API to use the exact same ORM model definitions as the worker to interact with the database.
    *   Ensure `init_db` correctly sets up SQLAlchemy for the primary PostgreSQL database.

### 6.2. Schema and Model Alignment (MCP Integration)

*   **Task 2.1: Overhaul `Api/p2p_api/schemas.py`**
    *   Replace the existing simplified `Offer`, `PaymentMethod` schemas with Pydantic models that precisely map to the dimensional models (`dim_cryptocurrencies`, `dim_fiat_currencies`, `dim_payment_methods`, `dim_advertisers`, `fact_offers`, `fact_offer_payment_methods`) defined in the `worker/models.py`.
    *   Introduce explicit MCP-aligned Pydantic models for:
        *   `Cryptocurrency` (mapping to `dim_cryptocurrencies`)
        *   `FiatCurrency` (mapping to `dim_fiat_currencies`)
        *   `PaymentMethod` (mapping to `dim_payment_methods`)
        *   `Advertiser` (mapping to `dim_advertisers`, focusing on `is_current=TRUE`)
        *   `Offer` (a rich model combining `fact_offers` with nested `Cryptocurrency`, `FiatCurrency`, `Advertiser`, and `PaymentMethods` from `fact_offer_payment_methods`).
    *   Retain `User` and `APIKey` schemas as they are valid for API management.
    *   Retain `Run` schemas for managing extraction runs, though their purpose might shift from storing new scrapes to perhaps tracking API query performance or similar.

### 6.3. CRUD Operations Refactoring

*   **Task 3.1: Rewrite `Api/p2p_api/crud.py`**
    *   Remove `get_or_create_payment_method` and `create_offer`, as the API will no longer directly ingest data using its own simplified models.
    *   Implement new read-only CRUD functions (`get_offers`, `get_advertisers`, `get_cryptocurrencies`, `get_fiat_currencies`, `get_payment_methods`) that query the dimensional models imported from `worker/models.py`.
    *   These functions must handle filtering, pagination, sorting, and join operations as needed to construct the rich MCP models.
    *   Retain and adapt `create_run` and `finalize_run` if the API needs to track its own operations or provide a mechanism to trigger the *worker*'s scraping. (Initial thought: the API should *not* trigger the worker's scraping, as the worker runs independently. The `Run` table might become a read-only view of the worker's runs, or be repurposed for API-specific activities). For Phase II, assume the worker runs independently.
    *   Retain and adapt User and API Key CRUD operations.

### 6.4. API Endpoint Overhaul

*   **Task 4.1: Modify `Api/p2p_api/main.py` and `Api/p2p_api/routers/`**
    *   **Remove/Deprecate Internal Scrapers:** Remove or clearly mark as deprecated `Api/p2p_api/binance_scraper.py` and `Api/p2p_api/bybit_scraper.py`.
    *   **Revise `/api/v1/binance/offers`:** Change this endpoint's functionality from triggering a scrape to performing a query against the dimensional `fact_offers` table. Update its parameters and `response_model` to return the rich `Offer` MCP model.
    *   **Implement New Query Endpoints:** Create new endpoints based on the `prd_proposal.md` for querying:
        *   `GET /api/v1/offers`: Paginated, filterable list of rich `Offer` MCP models.
        *   `GET /api/v1/offers/{offer_external_id}`: Single rich `Offer` MCP model.
        *   `GET /api/v1/advertisers`: Paginated, filterable list of `Advertiser` MCP models (for current advertisers).
        *   `GET /api/v1/advertisers/{advertiser_id}`: Single `Advertiser` MCP model.
        *   `GET /api/v1/cryptocurrencies`: List of `Cryptocurrency` MCP models.
        *   `GET /api/v1/fiat_currencies`: List of `FiatCurrency` MCP models.
        *   `GET /api/v1/payment_methods`: List of `PaymentMethod` MCP models.
    *   **Update `/api/v1/binance/pairs`:** Ensure it now queries `dim_cryptocurrencies` and `dim_fiat_currencies` from the dimensional database to generate pairs, or retrieve pre-defined pairs if `p2p_config.json` remains the source of truth for *configured* pairs.

### 6.5. Testing Adjustments

*   **Task 5.1: Update `Api/tests/test_main.py` and `Api/tests/conftest.py`**
    *   Modify existing tests to reflect the new database schema interaction and endpoint functionalities.
    *   Add new tests for the newly implemented query endpoints.
    *   Ensure the test database setup aligns with the worker's database schema for testing purposes.

### 6.6. Documentation Updates

*   **Task 6.1: Update `Api/README.md` and `Api/docs/`**
    *   Reflect the new API functionalities, especially the shift from scraping to querying the worker's database.
    *   Provide updated examples for the new query endpoints.
    *   Clarify the relationship between this API and the separate worker application.

## 7. Technical Stack

*   **Framework:** FastAPI (Python)
*   **Database Interaction:** SQLAlchemy ORM (re-aligned with worker's models)
*   **Data Validation:** Pydantic (for MCP models)
*   **Database:** PostgreSQL (primary dimensional database)
*   **Migrations:** Alembic (existing setup to be reviewed for compatibility with new ORM models if needed)
*   **Deployment:** Docker (existing setup)
*   **Authentication:** API Key (existing setup)

## 8. Deliverables

*   Updated "Api" folder reflecting all implementation tasks.
*   Revised `prd_implementation.md` with any further refinements during the process.
*   Updated local git repository with all changes committed and ready for push.

This PRD provides a clear roadmap for transforming the provided "Api" framework into the Phase II FastAPI that interacts with your worker's populated database.

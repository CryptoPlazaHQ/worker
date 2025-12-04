# PRD Proposal: Binance P2P Data Access FastAPI

## 1. Introduction/Executive Summary

This document proposes the Product Requirements Document (PRD) for a FastAPI application designed to expose the Binance P2P trading data currently ingested into a PostgreSQL database. This API will serve as the primary interface for various downstream applications, including dashboards, analytical tools, and AI/ML models utilizing the Model Context Protocol (MCP), to interact with the collected data. The FastAPI will provide structured, secure, and performant access to the rich dataset, enabling data analysis and monetization opportunities.

This proposal aligns with Phase 2: Data Access as outlined in `project_deep_dive.md` and builds directly upon the robust data ingestion pipeline detailed in `documentation.md`.

## 2. Goals

The primary goals of this FastAPI are to:

*   **Provide programmatic access:** Offer a standardized RESTful interface for external applications to query the Binance P2P data.
*   **Enable data consumption:** Facilitate the integration of business intelligence dashboards and analytical tools that leverage the ingested data.
*   **Support AI/ML tooling (MCP):** Expose data using well-defined Model Context Protocol (MCP) data models to ensure consistency and ease of consumption by AI/ML applications.
*   **Ensure data integrity and consistency:** Validate API requests and structure responses in a consistent manner, reflecting the underlying database schema.
*   **Maintain performance and scalability:** Design endpoints to be efficient and scalable to handle a growing volume of data and requests.
*   **Implement robust security:** Safeguard data access through appropriate authentication and authorization mechanisms.

## 3. Scope

### 3.1. In-Scope Functionalities

*   **Data Querying:**
    *   Retrieve lists of offers with filtering, pagination, and sorting.
    *   Retrieve specific offers by ID.
    *   Retrieve lists of advertisers with filtering and pagination.
    *   Retrieve specific advertisers by ID.
    *   Retrieve lists of cryptocurrencies, fiat currencies, and payment methods.
*   **Data Models (MCP):** Definition of Pydantic models for all exposed entities (Offer, Advertiser, Cryptocurrency, FiatCurrency, PaymentMethod) directly mapping to the database schema.
*   **Basic Authentication/Authorization:** Integration with a standard authentication method (e.g., API Key, JWT).
*   **Error Handling:** Consistent and informative error responses.

### 3.2. Out-of-Scope Functionalities (for initial release)

*   **Data Modification/Writes:** The API will be read-only in its initial release.
*   **Complex Analytics:** No embedded complex analytical functions (e.g., arbitrage calculation) beyond basic data retrieval. These should be handled by downstream applications.
*   **Real-time Subscriptions:** No WebSocket or SSE for real-time data streaming (beyond the existing worker's SSE capabilities for its own runs).
*   **Advanced Search/Aggregation:** While basic filtering will be supported, highly complex full-text search or advanced aggregations will be out of scope for the initial release.

## 4. Target Audience

*   **Data Analysts:** Building dashboards and reports.
*   **Data Scientists/ML Engineers:** Training and deploying AI/ML models based on P2P data (leveraging MCP).
*   **Application Developers:** Integrating P2P data into various applications.

## 5. Functional Requirements (API Endpoints)

All endpoints will return JSON responses. Request bodies will conform to Pydantic schemas.

### 5.1. Offers Endpoints

#### `GET /offers`

*   **Description:** Retrieves a paginated and filterable list of P2P offers.
*   **HTTP Method:** `GET`
*   **Query Parameters:**
    *   `fiat_currency_code` (string, optional): Filter by fiat currency code (e.g., "ARS").
    *   `crypto_symbol` (string, optional): Filter by cryptocurrency symbol (e.g., "USDT").
    *   `trade_type` (string, optional): Filter by trade type ("BUY" or "SELL").
    *   `min_price` (float, optional): Filter offers with price greater than or equal to this value.
    *   `max_price` (float, optional): Filter offers with price less than or equal to this value.
    *   `advertiser_id` (string, optional): Filter by Binance's external advertiser ID.
    *   `payment_method_code` (string, optional): Filter by payment method code (e.g., "Mercadopago").
    *   `page` (integer, optional, default: 1): Page number for pagination.
    *   `page_size` (integer, optional, default: 100, max: 1000): Number of items per page.
    *   `sort_by` (string, optional, default: "extraction_timestamp"): Field to sort by (e.g., "price", "extraction_timestamp").
    *   `sort_order` (string, optional, default: "desc"): Sort order ("asc" or "desc").
*   **Response Body (200 OK):** `List[Offer]` (MCP Offer Model)
    *   Includes total count and pagination metadata.
*   **Error Responses:**
    *   `400 Bad Request`: Invalid query parameters.
    *   `500 Internal Server Error`: Server-side issues.

#### `GET /offers/{offer_external_id}`

*   **Description:** Retrieves a single offer by its external Binance ID.
*   **HTTP Method:** `GET`
*   **Path Parameters:**
    *   `offer_external_id` (string, required): The external ID of the offer (`advNo` from Binance).
*   **Response Body (200 OK):** `Offer` (MCP Offer Model)
*   **Error Responses:**
    *   `404 Not Found`: Offer with the given ID not found.
    *   `500 Internal Server Error`: Server-side issues.

### 5.2. Advertisers Endpoints

#### `GET /advertisers`

*   **Description:** Retrieves a paginated and filterable list of current advertisers.
*   **HTTP Method:** `GET`
*   **Query Parameters:**
    *   `nickname` (string, optional): Filter by advertiser nickname (partial match).
    *   `is_merchant` (boolean, optional): Filter by merchant status.
    *   `min_completion_rate` (float, optional): Filter by minimum completion rate.
    *   `page` (integer, optional, default: 1): Page number.
    *   `page_size` (integer, optional, default: 100, max: 1000): Items per page.
    *   `sort_by` (string, optional, default: "nickname"): Field to sort by.
    *   `sort_order` (string, optional, default: "asc"): Sort order.
*   **Response Body (200 OK):** `List[Advertiser]` (MCP Advertiser Model)
    *   Note: This will return the *current* version of the advertiser from `dim_advertisers` (`is_current=TRUE`).
*   **Error Responses:**
    *   `400 Bad Request`: Invalid query parameters.
    *   `500 Internal Server Error`: Server-side issues.

#### `GET /advertisers/{advertiser_id}`

*   **Description:** Retrieves a specific advertiser by their external Binance ID.
*   **HTTP Method:** `GET`
*   **Path Parameters:**
    *   `advertiser_id` (string, required): The external ID of the advertiser (`userNo` from Binance).
*   **Response Body (200 OK):** `Advertiser` (MCP Advertiser Model)
    *   Returns the *current* version of the advertiser.
*   **Error Responses:**
    *   `404 Not Found`: Advertiser with the given ID not found.
    *   `500 Internal Server Error`: Server-side issues.

### 5.3. Dimension Endpoints

#### `GET /cryptocurrencies`

*   **Description:** Retrieves a list of supported cryptocurrencies.
*   **HTTP Method:** `GET`
*   **Query Parameters:**
    *   `symbol` (string, optional): Filter by crypto symbol.
    *   `is_active` (boolean, optional): Filter by active status.
*   **Response Body (200 OK):** `List[Cryptocurrency]` (MCP Cryptocurrency Model)

#### `GET /fiat_currencies`

*   **Description:** Retrieves a list of supported fiat currencies.
*   **HTTP Method:** `GET`
*   **Query Parameters:**
    *   `currency_code` (string, optional): Filter by currency code.
    *   `country_code` (string, optional): Filter by country code.
    *   `is_active` (boolean, optional): Filter by active status.
*   **Response Body (200 OK):** `List[FiatCurrency]` (MCP FiatCurrency Model)

#### `GET /payment_methods`

*   **Description:** Retrieves a list of supported payment methods.
*   **HTTP Method:** `GET`
*   **Query Parameters:**
    *   `method_code` (string, optional): Filter by method code.
    *   `category` (string, optional): Filter by category.
    *   `is_active` (boolean, optional): Filter by active status.
*   **Response Body (200 OK):** `List[PaymentMethod]` (MCP PaymentMethod Model)

## 6. Data Models (Model Context Protocol - MCP)

These Pydantic models will define the structure of data exposed by the API, directly mapping to the database schema (`schema.md` and `worker/models.py`). They represent the MCP for AI tooling and consistent data interaction.

### `Cryptocurrency` (Maps to `dim_cryptocurrencies`)

```python
from pydantic import BaseModel

class Cryptocurrency(BaseModel):
    id: int # Maps to crypto_id
    symbol: str
    name: str
    binance_asset_code: str
    is_active: bool
```

### `FiatCurrency` (Maps to `dim_fiat_currencies`)

```python
from pydantic import BaseModel

class FiatCurrency(BaseModel):
    id: int # Maps to fiat_id
    currency_code: str
    currency_name: str
    country_code: Optional[str] = None
    is_active: bool
```

### `PaymentMethod` (Maps to `dim_payment_methods`)

```python
from pydantic import BaseModel

class PaymentMethod(BaseModel):
    id: int # Maps to payment_method_id
    method_code: str
    method_name: str
    category: Optional[str] = None
    is_active: bool
```

### `Advertiser` (Maps to `dim_advertisers` - current record)

```python
from pydantic import BaseModel

class Advertiser(BaseModel):
    # This represents the current state of an advertiser
    id: str # Maps to advertiser_id
    nickname: str
    is_merchant: bool
    registration_days: Optional[int] = None
    # For simplicity, completion_rate and total_orders_count are denormalized in fact_offers,
    # but could also be aggregated/denormalized here if needed for direct advertiser endpoint use.
    # For now, we'll expose a simplified current view.
```

### `Offer` (Maps to `fact_offers` with joined dimensions)

```python
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List

class Offer(BaseModel):
    id: int # Maps to offer_id (surrogate key of the snapshot)
    external_id: str # Maps to offer_external_id (Binance's advNo)
    extraction_timestamp: datetime
    trade_type: str # "BUY" or "SELL"
    price: Decimal
    available_amount: Decimal
    min_limit: Decimal
    max_limit: Decimal

    # Denormalized Advertiser details (from fact_offers for performance)
    advertiser_nickname: str # From advertiser_sk -> dim_advertisers.nickname
    advertiser_completion_rate: Optional[Decimal] = None
    advertiser_total_orders: Optional[int] = None

    # Foreign key references to dimension details
    cryptocurrency: Cryptocurrency # Nested model
    fiat_currency: FiatCurrency # Nested model
    payment_methods: List[PaymentMethod] # Join with fact_offer_payment_methods -> dim_payment_methods
```
*(Note: The `Offer` model demonstrates how attributes from `fact_offers` would be combined with nested/joined dimension data. The `payment_methods` list would require an additional join or subquery logic.)*

## 7. Non-Functional Requirements

*   **Performance:**
    *   API response times for single resource retrieval should be under 100ms.
    *   API response times for list endpoints (with pagination) should be under 500ms for typical queries.
    *   Scalability to handle `X` concurrent requests (to be defined).
*   **Security:**
    *   **Authentication:** API Key-based authentication (Bearer token in `Authorization` header).
    *   **Authorization:** Role-based access control (RBAC) if different tiers of access are required (e.g., read-only for public, admin for internal tools) - *initially, all authenticated users will have read access.*
    *   Input validation and sanitization.
    *   Protection against common web vulnerabilities (e.g., SQL injection, XSS).
*   **Observability:**
    *   Comprehensive logging (request/response, errors, performance metrics).
    *   Integration with a monitoring system (e.g., Prometheus/Grafana) for API health and performance metrics.
    *   Tracing (as already set up by `get_fast_api_app` snippet).
*   **Maintainability:**
    *   Clean, modular code structure.
    *   Comprehensive unit and integration tests.
    *   Clear documentation for API consumers (OpenAPI/Swagger UI automatically generated by FastAPI).
*   **Reliability:** High availability with appropriate error handling and retry mechanisms for database interactions.

## 8. Technical Considerations

*   **Framework:** FastAPI (Python) - chosen for its performance, Pydantic integration, and automatic OpenAPI documentation.
*   **Database Interaction:** SQLAlchemy ORM (leveraging existing `worker/models.py`) for type-safe and efficient database queries.
*   **Deployment:** Containerization (Docker) for consistent deployment across environments.
*   **Environment:** Python 3.10+
*   **Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary` (for PostgreSQL), `pydantic`.

## 9. Future Considerations

*   **Write Endpoints:** Adding endpoints for data modification (e.g., updating advertiser details) once read-only access is stable.
*   **Advanced Analytics Endpoints:** Implementing endpoints for pre-computed analytics or exposing more complex aggregations.
*   **Real-time Data:** Integrating WebSockets for real-time offer updates.
*   **Full-Text Search:** Implementing full-text search capabilities for offers/advertisers.
*   **GraphQL Endpoint:** Exploring GraphQL for more flexible data querying.

This PRD provides a solid foundation for the development of the Binance P2P Data Access FastAPI, ensuring alignment with project goals and technical best practices.

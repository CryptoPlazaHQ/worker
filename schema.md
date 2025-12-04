# Database Schema Deep Dive

This document provides a detailed explanation of the database schema used by the Binance P2P data ingestion worker. This schema is designed to store and organize the data extracted from the Binance P2P API in a way that is efficient, scalable, and easy to query. It also serves as a foundational reference for the upcoming FastAPI implementation, which will expose this data for various applications and AI tooling via the Model Context Protocol (MCP).

## Overview

The database schema adheres to a dimensional modeling approach, consisting of two main types of tables:

*   **Dimension Tables (dim_\*):** These tables store descriptive attributes about the entities involved in the P2P trading process, such as cryptocurrencies, fiat currencies, payment methods, and advertisers. Dimension tables are designed to be relatively static and are used to provide context for the fact tables.
*   **Fact Tables (fact_\*):** These tables store the measurements or metrics that result from the P2P trading process, such as offer prices, available amounts, and trade types. Fact tables are designed to be dynamic, often including foreign keys to dimension tables, and are used to track the performance of the P2P trading process over time.

## Dimension Tables

Dimension tables store descriptive attributes about the entities involved in the P2P trading process. They provide context for the fact tables and are relatively static.

### `dim_cryptocurrencies`

Stores information about cryptocurrencies.

| Column Name        | Data Type   | Constraints         | Description                                                                     |
| :----------------- | :---------- | :------------------ | :------------------------------------------------------------------------------ |
| `crypto_id`        | SERIAL      | PRIMARY KEY         | Unique identifier for the cryptocurrency.                                       |
| `symbol`           | VARCHAR(10) | UNIQUE, NOT NULL    | The trading symbol of the cryptocurrency (e.g., "USDT", "BTC").                   |
| `name`             | VARCHAR(100)| NOT NULL            | Full name of the cryptocurrency (e.g., "Tether", "Bitcoin").                    |
| `binance_asset_code`| VARCHAR(20) | NOT NULL            | Binance-specific asset code for the cryptocurrency.                             |
| `is_active`        | BOOLEAN     | DEFAULT TRUE        | Indicates if the cryptocurrency is currently active.                            |
| `created_at`       | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Timestamp when the record was created.                                          |
| `updated_at`       | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Timestamp when the record was last updated.                                     |

**Indexes:**
*   `idx_crypto_symbol` on `symbol`

### `dim_fiat_currencies`

Stores information about fiat currencies.

| Column Name        | Data Type   | Constraints         | Description                                                                     |
| :----------------- | :---------- | :------------------ | :------------------------------------------------------------------------------ |
| `fiat_id`          | SERIAL      | PRIMARY KEY         | Unique identifier for the fiat currency.                                        |
| `currency_code`    | CHAR(3)     | UNIQUE, NOT NULL    | ISO 4217 currency code (e.g., "VES", "USD").                                    |
| `currency_name`    | VARCHAR(100)| NOT NULL            | Full name of the fiat currency (e.g., "Venezuelan Bolívar", "United States Dollar").|
| `country_code`     | CHAR(2)     |                     | ISO 3166-1 alpha-2 country code (e.g., "VE", "US").                             |
| `is_active`        | BOOLEAN     | DEFAULT TRUE        | Indicates if the fiat currency is currently active.                             |
| `created_at`       | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Timestamp when the record was created.                                          |
| `updated_at`       | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Timestamp when the record was last updated.                                     |

**Indexes:**
*   `idx_fiat_code` on `currency_code`

### `dim_payment_methods`

Stores information about payment methods.

| Column Name        | Data Type   | Constraints         | Description                                                                     |
| :----------------- | :---------- | :------------------ | :------------------------------------------------------------------------------ |
| `payment_method_id`| SERIAL      | PRIMARY KEY         | Unique identifier for the payment method.                                       |
| `method_code`      | VARCHAR(50) | UNIQUE, NOT NULL    | A unique code for the payment method (e.g., "Mercantil", "BankTransfer").       |
| `method_name`      | VARCHAR(200)| NOT NULL            | Display name of the payment method.                                             |
| `category`         | VARCHAR(50) |                     | Category of the payment method (e.g., 'bank_transfer', 'e_wallet', 'cash').     |
| `description`      | TEXT        |                     | Optional description of the payment method.                                     |
| `is_active`        | BOOLEAN     | DEFAULT TRUE        | Indicates if the payment method is currently active.                            |
| `created_at`       | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Timestamp when the record was created.                                          |

**Indexes:**
*   `idx_payment_method_code` on `method_code`
*   `idx_payment_category` on `category`

### `dim_advertisers`

Stores information about advertisers. This table employs a Type 2 Slowly Changing Dimension (SCD Type 2) strategy to track changes in advertiser attributes over time, preserving historical data.

| Column Name        | Data Type   | Constraints         | Description                                                                     |
| :----------------- | :---------- | :------------------ | :------------------------------------------------------------------------------ |
| `advertiser_sk`    | BIGSERIAL   | PRIMARY KEY         | Surrogate key, unique identifier for each version of an advertiser's record.    |
| `advertiser_id`    | VARCHAR(100)| NOT NULL            | The external unique identifier for the advertiser from Binance.                 |
| `nickname`         | VARCHAR(200)| NOT NULL            | The advertiser's nickname on the platform.                                      |
| `is_merchant`      | BOOLEAN     | DEFAULT FALSE       | Indicates if the advertiser is a verified merchant.                             |
| `registration_days`| INTEGER     |                     | Number of days since the advertiser registered.                                 |
| `effective_date`   | TIMESTAMP   | NOT NULL            | The date from which this version of the advertiser record is valid.             |
| `expiration_date`  | TIMESTAMP   |                     | The date until which this version of the advertiser record is valid (NULL if current).|
| `is_current`       | BOOLEAN     | DEFAULT TRUE        | Flag indicating if this is the currently active record for the advertiser.      |
| `created_at`       | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP | Timestamp when this specific record was created in the database.                |

**Indexes:**
*   `idx_advertiser_id_current` on `advertiser_id`, `is_current` (for efficient lookup of current records).
*   `idx_advertiser_nickname` on `nickname`

## Fact Tables

Fact tables store the measurable events or metrics (facts) of the P2P trading process. They typically contain foreign keys to dimension tables and numerical measures.

### `fact_offers`

The central fact table, storing snapshots of P2P offers at various extraction times.

| Column Name               | Data Type    | Constraints                             | Description                                                                     |
| :------------------------ | :----------- | :-------------------------------------- | :------------------------------------------------------------------------------ |
| `offer_id`                | BIGSERIAL    | PART OF PRIMARY KEY                   | Surrogate key, unique identifier for the offer snapshot.                        |
| `offer_external_id`       | VARCHAR(100) | NOT NULL                                | The unique identifier for the offer from the Binance API (`advNo`).             |
| `batch_id`                | UUID         | NOT NULL                                | Identifier for the extraction batch this offer belongs to.                      |
| `extraction_timestamp`    | TIMESTAMP    | PART OF PRIMARY KEY, NOT NULL           | Timestamp when this offer snapshot was extracted.                               |
| `crypto_id`               | INTEGER      | FOREIGN KEY (`dim_cryptocurrencies`)    | Foreign key to `dim_cryptocurrencies` table.                                    |
| `fiat_id`                 | INTEGER      | FOREIGN KEY (`dim_fiat_currencies`)     | Foreign key to `dim_fiat_currencies` table.                                     |
| `advertiser_sk`           | BIGINT       | FOREIGN KEY (`dim_advertisers`)         | Foreign key to `dim_advertisers` table (SCD Type 2 surrogate key).              |
| `trade_type`              | VARCHAR(4)   | NOT NULL, CHECK ('BUY', 'SELL')         | Type of trade (BUY or SELL).                                                    |
| `price`                   | NUMERIC(20,8)| NOT NULL                                | The price of the cryptocurrency in fiat currency.                               |
| `price_float_rate`        | NUMERIC(10,4)|                                         | Premium/discount rate relative to a market price (if available from API).       |
| `available_amount`        | NUMERIC(20,8)| NOT NULL                                | The total amount of crypto available for this offer.                            |
| `min_limit`               | NUMERIC(20,8)| NOT NULL                                | Minimum single transaction amount in fiat currency.                             |
| `max_limit`               | NUMERIC(20,8)| NOT NULL                                | Maximum single transaction amount in fiat currency.                             |
| `tradable_quantity`       | NUMERIC(20,8)|                                         | Quantity that can be traded.                                                    |
| `completion_rate`         | NUMERIC(5,2) |                                         | Advertiser's completion rate (denormalized for performance).                    |
| `total_orders_count`      | INTEGER      |                                         | Total number of orders for the advertiser (denormalized).                       |
| `avg_response_time_seconds`| INTEGER     |                                         | Average response time of the advertiser (denormalized).                         |
| `avg_completion_time_minutes`| INTEGER   |                                         | Average completion time of the advertiser (denormalized).                       |
| `terms_conditions`        | TEXT         |                                         | Any specific terms and conditions for the offer.                                |
| `is_available`            | BOOLEAN      | DEFAULT TRUE                            | Indicates if the offer was available at the time of extraction.                 |
| `created_at`              | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP               | Timestamp when this specific record was created in the database.                |

**Primary Key:** (`offer_id`, `extraction_timestamp`) - This composite key allows for tracking offer changes over time for a given external offer ID.

**Foreign Keys:**
*   `crypto_id` REFERENCES `dim_cryptocurrencies(crypto_id)`
*   `fiat_id` REFERENCES `dim_fiat_currencies(fiat_id)`
*   `advertiser_sk` REFERENCES `dim_advertisers(advertiser_sk)`

**Indexes:**
*   `idx_offers_batch` on `batch_id`
*   `idx_offers_timestamp` on `extraction_timestamp` (using `brin` for time-series queries)
*   `idx_offers_crypto_fiat` on `crypto_id`, `fiat_id`, `trade_type`
*   `idx_offers_advertiser` on `advertiser_sk`

### `fact_offer_payment_methods`

A bridge table linking `fact_offers` to `dim_payment_methods`, allowing for multiple payment methods per offer.

| Column Name            | Data Type   | Constraints                             | Description                                                                     |
| :--------------------- | :---------- | :-------------------------------------- | :------------------------------------------------------------------------------ |
| `offer_payment_id`     | BIGSERIAL   | PRIMARY KEY                             | Unique identifier for this payment method association.                          |
| `offer_id`             | BIGINT      | PART OF FOREIGN KEY, NOT NULL           | References `offer_id` from `fact_offers`.                                       |
| `extraction_timestamp` | TIMESTAMP   | PART OF FOREIGN KEY, NOT NULL           | References `extraction_timestamp` from `fact_offers`.                           |
| `payment_method_id`    | INTEGER     | FOREIGN KEY (`dim_payment_methods`)     | Foreign key to `dim_payment_methods` table.                                     |
| `is_primary`           | BOOLEAN     | DEFAULT FALSE                           | Indicates if this is considered the primary payment method for the offer (if applicable).|

**Foreign Keys:**
*   Composite Foreign Key (`offer_id`, `extraction_timestamp`) REFERENCES `fact_offers(offer_id`, `extraction_timestamp)` ON DELETE CASCADE

**Indexes:**
*   `idx_offer_payments` on `offer_id`, `extraction_timestamp`
*   `idx_payment_offers` on `payment_method_id`

## Mapping to FastAPI and MCP Data Models

The defined database schema provides a direct foundation for creating FastAPI endpoints and corresponding Model Context Protocol (MCP) data models. Each dimension table can directly map to an MCP model (e.g., `dim_cryptocurrencies` to `Cryptocurrency` MCP model), and the `fact_offers` table will be the basis for the `Offer` MCP model.

For example:

*   **MCP `Cryptocurrency` Model:** Would expose `crypto_id`, `symbol`, `name`, `binance_asset_code`, `is_active`.
*   **MCP `FiatCurrency` Model:** Would expose `fiat_id`, `currency_code`, `currency_name`, `country_code`, `is_active`.
*   **MCP `Advertiser` Model:** Would primarily expose the *current* `advertiser_id`, `nickname`, `is_merchant`, `registration_days` from the `dim_advertisers` table (filtered by `is_current=TRUE`). Historical attributes would be accessible for analytical purposes if needed.
*   **MCP `Offer` Model:** Would combine attributes from `fact_offers` with relevant details from linked dimension tables (`dim_cryptocurrencies`, `dim_fiat_currencies`, `dim_advertisers`, `dim_payment_methods`). This model would encapsulate the full context of a P2P offer.

This structured schema ensures that the data is readily available and well-defined for consumption by an API, facilitating consistent data interaction and AI tooling integration.

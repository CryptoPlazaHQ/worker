# Binance P2P Data Ingestion Worker Documentation

## Introduction

This document provides a comprehensive guide to the Binance P2P data ingestion worker, explaining its architecture, configuration, data extraction process, data loading process, and how to extend and scale the worker. This worker is designed to extract trading data from the Binance P2P API and load it into a PostgreSQL database for analysis and monetization.

We will use the analogy of building a mining worker that extracts valuable resources (data) for profit.

## The Mining Worker Analogy

Think of this data ingestion worker as a mining operation. We are extracting valuable resources (data) from the Binance P2P API and processing them to generate profit.

*   **The Mining Rig (Data Ingestion Worker):** This is the software that extracts the data from the Binance P2P API.
*   **The Resources (Data):** This is the raw data extracted from the Binance P2P API, such as offer prices, available amounts, and payment methods.
*   **The Processing Plant (Data Loading Process):** This is the process of cleaning, transforming, and loading the data into the PostgreSQL database.
*   **The Gold (Valuable Insights):** This is the valuable insights that can be derived from the data, such as arbitrage opportunities, market trends, and advertiser performance.
*   **The Profit (Monetization):** This is the profit that can be generated from the valuable insights, such as through internal use, data sharing, or other monetization strategies.

## Architecture

The worker consists of the following main components:

*   **Configuration (worker/config.py):** Reads configuration settings from environment variables and the `p2p_config.json` file.
*   **Extraction (worker/extractor.py):** Extracts data from the Binance P2P API.
*   **Loading (worker/loader.py):** Loads the extracted data into the PostgreSQL database.
*   **Database (schema.sql):** Defines the database schema.

## Database Schema

The database schema consists of the following tables:

*   **Dimensions:**
    *   `dim_cryptocurrencies`: Stores information about cryptocurrencies (symbol, name, binance_asset_code).
    *   `dim_fiat_currencies`: Stores information about fiat currencies (currency_code, currency_name, country_code).
    *   `dim_payment_methods`: Stores information about payment methods (method_code, method_name, category).
    *   `dim_advertisers`: Stores information about advertisers (advertiser_id, nickname). This table uses SCD Type 2 to track changes over time.
*   **Facts:**
    *   `fact_offers`: Stores information about offers (price, available_amount, min_limit, max_limit). This is the main fact table.
    *   `fact_offer_payment_methods`: A bridge table that links offers to payment methods.

## Configuration

The worker is configured using environment variables and the `p2p_config.json` file.

### Environment Variables

The following environment variables are used to configure the worker:

*   `WORKER_DATABASE_URL`: The URL of the PostgreSQL database.
*   `WORKER_RATE_LIMIT_REQUESTS_PER_MINUTE`: The number of requests per minute allowed by the rate limiter.
*   `WORKER_EXTRACTION_INTERVAL_MINUTES`: The interval in minutes between data extraction runs.
*   `WORKER_MAX_WORKERS`: The maximum number of worker threads to use for parallel extraction.
*   `WORKER_LOG_LEVEL`: The log level for the worker.

### p2p\_config.json

The `p2p_config.json` file contains configuration settings specific to the Binance P2P API. It defines the fiat currencies and cryptocurrencies to extract data for, as well as other settings such as the maximum number of pages to extract per trading pair.

## Data Extraction

The `worker/extractor.py` file is responsible for extracting data from the Binance P2P API.

### BinanceP2PExtractor Class

The `BinanceP2PExtractor` class handles the data extraction process.

*   `get_all_trading_pairs()`: Generates a list of trading pairs based on the `p2p_config.json` file.
*   `extract_pair_offers()`: Extracts offers for a specific trading pair.
*   `extract_all_offers()`: Extracts offers for all trading pairs in parallel using a `ThreadPoolExecutor`.
*   `_parse_offer()`: Parses the raw offer data and extracts relevant information.

## Data Loading

The `worker/loader.py` file is responsible for loading the extracted data into the PostgreSQL database.

### DataLoader Class

The `DataLoader` class handles the data loading process.

*   `load_offers()`: Processes and loads a batch of offers into the database.
*   `_get_or_create()`: Generic get-or-create function for dimension tables.
*   `_load_dimensions()`: Pre-loads all dimensions to leverage caching.
*   `_load_facts()`: Loads the fact records into the database.

## Adding More Fiat Currencies

To add a new fiat currency, you need to modify the `p2p_config.json` file.

1.  Add the currency code to the `"FIATS"` array.
2.  Add a new entry to the `"CRYPTOS_BY_FIAT"` dictionary, where the key is the currency code and the value is an array of supported cryptocurrencies.
3.  Add a new entry to the `"PAYMENT_METHODS_BY_FIAT"` dictionary, where the key is the currency code and the value is an array of supported payment methods.

**Note:** The currency code must be a valid ISO 4217 currency code.

## Scaling Data Ingestion

To scale data ingestion, you can adjust the following parameters:

*   `WORKER_MAX_WORKERS`: This environment variable controls the maximum number of worker threads used for parallel extraction. Increasing this value will increase the number of parallel requests to the Binance P2P API, which can improve the data ingestion rate. However, it is important to consider the rate limits imposed by the Binance P2P API.
*   `BINANCE_P2P_UNTIL_PAGE`: This setting in the `p2p_config.json` file controls the maximum number of pages to extract per trading pair. Increasing this value will increase the amount of data extracted per trading pair, but it will also increase the extraction time.
*   `WORKER_RATE_LIMIT_REQUESTS_PER_MINUTE`: This environment variable controls the number of requests per minute allowed by the rate limiter. Increasing this value will allow more requests to the Binance P2P API, which can improve the data ingestion rate. However, it is important to consider the rate limits imposed by the Binance P2P API.

## API and MCP Proposal for Database Interaction

To enable interaction with the database for dashboards and other applications, we propose creating an API and using the Model Context Protocol (MCP).

### API Endpoints

The API should provide the following endpoints:

*   `/offers`: Returns a list of offers, with filtering and pagination options.
*   `/advertisers`: Returns a list of advertisers, with filtering and pagination options.
*   `/cryptocurrencies`: Returns a list of cryptocurrencies.
*   `/fiat_currencies`: Returns a list of fiat currencies.
*   `/payment_methods`: Returns a list of payment methods.

### MCP (Model Context Protocol)

The API should use the following MCP data models:

*   `Offer`: Represents an offer, with fields such as price, available_amount, min_limit, max_limit, etc.
*   `Advertiser`: Represents an advertiser, with fields such as advertiser_id, nickname, etc.
*   `Cryptocurrency`: Represents a cryptocurrency, with fields such as symbol, name, binance_asset_code, etc.
*   `FiatCurrency`: Represents a fiat currency, with fields such as currency_code, currency_name, country_code, etc.
*   `PaymentMethod`: Represents a payment method, with fields such as method_code, method_name, category, etc.

MCP would be used to define the data models used by the API. This would ensure that the data is consistent and well-defined, making it easier for applications to consume the data.

## Chatting with Data Extraction for Arbitrage Opportunities

To enable chatting with data extraction for arbitrage opportunities, we can use a combination of the API and a natural language processing (NLP) model.

To enable chatting with data extraction for arbitrage opportunities, you can use a combination of the API and a natural language processing (NLP) model.

1.  **User Input:** The user provides a chat message describing the desired arbitrage opportunity (e.g., "Find arbitrage opportunities for BTC/USD").
2.  **NLP Processing:** The NLP model processes the chat message and extracts the relevant information, such as the cryptocurrency pair (BTC/USD) and the desired action (find arbitrage opportunities).
3.  **API Query:** The extracted information is used to query the API for the relevant data. For example, the API might be queried for the current prices of BTC/USD on different exchanges.
4.  **Arbitrage Calculation:** The data from the API is used to calculate potential arbitrage opportunities.
5.  **Response Generation:** The results are returned to the user in a natural language format, describing the potential arbitrage opportunities and the steps required to take advantage of them.
# P2P Dashboard Data API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A unified, high-performance FastAPI for querying P2P cryptocurrency trading data from a worker-populated dimensional PostgreSQL database. This API serves as the Phase II data access layer, providing structured and secure access to the wealth of data ingested by the independent data worker.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Docker Usage](#docker-usage)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

-   **Dimensional Data Access:** Query rich, historical P2P trading data organized in a dimensional model (facts and dimensions).
-   **Comprehensive Filtering & Pagination:** Access offers, advertisers, and core dimensions with advanced filtering, pagination, and sorting capabilities.
-   **MCP-Aligned Models:** Data exposed via Pydantic models (acting as Model Context Protocol - MCP) for consistent consumption by analytics tools and AI/ML applications.
-   **Secure Access:** Protect your API with robust API key authentication.
-   **Containerized Deployment:** Ready for deployment using Docker for consistent environments.
-   **Scalable Architecture:** Designed for high performance and scalability as a read-only interface.

## Getting Started

This API connects to the PostgreSQL database populated by the independent `worker/` application. Ensure your worker is running and populating the database before starting this API.

For detailed instructions on local installation, environment setup, configuration, running the API server, and generating API keys, please refer to the comprehensive guide: [**`Api/howto_run.md`**](./howto_run.md)

### Key Prerequisites (Summary)

*   **Python 3.12** installed on your system.
*   **Git** installed.
*   **Docker** (optional, for containerized deployment).
*   **PostgreSQL Database:** The same database instance that the `worker/` application is feeding.
*   **`.env` file:** Located in the **project root directory** (`dashboards/`). This file must contain `API_DATABASE_URL` (for the database connection) and `API_KEY` (your Internal API Admin Key).

### Local Installation & Running the API

Please follow the detailed steps in [**`Api/howto_run.md`**](./howto_run.md).

### Docker Usage

Alternatively, you can build and run the application using Docker for a containerized environment.

1.  **Navigate to the `Api` directory:**

    ```bash
    cd Api
    ```

2.  **Build the Docker image:**

    ```bash
    docker build -t p2p-dashboard-data-api .
    ```

3.  **Run the Docker container:**

    Ensure your `.env` file (in the project root) is correctly configured with your `API_DATABASE_URL` and `API_KEY`. You will need to mount this file into the container.

    ```bash
    docker run -d --name p2p-dashboard-api -p 8000:8000 --env-file ../.env p2p-dashboard-data-api
    ```

    -   `-d`: Runs the container in detached mode (in the background).
    -   `--name p2p-dashboard-api`: Assigns a name to your container for easy reference.
    -   `-p 8000:8000`: Maps port 8000 on your host to port 8000 in the container.
    -   `--env-file ../.env`: Mounts the `.env` file from the **parent directory** (project root) into the container to provide environment variables.

## Usage

For comprehensive instructions on how to run the API locally or via Docker, please refer to the detailed guide: [**`Api/howto_run.md`**](./howto_run.md)

Once running, the API will be available at `http://127.0.0.1:8000`.

You can view the auto-generated interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## API Endpoints

All data endpoints require a **Client-Facing API Key** for authentication, sent via the `X-API-Key` header. For instructions on how to generate these client keys, please refer to Section 6 of [**`Api/howto_run.md`**](./howto_run.md).

### 1. Offers Endpoints

#### `GET /api/v1/offers`

*   **Description:** Retrieves a paginated and filterable list of P2P offers from the dimensional database.
*   **Query Parameters:**
    *   `fiat_code` (string, optional): Filter by fiat currency code (e.g., `ARS`).
    *   `crypto_symbol` (string, optional): Filter by cryptocurrency symbol (e.g., `USDT`).
    *   `trade_type` (string, optional): Filter by trade type (`BUY` or `SELL`).
    *   `min_price` (number, optional): Filter offers with price greater than or equal to this value.
    *   `max_price` (number, optional): Filter offers with price less than or equal to this value.
    *   `advertiser_id` (string, optional): Filter by external Binance advertiser ID.
    *   `payment_method_code` (string, optional): Filter by payment method code (e.g., `Mercadopago`).
    *   `page` (integer, optional, default: 1): Page number (starting from 1).
    *   `page_size` (integer, optional, default: 100, max: 1000): Number of items per page.
    *   `sort_by` (string, optional, default: `extraction_timestamp`): Field to sort by (e.g., `price`, `extraction_timestamp`).
    *   `sort_order` (string, optional, default: `desc`): Sort order (`asc` or `desc`).
*   **Headers:** `X-API-Key: your_api_key`

#### `GET /api/v1/offers/{offer_external_id}`

*   **Description:** Retrieves a single offer by its external Binance ID (`offer_external_id`).
*   **Path Parameters:** `offer_external_id` (string, required)
*   **Headers:** `X-API-Key: your_api_key`

### 2. Advertisers Endpoints

#### `GET /api/v1/advertisers`

*   **Description:** Retrieves a paginated and filterable list of current P2P advertisers.
*   **Query Parameters:**
    *   `nickname` (string, optional): Filter by advertiser nickname (partial match).
    *   `is_merchant` (boolean, optional): Filter by merchant status.
    *   `page` (integer, optional, default: 1)
    *   `page_size` (integer, optional, default: 100, max: 1000)
*   **Headers:** `X-API-Key: your_api_key`

#### `GET /api/v1/advertisers/{advertiser_id}`

*   **Description:** Retrieves a specific current advertiser by their external Binance ID.
*   **Path Parameters:** `advertiser_id` (string, required)
*   **Headers:** `X-API-Key: your_api_key`

### 3. Dimensional Data Endpoints

#### `GET /api/v1/cryptocurrencies`

*   **Description:** Retrieves a paginated list of supported cryptocurrencies.
*   **Query Parameters:** `page`, `page_size`
*   **Headers:** `X-API-Key: your_api_key`

#### `GET /api/v1/fiat_currencies`

*   **Description:** Retrieves a paginated list of supported fiat currencies.
*   **Query Parameters:** `page`, `page_size`
*   **Headers:** `X-API-Key: your_api_key`

#### `GET /api/v1/payment_methods`

*   **Description:** Retrieves a paginated list of supported payment methods.
*   **Query Parameters:** `page`, `page_size`
*   **Headers:** `X-API-Key: your_api_key`

## Testing

To run the tests for this API application (assuming the test suite has been updated to reflect the new functionality):

```bash
python -m pytest
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

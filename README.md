# P2P Data Ingestion Worker

## Introduction

This document provides instructions on how to deploy and run the P2P data ingestion worker. The worker extracts data from Binance P2P and loads it into a PostgreSQL database.

## Prerequisites

- Python 3.12
- PostgreSQL database
- `.venv` virtual environment
- Required Python packages (see `requirements.txt`)

## Deployment

### 1. Clone the repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Setup and Activate Python Virtual Environment

Create and activate a Python 3.12 virtual environment from the **project root directory**:

```bash
# Ensure you are in the project root: C:\Users\DELL\Desktop\dashboards
py -3.12 -m venv .venv

# On Windows:
.\\.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```
(Your terminal prompt should now show `(.venv)` at the beginning, indicating the environment is active.)

## 3. Install Dependencies

With the virtual environment active, install all required Python packages for both the worker and API:

```bash
# Ensure you are in the project root: C:\Users\DELL\Desktop\dashboards
pip install -r requirements.txt
pip install -r Api/requirements.txt
```

### 5. Configure the worker

Create a `.env` file in the root directory with the following variables:

```env
# Database
WORKER_DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>

# Rate Limiting
WORKER_RATE_LIMIT_REQUESTS_PER_MINUTE=100

# Extraction
WORKER_EXTRACTION_INTERVAL_MINUTES=10
WORKER_MAX_WORKERS=20

# Monitoring
WORKER_LOG_LEVEL=INFO
```

Replace the placeholders with your actual values.



## 6. Run the Worker (and Initial Database Setup)

The worker needs the database schema to be created before it can operate. The `run_api.py` script (located in the project root) is responsible for this initial database schema creation for all models.

First, ensure the database schema is initialized by running the API startup script *once*:

```bash
# Ensure you are in the project root: C:\Users\DELL\Desktop\dashboards
python run_api.py
# You can stop this process after it logs "Checking and creating tables if they don't exist..." and no errors occur.
# Or, keep it running in a separate terminal if you intend to use the API.
```

Once the database schema is created (or if the API is already running), you can start the worker:

```bash
# Ensure your virtual environment is active and you are in the project root
python -m worker.main
```

The worker will start extracting data from Binance P2P and loading it into the PostgreSQL database.

## 7. Monitoring

The worker exposes Prometheus metrics on port 9090. You can use Prometheus to monitor the worker's performance.

## 8. Logging

The worker uses the logging module to log events. The log level can be configured using the `WORKER_LOG_LEVEL` environment variable.

## 9. Contributing

Contributions are welcome! Please submit a pull request with your changes.
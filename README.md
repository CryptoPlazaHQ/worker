# P2P Financial Data Platform

## 1. Project Overview

This project is a comprehensive platform for collecting, storing, and analyzing peer-to-peer (P2P) financial data. It consists of three main components:

- **P2P Data Ingestion Worker**: A robust worker responsible for extracting P2P data from external sources (e.g., Binance) and loading it into a central PostgreSQL database.
- **FastAPI Backend (API)**: A powerful API built with FastAPI that serves the collected data, provides endpoints for data analysis, and handles user authentication.
- **Streamlit Dashboard**: An interactive web application built with Streamlit that allows users to visualize data, explore API endpoints, and monitor platform activity.

The project is designed to be modular and scalable, allowing for the easy addition of new data sources, API endpoints, and dashboard features.

## 2. Prerequisites

- Python 3.12
- PostgreSQL database
- A Python virtual environment (e.g., `.venv`)

## 3. Setup and Installation

### 3.1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 3.2. Setup and Activate Python Virtual Environment

Create and activate a Python 3.12 virtual environment from the project's root directory:

```bash
# Ensure you are in the project root (e.g., C:\Users\DELL\Desktop\dashboards)
py -3.12 -m venv .venv

# Activate the environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```
Your terminal prompt should now be prefixed with `(.venv)`, indicating that the virtual environment is active.

### 3.3. Install Dependencies

With the virtual environment active, install all required Python packages for the worker, API, and Streamlit app:

```bash
# Ensure you are in the project root
pip install -r requirements.txt
pip install -r Api/requirements.txt
pip install -r streamlit_app/requirements.txt
```

### 3.4. Configure Environment Variables

Create a `.env` file in the project's root directory by copying the template:

```bash
cp .env.template .env
```

Now, edit the `.env` file and provide the necessary configuration values, such as your database connection URL and other sensitive settings:

```env
# Database
WORKER_DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>

# API Secret Key (important for security)
SECRET_KEY=your_super_secret_key_here

# Rate Limiting
WORKER_RATE_LIMIT_REQUESTS_PER_MINUTE=100

# Extraction
WORKER_EXTRACTION_INTERVAL_MINUTES=10
WORKER_MAX_WORKERS=20

# Monitoring
WORKER_LOG_LEVEL=INFO
```

## 4. Running the Platform

This platform consists of three services that can be run independently: the API, the Worker, and the Streamlit Dashboard.

### 4.1. Initialize the Database and Run the API

The FastAPI application is the primary entry point for initializing the database schema and running the backend services.

To start the API, run the following command from the project root:

```bash
# This will start the FastAPI server and automatically create database tables
python run_api.py
```

The API will be accessible at `http://127.0.0.1:8000`, and the interactive API documentation (Swagger UI) can be found at `http://127.0.0.1:8000/docs`.

**Note**: The first time you run this command, it will create all the necessary tables in the database. You can keep this process running in a terminal to serve API requests.

### 4.2. Run the P2P Data Ingestion Worker

Once the database is initialized and the API is running, you can start the data ingestion worker. The worker will continuously extract data from P2P platforms and store it in the database.

Open a **new terminal**, activate the virtual environment, and run the following command:

```bash
# Ensure your virtual environment is active
python -m worker.main
```

The worker will now run in the background, populating the database with fresh data.

### 4.3. Run the Streamlit Dashboard

To explore the data and interact with the platform, you can use the Streamlit dashboard.

Open another **new terminal**, activate the virtual environment, and run the following command:

```bash
# Ensure your virtual environment is active and you are in the project root
streamlit run streamlit_app/app.py
```

The Streamlit application will be available at the local URL displayed in your terminal (usually `http://localhost:8501`).

## 5. Monitoring and Logging

- **API**: The FastAPI backend provides structured logging. Check the terminal where the API is running for real-time logs.
- **Worker**: The worker uses Prometheus for metrics, which are exposed on port 9090. You can configure a Prometheus instance to scrape these metrics for monitoring. The worker's log level can be set via the `WORKER_LOG_LEVEL` environment variable.

## 6. Contributing

Contributions are welcome! Please create a feature branch, make your changes, and submit a pull request. We appreciate your help in making this platform better.
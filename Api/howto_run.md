# How to Run the P2P Dashboard Data API Locally

This guide provides a step-by-step walkthrough for setting up and running the P2P Dashboard Data API on your local machine. This API acts as the Phase II data access layer, connecting to the PostgreSQL database populated by the independent data ingestion `worker/` application.

## 1. Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.10+** installed.
*   **Git** installed.
*   **Docker** (optional, for containerized deployment).
*   **PostgreSQL Database:** A running PostgreSQL instance that is actively being populated by the `worker/` application. This API will connect to this same database.
*   **API Key:** A valid API key for authentication. This key needs to be stored in the database's `api_keys` table (managed via the API's admin endpoints once it's running).

## 2. Setting up the Environment

1.  **Clone the Project:** If you haven't already, clone the main project repository.
    ```bash
    git clone https://github.com/CryptoPlazaHQ/worker.git # Or your specific repo
    cd worker # Navigate to the project root
    ```

2.  **Navigate to the API Directory:**
    ```bash
    cd Api
    ```

3.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```
    Your terminal prompt should now start with `(.venv)`.

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 3. Configuration

The API requires environment variables for database connection and API key management. These should be placed in an `.env` file located in the **project's root directory** (i.e., `dashboards/.env`, which is one level up from the `Api/` folder).

1.  **Create/Edit the `.env` file:** In the root of your main project directory (e.g., `dashboards/`), create a file named `.env` if it doesn't exist.

2.  **Add Configuration Variables:**
    *   `API_DATABASE_URL`: The connection string for your PostgreSQL database. This *must* be the same database that your `worker/` application is feeding.
    *   `API_KEY`: The API key that the API itself will use for its admin operations (e.g., creating users, generating new keys). **This is NOT the key used by clients to access data endpoints.**

    Your `.env` file should look something like this:
    ```dotenv
    # Located at dashboards/.env
    API_DATABASE_URL="postgresql://user:password@host:port/your_database_name"
    API_KEY="a_strong_random_key_for_internal_api_admin_ops"
    ```
    > **Note:** Replace `user`, `password`, `host`, `port`, `your_database_name` with your actual PostgreSQL credentials. The `API_KEY` can be any strong random string.

## 4. Database Initialization (Admin Setup)

The API needs to manage users and API keys within its connected database. This typically requires running migrations or ensuring the `users` and `api_keys` tables exist.

1.  **Ensure Database Schema is Up-to-Date:** This API now connects to the worker's database. The worker should have initialized the base schema (`dim_` and `fact_` tables). However, the `users` and `api_keys` tables (and `runs` table) are now part of the shared schema (from `worker/models.py`). You might need to run Alembic migrations *from this API project* if these specific tables are not yet present in your worker's database.

    *   **Initial Setup (if `users`, `api_keys`, `runs` tables are missing):**
        ```bash
        # Ensure you are in the Api/ directory and virtual environment is active
        alembic upgrade head
        ```
        > **Warning:** Be cautious when running migrations. Ensure your database is backed up if you are unsure. If the worker's database already has these tables from a previous API setup or manual creation, `alembic upgrade head` might not be necessary or could error if tables exist.

2.  **Generate an initial API Admin Key:** For clients to access the API's data endpoints, you need to create a user and generate an API key. This is done via the API's own `/admin` endpoints.
    *   First, start the API (see Section 5).
    *   Access the Swagger UI at `http://127.0.0.1:8000/docs`.
    *   **Use the `API_KEY` from your `.env` as the `X-API-Key` to authorize yourself for admin operations.** This `API_KEY` allows you to create users and generate client-facing API keys.
    *   Find the "Admin" section and expand `POST /admin/users/`. Create an admin user.
    *   Log in via `POST /admin/token` with the admin user credentials to get a JWT `access_token`.
    *   Use this `access_token` (as a `Bearer` token) to authorize your session in Swagger UI.
    *   Then, use `POST /admin/keys/` to generate client-facing API keys. **This is the key you will provide to your frontend or other data consumers.**

## 5. Running the API Server

1.  **Ensure your virtual environment is active** and you are in the `Api/` directory.
2.  **Run the API:**
    ```bash
    uvicorn p2p_api.main:app --reload
    ```
3.  You should see output indicating the server is running on `http://127.0.0.1:8000`.

The API will now be live and serving data from your worker-populated PostgreSQL database.

## 6. Accessing API Documentation

You can view the auto-generated interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`. This is where you can explore the available endpoints and test them.

## 7. Next Steps (Connecting a Frontend)

If you are running a frontend application (e.g., Streamlit), ensure it's configured to:
*   Point to this API's URL (`http://127.0.0.1:8000`).
*   Use one of the client-facing API keys generated in Section 4.

## 8. Testing

To run the tests for this API application:

```bash
# Ensure you are in the Api/ directory and virtual environment is active
python -m pytest
```

## 9. Troubleshooting

*   **`DATABASE_URL` Error:** Double-check your `.env` file for `API_DATABASE_URL` spelling and connection string format. Ensure your PostgreSQL server is running and accessible.
*   **API Key Authorization Issues:** Verify you are using the correct API key. Remember the `API_KEY` in `.env` is for *admin operations* only; client applications need API keys generated via `/admin/keys`. Ensure the generated client keys are active in the database.
*   **Database Tables Missing:** If `users`, `api_keys`, or `runs` tables are missing, ensure `alembic upgrade head` was run successfully. If dimensional tables are missing, ensure your `worker/` application has run and populated the database.

---
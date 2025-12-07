# How to Run the P2P Dashboard Data API Locally (Beginner's Guide)

This guide provides a clear, step-by-step walkthrough for setting up and running the P2P Dashboard Data API on your local machine.

**IMPORTANT CONTEXT:**

*   **Phase I (Data Worker):** We assume the independent `worker/` application (from the main project) is ALREADY running and successfully populating your PostgreSQL database with P2P trading data. This API will connect to *that very same database* to read the data the worker has collected.
*   **API's Role (Phase II):** This API is purely a **read-only interface** to the data in your PostgreSQL database. It does not perform new data scraping or modify the core dimensional data.
*   **API Key Management:** This API itself has features to manage users and issue API keys for secure access to its data endpoints.

## 1. Prerequisites: What You Need Before You Start

Make sure you have these tools and resources ready:

*   **Python 3.12** installed on your system.
*   **Git** installed.
*   **Docker** (optional, for containerized deployment).
*   **PostgreSQL Database Connection String:** This is the `API_DATABASE_URL` for the database that your `worker/` application is already feeding. You'll need it.
*   **A strong random string** to use as your **Internal API Admin Key**. You can generate one with `python -c "import secrets; print(secrets.token_hex(32))"`.

## 2. Setting up the API's Local Environment

This API operates within the same Python virtual environment established at the **project root**. Ensure you have completed the following steps outlined in the main `README.md` first:

*   **Created and activated a Python 3.12 virtual environment** at the project root.
*   **Installed all core project dependencies** from both `requirements.txt` (root) and `Api/requirements.txt` from the project root.

Once the main project environment is set up and active, navigate into the API directory:

```bash
cd Api
```
(Your terminal prompt should show `(.venv)` and you should be in the `Api/` directory.)

## 3. Configuring the API: The `.env` File (for Internal API Admin Key and DB Connection)

The API needs two crucial pieces of information from you: where to find the database, and a special **Internal API Admin Key** for its own admin tasks. We provide these via an `.env` file.

1.  **Locate/Create the `.env` File:**
    *   This `.env` file **must** be the **same `.env` file** that your `worker/` application is using. It is located in the **root directory of your entire project** (e.g., `C:\Users\DELL\Desktop\dashboards\.env`), *not* inside the `Api` folder.
    *   If you already have a `.env` file for your worker, you will *edit that same file*. If not, create a new one.

2.  **Add Configuration Variables to `.env`:**
    Open the `.env` file and add these two lines, replacing the placeholder values with your actual information:

    ```dotenv
    # Located at C:\Users\DELL\Desktop\dashboards\.env (or your project root)
    API_DATABASE_URL="postgresql://user:password@host:port/your_database_name"
    API_KEY="your_internal_api_admin_key_generated_in_prerequisites"
    ```
    *   **`API_DATABASE_URL`**: This is the connection string to the *same PostgreSQL database* where your data `worker/` is storing its data. Example: `postgresql://p2p_user:strongpassword@localhost:5432/p2p_dashboard`.
    *   **`API_KEY`**: This is your **Internal API Admin Key**. It's a **private key** used by the API itself to secure its own administrative endpoints (like creating new users or issuing client-facing API keys). You should set this to a strong, randomly generated string (e.g., from `python -c "import secrets; print(secrets.token_hex(32))"`). **Keep this key secure and secret!**

## 4. Database Initialization: Creating API Users & Keys Tables

The API needs its own tables for managing users and their API keys (`users`, `api_keys`, and `runs` tables). These tables are defined in `worker/models.py`.

**Important:** The initial creation of these tables, along with all other project tables, is handled automatically when `run_api.py` is executed for the first time. You do **not** need to run `alembic upgrade head` for initial table creation.

Simply running the API server (as described in the next section) will ensure these tables are created if they don't already exist in your database.

*   **Alembic Migrations (for Schema Evolution):** If you are developing and need to apply schema changes (migrations) after the initial setup, you would use Alembic. Ensure your `alembic.ini` is correctly configured to connect to your database. For initial setup, this step is not required.

## 4.1. Creating the Initial Admin User (CLI)

Before you can use the API's administrative features (like generating client API keys), you need to create your first admin user. This is done via a command-line script for security and ease of setup.

1.  **Navigate to the project root:**
    Ensure you are in the project root directory (`C:\Users\DELL\Desktop\dashboards`).
2.  **Run the admin user creation script:**
    ```bash
    # Ensure your virtual environment is active and you are in the project root
    python create_admin_user.py
    ```
    Follow the prompts to enter your desired admin username and a strong password. This script will create the first administrator user in your database.

## 5. Running the API Server

Now you can start the API! The `run_api.py` script (located in the project root) is the single entry point for starting the FastAPI application and will also handle initial database schema creation.

1.  **Navigate to the project root:**
    If you are currently in the `Api/` directory, navigate back to the project root:
    ```bash
    cd ..
    ```
2.  **Start the API Server:**
    ```bash
    # Ensure your virtual environment is active and you are in the project root
    python run_api.py
    ```
3.  You should see output indicating the server is running, typically on `http://127.0.0.1:8000`.

The P2P Dashboard Data API is now live and serving data from your worker-populated PostgreSQL database!

## 6. Accessing API Documentation & Generating Client-Facing API Keys

The API automatically generates interactive documentation (Swagger UI) where you can test endpoints and manage user access. This is also where you will **generate the API Keys that your frontend applications will use.**

1.  **Open API Documentation (Swagger UI):**
    Go to `http://127.0.0.1:8000/docs` in your web browser.

2.  **Authorize Your Swagger UI Session (for Admin Operations):**
    To access administrative endpoints (like generating new client-facing API keys), you need to authorize your Swagger UI session with the admin user credentials you created in **Section 4.1**.
    *   Click the green **"Authorize"** button (usually at the top right).
    *   In the pop-up dialog, locate the `OAuth2PasswordBearer (OAuth2, password)` section.
    *   Enter the `username` and `password` of the admin user you created via `create_admin_user.py`.
    *   Click **"Authorize"** within this section of the dialog.
    *   Click **"Close"** on the pop-up.
    *   The padlock icon next to the main "Authorize" button should now appear "locked," indicating your session is authorized for admin operations.

3.  **Generate a Client-Facing API Key (for your Frontend/Clients):**
    This key is what your frontend or other applications will use to access the data endpoints.
    *   Expand the **"Admin"** section in the Swagger UI.
    *   Find the `POST /admin/keys/` endpoint.
    *   Click "Try it out".
    *   In the "Request body", provide a descriptive `name` for this new API key (e.g., `{"name": "my-frontend-app-key"}`).
    *   Click "Execute".
    *   The response will show your new **Client-Facing API Key** (e.g., `p2p_abcdefgh_ijklmnopqrstuv`). **Copy this entire key IMMEDIATELY! It will NOT be shown again for security reasons.** Save it securely for use in your client applications.

## 7. Next Steps: Connecting a Frontend (Optional)

If you are running a frontend application (e.g., Streamlit, React, etc.), configure it to:

*   Point to this API's base URL (`http://127.0.0.1:8000`).
*   Include the **Client-Facing API Key** (generated in Section 6, Step 5) in the `X-API-Key` header for all requests to data endpoints.

## 8. Testing

To run the tests for this API application:

```bash
# Ensure you are in the Api/ directory and virtual environment is active
python -m pytest
```

## 9. Troubleshooting

*   **`DATABASE_URL` / `API_DATABASE_URL` Error:** Double-check your `.env` file for correct spelling and connection string format. Ensure your PostgreSQL server is running and accessible from where you're running the API.
*   **Internal API Admin Key Authorization Issues:** Verify you are using the correct `API_KEY` from your `.env` file when authorizing for admin operations (Section 6, Step 1).
*   **Client-Facing API Key Authorization Issues:**
    *   Ensure the client-facing API key you're using was generated in Section 6, Step 5.
    *   Remember the format for clients: `X-API-Key: your_generated_client_key`.
    *   Ensure the generated client keys are active in the database.
*   **Database Tables Missing:** The API automatically creates its required tables (`users`, `api_keys`, `runs`) on its first run (Section 5). If these tables are missing after running the API, check the API server logs for database connection errors. `alembic upgrade head` is used for applying *migrations* (schema changes), not for initial table creation. If dimensional tables (`dim_`, `fact_`) are missing, ensure your `worker/` application has run and populated the database.

---
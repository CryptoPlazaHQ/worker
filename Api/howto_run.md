# How to Run the P2P Dashboard Data API Locally (Beginner's Guide)

This guide provides a clear, step-by-step walkthrough for setting up and running the P2P Dashboard Data API on your local machine.

**IMPORTANT CONTEXT:**

*   **Phase I (Data Worker):** We assume the independent `worker/` application (from the main project) is ALREADY running and successfully populating your PostgreSQL database with P2P trading data. This API will connect to *that very same database* to read the data the worker has collected.
*   **API's Role (Phase II):** This API is purely a **read-only interface** to the data in your PostgreSQL database. It does not perform new data scraping or modify the core dimensional data.
*   **API Key Management:** This API itself has features to manage users and issue API keys for secure access to its data endpoints.

## 1. Prerequisites: What You Need Before You Start

Make sure you have these tools and resources ready:

*   **Python 3.10+** installed on your system.
*   **Git** installed.
*   **Docker** (optional, for containerized deployment).
*   **PostgreSQL Database Connection String:** This is the `API_DATABASE_URL` for the database that your `worker/` application is already feeding. You'll need it.
*   **A strong random string** to use as your **Internal API Admin Key**. You can generate one with `python -c "import secrets; print(secrets.token_hex(32))"`.

## 2. Setting up the API's Local Environment

1.  **Navigate to the API Folder:**
    Open your terminal or command prompt and go to the `Api` directory within your main project folder.
    ```bash
    cd /path/to/your/main-project/Api 
    # Example: cd C:\Users\DELL\Desktop\dashboards\Api
    ```

2.  **Create and Activate a Python Virtual Environment:**
    This isolates the API's dependencies.
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```
    (Your terminal prompt should now show `(.venv)` at the beginning, indicating the environment is active.)

3.  **Install Necessary Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```

## 3. Configuring the API: The `.env` File (for Internal API Admin Key and DB Connection)

The API needs two crucial pieces of information from you: where to find the database, and a special **Internal API Admin Key** for its own admin tasks. We provide these via an `.env` file.

1.  **Locate/Create the `.env` File:**
    *   This `.env` file **must** be in the **root directory of your entire project** (e.g., `C:\Users\DELL\Desktop\dashboards\.env`), *not* inside the `Api` folder.
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

## 4. Database Initialization: Setting up API Users & Keys Tables

Even though your worker has created the main data tables (`dim_` and `fact_`), this API needs its *own* tables for managing users and their API keys (`users` and `api_keys` tables).

1.  **Run Database Migrations (if needed):**
    The API uses Alembic for database migrations. If the `users`, `api_keys`, or `runs` tables (which are defined in the shared `worker/models.py`) are not yet in your database, you need to run the migrations for this API project.
    *   **Ensure your virtual environment is active** (`(.venv)` in your terminal prompt) and you are in the `Api/` directory.
    ```bash
    alembic upgrade head
    ```
    > **Note:** If these tables already exist (e.g., from a previous setup or manual creation), this command might indicate "No migrations found" or similar. This is fine. If you encounter errors, ensure your `API_DATABASE_URL` is correct.

## 5. Running the API Server

Now you can start the API!

1.  **Ensure your virtual environment is active** (`(.venv)` in your terminal prompt) and you are in the `Api/` directory.
2.  **Start the API Server:**
    ```bash
    uvicorn p2p_api.main:app --reload
    ```
3.  You should see output indicating the server is running, typically on `http://127.0.0.1:8000`.

The P2P Dashboard Data API is now live and serving data from your worker-populated PostgreSQL database!

## 6. Accessing API Documentation & Generating Client-Facing API Keys

The API automatically generates interactive documentation (Swagger UI) where you can test endpoints and manage user access. This is also where you will **generate the API Keys that your frontend applications will use.**

1.  **Open API Documentation (Swagger UI):**
    Go to `http://127.0.0.1:8000/docs` in your web browser.

2.  **Step 1: Authorize for API Admin Operations (using your Internal API Admin Key)**
    To use the administrative endpoints (like creating users or generating new client-facing API keys), you need to authorize with the **Internal API Admin Key** you set in your `.env` file.
    *   Click the green **"Authorize"** button (usually at the top right).
    *   In the dialog, find the `X-API-Key (apiKey)` section.
    *   Enter the exact value of your `API_KEY` from your project's root `.env` file into the "Value" field.
    *   Click "Authorize" and then "Close".

3.  **Step 2: Create an Admin User (First Time Only):**
    This user will be able to log in and generate client-facing API keys.
    *   Expand the **"Admin"** section in the Swagger UI.
    *   Find the `POST /admin/users/` endpoint.
    *   Click "Try it out".
    *   In the "Request body" (JSON format), enter a username and a strong password for your admin user.
        ```json
        {
          "username": "admin",
          "password": "your_strong_admin_password"
        }
        ```
    *   Click "Execute". A `200` response means the user was created.

4.  **Step 3: Log In as Admin User & Get an Access Token:**
    You'll use this token to authorize yourself for the next step (generating client-facing API keys).
    *   Expand the **"Admin"** section again.
    *   Find the `POST /admin/token` endpoint.
    *   Click "Try it out".
    *   Enter the username and password of the admin user you just created.
    *   Click "Execute".
    *   The response will contain an `access_token` (a long string starting with `eyJ...`). **Copy this entire token string.**

5.  **Step 4: Authorize with the Access Token (for generating client keys):**
    This authorizes your Swagger UI session to generate client-facing API keys on behalf of the admin user.
    *   Click the green **"Authorize"** button again.
    *   In the dialog, in the `Bearer (apiKey)` section, type `Bearer ` (with a space after "Bearer") and then paste the `access_token` you copied.
    *   Click "Authorize" and then "Close".

6.  **Step 5: Generate a Client-Facing API Key (for your Frontend/Clients):**
    This key is what your frontend or other applications will use to access the data endpoints.
    *   Expand the **"Admin"** section.
    *   Find the `POST /admin/keys/` endpoint.
    *   Click "Try it out".
    *   In the "Request body", provide a name for this new API key (e.g., `{"name": "my-frontend-app-key"}`).
    *   Click "Execute".
    *   The response will show your new **Client-Facing API Key** (e.g., `prefix_secret_string`). **Copy this entire key! This is the key you will provide to your frontend or other data consumers.** It will not be shown again!

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
*   **Database Tables Missing:** If `users`, `api_keys`, or `runs` tables are missing, ensure `alembic upgrade head` was run successfully (Section 4.1). If dimensional tables (`dim_`, `fact_`) are missing, ensure your `worker/` application has run and populated the database.

---

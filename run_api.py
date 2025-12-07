import sys
import os
import uvicorn
from dotenv import load_dotenv
from sqlalchemy import create_engine
from worker.models import Base

def init_db(database_url):
    """Initializes the database and creates tables if they don't exist."""
    if not database_url:
        raise ValueError("API_DATABASE_URL not found in environment. Make sure it's set in your .env file.")
    
    print(f"Connecting to database...")
    engine = create_engine(database_url)
    
    print("Checking and creating tables if they don't exist...")
    Base.metadata.create_all(engine)
    print("Database schema is ready.")

def main():
    # Load environment variables from .env file in the project root
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(dotenv_path):
        print(f"Loading environment variables from: {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print(f"Warning: .env file not found at {dotenv_path}. App may not run correctly.")

    # Initialize the database and create tables
    # Note: For the API, we use API_DATABASE_URL, but the tables (worker.models) are shared.
    # This ensures all tables from worker.models are created in the specified database.
    init_db(os.getenv("WORKER_DATABASE_URL"))

    # Add paths for uvicorn to find the app module
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    api_dir = os.path.join(project_root, "Api")
    sys.path.insert(0, api_dir)

    print("Starting API server...")
    uvicorn.run("p2p_api.main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[api_dir])

if __name__ == "__main__":
    main()


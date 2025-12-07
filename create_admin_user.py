"""
Script to create the initial admin user for the P2P Dashboard API.
Run this ONCE during initial setup: python create_admin_user.py
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Add project root to path
# This assumes the script is run from the project root directory (e.g., C:\Users\DELL\Desktop\dashboards)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
api_dir = os.path.join(project_root, "Api")
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

# Load environment variables
dotenv_path = os.path.join(project_root, '.env')
if os.path.exists(dotenv_path):
    print(f"Loading environment variables from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}. Script may not run correctly.")


# Ensure imports from Api.p2p_api work
try:
    from Api.p2p_api.database import init_db
    from Api.p2p_api import crud, schemas
    from Api.p2p_api.auth import get_password_hash
except ImportError as e:
    print(f"ImportError: {e}")
    print("Please ensure you are running this script from the project root directory")
    print("(e.g., C:\\Users\\DELL\\Desktop\\dashboards) and your virtual environment is activated.")
    sys.exit(1)


def create_admin():
    """Creates the initial admin user."""
    db_url = os.getenv("WORKER_DATABASE_URL")
    if not db_url:
        print("ERROR: WORKER_DATABASE_URL not found in .env or environment variables.")
        print("Please ensure your .env file is correctly configured and located in the project root.")
        sys.exit(1)
    
    # Initialize DB (using API's init_db for consistency)
    engine, SessionLocal = init_db(db_url)
    db = SessionLocal()
    
    try:
        # Get credentials from user
        username = input("Enter admin username: ").strip()
        if not username:
            print("Username cannot be empty")
            sys.exit(1)
        
        # Check if user exists
        existing = crud.get_user_by_username(db, username)
        if existing:
            print(f"User '{username}' already exists! Exiting without changes.")
            sys.exit(0) # Exit with 0 if user already exists, as it's not an error

        import getpass
        password = getpass.getpass("Enter admin password: ")
        password_confirm = getpass.getpass("Confirm password: ")
        
        if password != password_confirm:
            print("Passwords do not match!")
            sys.exit(1)
        
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            sys.exit(1)
        
        # Create user
        user_create = schemas.UserCreate(username=username, password=password)
        hashed_password = get_password_hash(password)
        user = crud.create_user(db, user_create, hashed_password)
        
        print(f"\n✅ Admin user '{username}' created successfully!")
        print(f"   User ID: {user.id}")
        print("\nNext steps (after API server is running):")
        print("1. Go to http://127.0.0.1:8000/docs")
        print("2. Use the 'POST /admin/token' endpoint to log in with the username and password you just created.")
        print("3. Copy the 'access_token' from the response.")
        print("4. Click the global 'Authorize' button (top right).")
        print("5. In the 'Bearer Auth (http, bearer)' section, paste the copied 'access_token'. Click 'Authorize', then 'Close'.")
        print("6. Now you can use 'POST /admin/keys/' to generate client API keys, and access all other protected /admin/* endpoints!")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()
        engine.dispose()

if __name__ == "__main__":
    create_admin()

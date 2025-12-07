import uvicorn
import os

def main():
    """
    Main entry point to run the FastAPI application.
    This script is kept for convenience to start the server from the project root.
    All configuration and initialization is handled within the FastAPI app itself.
    """
    # Get the absolute path to the 'Api' directory for uvicorn's reload_dirs
    api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Api")
    
    print("Starting API server...")
    # The application is specified as 'Api.p2p_api.main:app'
    # Uvicorn will look for the 'app' object in 'Api/p2p_api/main.py'
    uvicorn.run("Api.p2p_api.main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[api_dir])

if __name__ == "__main__":
    main()


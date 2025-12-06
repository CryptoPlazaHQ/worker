import sys
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(dotenv_path):
    print(f"Loading .env file from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

def main():
    # Add the project root to the Python path to allow for imports from the 'worker' module
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Add the 'Api' directory to the path so uvicorn can find 'p2p_api'
    api_dir = os.path.join(project_root, "Api")
    sys.path.insert(0, api_dir)

    print("Starting API server...")
    print(f"Project Root: {project_root}")
    print(f"API Directory: {api_dir}")
    
    # Run uvicorn programmatically
    uvicorn.run("p2p_api.main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[api_dir])

if __name__ == "__main__":
    main()

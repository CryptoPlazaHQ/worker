import requests
import os

API_KEY = "p2p_f55d518caf23e92a_z0oRnS74iyrWIyHdx77Q5XdJJTc1GcqzLMsul7XlVJE"
BASE_URL = "http://127.0.0.1:8000" # Assuming the API is running locally

def test_api_connection():
    headers = {
        "X-API-Key": API_KEY
    }
    
    # Test a simple endpoint that doesn't require complex parameters
    endpoint = f"{BASE_URL}/api/v1/cryptocurrencies"
    
    print(f"Attempting to connect to {endpoint} with API Key...")
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        print("API Connection Successful!")
        print("Received data (first 3 items):")
        for item in data[:3]:
            print(f"- {item.get('symbol')}: {item.get('name')}")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        print("Please ensure the FastAPI server is running at http://127.0.0.1:8000")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")

if __name__ == "__main__":
    test_api_connection()

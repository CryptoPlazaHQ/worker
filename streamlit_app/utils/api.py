import requests
import streamlit as st
import logging
from typing import Optional, List, Dict, Any

# Set up logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Use a cached function to prevent re-fetching data on every rerun
@st.cache_data(ttl=300) # Cache for 5 minutes
def cached_api_call(url: str, headers: Dict, params: Dict = None) -> List[Dict[str, Any]]:
    """A cached wrapper for making API GET requests."""
    logger.info(f"Making API call to: {url} with params: {params}")
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        logger.info(f"API call successful, status code: {response.status_code}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - For URL: {url}")
        st.error(f"HTTP error occurred: {http_err} - Check if the API is running and the endpoint is correct.")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error: Could not connect to the API at {url}")
        st.error("Connection error: Could not connect to the API. Is the server running at the specified base URL?")
    except requests.exceptions.Timeout:
        logger.error(f"Request timed out for URL: {url}")
        st.error("Request timed out. The API server may be slow to respond.")
    except requests.exceptions.RequestException as e:
        logger.error(f"An unexpected error occurred for URL: {url}: {e}")
        st.error(f"An unexpected error occurred: {e}")
    return [] # Return empty list on error

class P2PAPIClient:
    """Enhanced API client with caching and error handling."""
    
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:8000"):
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": self.api_key}
    
    def get_offers(
        self,
        fiat_code: Optional[str] = None,
        crypto_symbol: Optional[str] = None,
        trade_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        payment_methods: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch offers with comprehensive filtering."""
        # Build params dict, excluding None values
        params = {
            "fiat_code": fiat_code,
            "crypto_symbol": crypto_symbol,
            "trade_type": trade_type,
            "min_price": min_price,
            "max_price": max_price,
            "payment_methods": payment_methods,
            "page": page,
            "page_size": page_size,
        }
        params = {k: v for k, v in params.items() if v is not None and v != []}
        
        return cached_api_call(
            f"{self.base_url}/api/v1/offers",
            headers=self.headers,
            params=params
        )
    
    def get_cryptocurrencies(self) -> List[Dict[str, Any]]:
        """Fetch available cryptocurrencies."""
        return cached_api_call(
            f"{self.base_url}/api/v1/cryptocurrencies",
            headers=self.headers
        )
    
    def get_fiat_currencies(self) -> List[Dict[str, Any]]:
        """Fetch available fiat currencies."""
        return cached_api_call(
            f"{self.base_url}/api/v1/fiat_currencies", # Corrected endpoint
            headers=self.headers
        )
    
    def get_payment_methods(self) -> List[Dict[str, Any]]:
        """Fetch available payment methods."""
        return cached_api_call(
            f"{self.base_url}/api/v1/payment_methods", # Corrected endpoint
            headers=self.headers
        )

import requests
import logging
from src.config import Config

logger = logging.getLogger(__name__)

def fetch_country_data(country_name: str) -> dict:
    """
    Fetches country data from the REST Countries API.
    Designed to return raw data gracefully or structured error messages.
    """
    url = f"{Config.REST_COUNTRIES_BASE_URL}/{country_name}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Handle 404 (Country not found) gracefully
        if response.status_code == 404:
            return {"error": f"Country '{country_name}' not found in the public database."}
            
        response.raise_for_status()
        data = response.json()
        
        # The API returns a list of matches. We take the first/closest match.
        if data and isinstance(data, list):
            return data[0]
        return {"error": "Unexpected data format received from API."}
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching data for {country_name}")
        return {"error": "The country database is currently taking too long to respond."}
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error for {country_name}: {e}")
        return {"error": "An error occurred while communicating with the country database."}
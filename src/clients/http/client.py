from typing import Dict, Any, Union, Optional
import requests
from requests.exceptions import RequestException


class HTTPError(Exception):
    """Base exception for HTTP client errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class HTTPClient:
    """
    HTTP client for making requests to external services.
    
    Raises:
        HTTPError: If the request fails or returns an error status code
        RequestException: If there's a network or connection error
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, path: str) -> Dict[str, Any]:
        """
        Make a GET request to the specified path.
        
        Args:
            path: The path to request
            
        Returns:
            Dict[str, Any]: The JSON response
            
        Raises:
            HTTPError: If the response status code is not 2xx
            RequestException: If there's a network error
            ValueError: If the response is not valid JSON
        """
        try:
            url = f"{self.base_url}{path}"
            response = self.session.get(url)
            
            # Check for HTTP errors
            if not response.ok:
                raise HTTPError(
                    f"HTTP {response.status_code} error",
                    status_code=response.status_code,
                    response=response.json() if response.text else None
                )
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # Handle network errors
            raise HTTPError(f"Network error: {str(e)}")
        except ValueError as e:
            # Handle JSON parsing errors
            raise HTTPError(f"Invalid JSON response: {str(e)}") 
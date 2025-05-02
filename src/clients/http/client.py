from typing import Dict, Any
import requests


class HTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, path: str) -> Dict[str, Any]:
        """Make a GET request to the specified path."""
        url = f"{self.base_url}{path}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json() 
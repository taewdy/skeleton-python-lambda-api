from typing import List
import requests
from ..clients.http.client import HTTPClient, HTTPError
from ..api.exceptions import ExternalServiceError
from .models import Photo


class PhotoService:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def get_photos(self) -> List[Photo]:
        """
        Fetch photos from the external API.
        
        Returns:
            List[Photo]: List of photos
            
        Raises:
            ExternalServiceError: If there's an error fetching or processing the photos
        """
        try:
            data = self.http_client.get("/photos")
            return [Photo.from_dict(photo_data) for photo_data in data]
        except HTTPError as e:
            # Handle HTTP-specific errors
            raise ExternalServiceError(
                f"Failed to fetch photos: {e.message}",
                {
                    "error": str(e),
                    "type": "http_error",
                    "status_code": e.status_code,
                    "response": e.response
                }
            )
        except (ValueError, KeyError) as e:
            # Handle data parsing errors
            raise ExternalServiceError(
                "Invalid response format from external service",
                {"error": str(e), "type": "invalid_response"}
            ) 
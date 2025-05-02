from typing import List
from ..clients.http.client import HTTPClient
from .models import Photo


class PhotoService:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def get_photos(self) -> List[Photo]:
        """Fetch photos from the external API."""
        data = self.http_client.get("/photos")
        return [Photo.from_dict(photo_data) for photo_data in data] 
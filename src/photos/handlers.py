import json
from typing import Dict, Any, Optional
from .http_client import HTTPClient
from .services import PhotoService


class PhotoHandler:
    def __init__(self, http_client: Optional[HTTPClient] = None):
        self.http_client = http_client or HTTPClient("https://jsonplaceholder.typicode.com")
        self.photo_service = PhotoService(self.http_client)

    def get_photos(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """Lambda handler for GET /photos endpoint."""
        try:
            photos = self.photo_service.get_photos()

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps([{
                    "albumId": photo.album_id,
                    "id": photo.id,
                    "title": photo.title,
                    "url": photo.url,
                    "thumbnailUrl": photo.thumbnail_url,
                } for photo in photos]),
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps({"error": str(e)}),
            }


# Create a default handler instance for Lambda
handler = PhotoHandler()
get_photos_handler = handler.get_photos 
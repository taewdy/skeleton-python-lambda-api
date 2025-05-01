import json
from typing import Dict, Any
from .http_client import HTTPClient
from .services import PhotoService


def get_photos_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for GET /photos endpoint."""
    try:
        http_client = HTTPClient("https://jsonplaceholder.typicode.com")
        photo_service = PhotoService(http_client)
        photos = photo_service.get_photos()

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
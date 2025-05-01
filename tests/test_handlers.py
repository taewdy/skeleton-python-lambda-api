import json
from unittest.mock import Mock, patch
from src.photos.handlers import PhotoHandler
from src.photos.http_client import HTTPClient


def test_get_photos_handler_success():
    mock_photos = [
        {
            "albumId": 1,
            "id": 1,
            "title": "test photo",
            "url": "http://example.com/photo.jpg",
            "thumbnailUrl": "http://example.com/thumb.jpg",
        }
    ]
    
    mock_client = Mock(spec=HTTPClient)
    mock_client.get.return_value = mock_photos
    
    handler = PhotoHandler(http_client=mock_client)
    response = handler.get_photos({}, None)
    
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == mock_photos
    assert response["headers"]["Content-Type"] == "application/json"


def test_get_photos_handler_error():
    mock_client = Mock(spec=HTTPClient)
    mock_client.get.side_effect = Exception("API Error")
    
    handler = PhotoHandler(http_client=mock_client)
    response = handler.get_photos({}, None)
    
    assert response["statusCode"] == 500
    assert "error" in json.loads(response["body"])
    assert response["headers"]["Content-Type"] == "application/json" 
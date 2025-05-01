import json
from unittest.mock import patch
from src.handlers import get_photos_handler


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
    
    with patch("src.handlers.HTTPClient") as mock_client:
        mock_client.return_value.get.return_value = mock_photos
        
        response = get_photos_handler({}, None)
        
        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == mock_photos
        assert response["headers"]["Content-Type"] == "application/json"


def test_get_photos_handler_error():
    with patch("src.handlers.HTTPClient") as mock_client:
        mock_client.return_value.get.side_effect = Exception("API Error")
        
        response = get_photos_handler({}, None)
        
        assert response["statusCode"] == 500
        assert "error" in json.loads(response["body"])
        assert response["headers"]["Content-Type"] == "application/json" 
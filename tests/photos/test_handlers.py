import pytest
from unittest.mock import Mock, patch
from src.clients.http.client import HTTPClient
from src.photos.handlers import PhotoHandler


@pytest.fixture
def mock_http_client():
    return Mock(spec=HTTPClient)


@pytest.fixture
def photo_handler(mock_http_client):
    return PhotoHandler(mock_http_client)


def test_get_photos_handler(photo_handler, mock_http_client):
    # Arrange
    mock_response = [
        {
            "albumId": 1,
            "id": 1,
            "title": "test photo",
            "url": "http://example.com/photo.jpg",
            "thumbnailUrl": "http://example.com/thumb.jpg",
        }
    ]
    mock_http_client.get.return_value = mock_response

    # Act
    response = photo_handler.get_photos({}, None)

    # Assert
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
    assert len(response["body"]) > 0
    mock_http_client.get.assert_called_once_with("/photos")


def test_get_photos_handler_error(photo_handler, mock_http_client):
    # Arrange
    mock_http_client.get.side_effect = Exception("Test error")

    # Act
    response = photo_handler.get_photos({}, None)

    # Assert
    assert response["statusCode"] == 500
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
    assert "error" in response["body"] 
import pytest
from unittest.mock import Mock, patch
from src.clients.http.client import HTTPClient
from src.photos.services import PhotoService


@pytest.fixture
def mock_http_client():
    return Mock(spec=HTTPClient)


@pytest.fixture
def photo_service(mock_http_client):
    return PhotoService(mock_http_client)


def test_get_photos(photo_service, mock_http_client):
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
    photos = photo_service.get_photos()

    # Assert
    assert len(photos) == 1
    assert photos[0].album_id == 1
    assert photos[0].id == 1
    assert photos[0].title == "test photo"
    assert photos[0].url == "http://example.com/photo.jpg"
    assert photos[0].thumbnail_url == "http://example.com/thumb.jpg"
    mock_http_client.get.assert_called_once_with("/photos") 
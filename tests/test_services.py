import pytest
from unittest.mock import Mock
from src.services import PhotoService
from src.http_client import HTTPClient


@pytest.fixture
def mock_http_client():
    client = Mock(spec=HTTPClient)
    client.get.return_value = [
        {
            "albumId": 1,
            "id": 1,
            "title": "test photo",
            "url": "http://example.com/photo.jpg",
            "thumbnailUrl": "http://example.com/thumb.jpg",
        }
    ]
    return client


def test_get_photos(mock_http_client):
    service = PhotoService(mock_http_client)
    photos = service.get_photos()
    
    assert len(photos) == 1
    photo = photos[0]
    assert photo.album_id == 1
    assert photo.id == 1
    assert photo.title == "test photo"
    assert photo.url == "http://example.com/photo.jpg"
    assert photo.thumbnail_url == "http://example.com/thumb.jpg" 
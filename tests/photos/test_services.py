import pytest
from unittest.mock import Mock, patch
from src.clients.http.client import HTTPClient, HTTPError
from src.photos.services import PhotoService


class TestPhotoService:
    @pytest.fixture
    def mock_http_client(self):
        return Mock()

    @pytest.fixture
    def photo_service(self, mock_http_client):
        return PhotoService(mock_http_client)

    def test_get_photos_success(self, photo_service, mock_http_client):
        mock_data = [
            {
                "id": 1,
                "title": "Photo 1",
                "url": "https://example.com/photo1.jpg",
                "thumbnailUrl": "https://example.com/thumb1.jpg"
            },
            {
                "id": 2,
                "title": "Photo 2",
                "url": "https://example.com/photo2.jpg",
                "thumbnailUrl": "https://example.com/thumb2.jpg"
            }
        ]
        mock_http_client.get.return_value = mock_data

        photos = photo_service.get_photos()
        assert len(photos) == 2
        assert photos[0].id == 1
        assert photos[0].title == "Photo 1"
        assert photos[1].id == 2
        assert photos[1].title == "Photo 2"

    def test_get_photos_http_error(self, photo_service, mock_http_client):
        mock_http_client.get.side_effect = HTTPError(
            message="API Error",
            status_code=500
        )

        with pytest.raises(HTTPError) as exc_info:
            photo_service.get_photos()
        assert exc_info.value.status_code == 500
        assert exc_info.value.message == "API Error"

    def test_get_photos_invalid_data(self, photo_service, mock_http_client):
        mock_http_client.get.return_value = "invalid data"

        with pytest.raises(ValueError) as exc_info:
            photo_service.get_photos()
        assert "Invalid data format" in str(exc_info.value)

    def test_get_photos_empty_list(self, photo_service, mock_http_client):
        mock_http_client.get.return_value = []

        photos = photo_service.get_photos()
        assert len(photos) == 0

    def test_get_photos_missing_fields(self, photo_service, mock_http_client):
        mock_data = [
            {
                "id": 1,
                "title": "Photo 1"
                # Missing url and thumbnailUrl
            }
        ]
        mock_http_client.get.return_value = mock_data

        with pytest.raises(ValueError) as exc_info:
            photo_service.get_photos()
        assert "Missing required fields" in str(exc_info.value)

    def test_get_photos_invalid_urls(self, photo_service, mock_http_client):
        mock_data = [
            {
                "id": 1,
                "title": "Photo 1",
                "url": "not-a-url",
                "thumbnailUrl": "not-a-url"
            }
        ]
        mock_http_client.get.return_value = mock_data

        with pytest.raises(ValueError) as exc_info:
            photo_service.get_photos()
        assert "Invalid URL format" in str(exc_info.value) 
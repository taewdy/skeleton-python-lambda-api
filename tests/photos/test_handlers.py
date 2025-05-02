import pytest
from unittest.mock import Mock, patch
from src.clients.http.client import HTTPClient, HTTPError
from src.api.exceptions import ExternalServiceError
from src.photos.handlers import PhotoHandler
from src.photos.services import PhotoService


@pytest.fixture
def mock_http_client():
    return Mock(spec=HTTPClient)


@pytest.fixture
def photo_handler(mock_http_client):
    return PhotoHandler(mock_http_client)


def test_get_photos_handler_success(photo_handler, mock_http_client):
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


def test_get_photos_handler_http_error(photo_handler, mock_http_client):
    # Arrange
    mock_http_client.get.side_effect = HTTPError(
        "Service unavailable",
        status_code=503,
        response={"error": "Service down"}
    )

    # Act
    response = photo_handler.get_photos({}, None)

    # Assert
    assert response["statusCode"] == 503
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
    error_body = response["body"]
    assert "error" in error_body
    assert "message" in error_body["error"]
    assert "details" in error_body["error"]


def test_get_photos_handler_unexpected_error(photo_handler, mock_http_client):
    # Arrange
    mock_http_client.get.side_effect = Exception("Unexpected error")

    # Act
    response = photo_handler.get_photos({}, None)

    # Assert
    assert response["statusCode"] == 500
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
    error_body = response["body"]
    assert "error" in error_body
    assert error_body["error"]["message"] == "An unexpected error occurred"
    assert "details" in error_body["error"]


class TestPhotoHandler:
    @pytest.fixture
    def mock_photo_service(self):
        return Mock(spec=PhotoService)

    @pytest.fixture
    def photo_handler(self, mock_photo_service):
        return PhotoHandler(mock_photo_service)

    def test_get_photos_success(self, photo_handler, mock_photo_service):
        mock_photos = [
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
        mock_photo_service.get_photos.return_value = mock_photos

        response = photo_handler.get_photos()
        assert response["statusCode"] == 200
        assert response["body"] == mock_photos
        assert response["headers"]["Content-Type"] == "application/json"

    def test_get_photos_http_error(self, photo_handler, mock_photo_service):
        mock_photo_service.get_photos.side_effect = HTTPError(
            message="API Error",
            status_code=500
        )

        response = photo_handler.get_photos()
        assert response["statusCode"] == 500
        assert "API Error" in response["body"]
        assert response["headers"]["Content-Type"] == "application/json"

    def test_get_photos_validation_error(self, photo_handler, mock_photo_service):
        mock_photo_service.get_photos.side_effect = ValueError("Invalid data format")

        response = photo_handler.get_photos()
        assert response["statusCode"] == 400
        assert "Invalid data format" in response["body"]
        assert response["headers"]["Content-Type"] == "application/json"

    def test_get_photos_unexpected_error(self, photo_handler, mock_photo_service):
        mock_photo_service.get_photos.side_effect = Exception("Unexpected error")

        response = photo_handler.get_photos()
        assert response["statusCode"] == 500
        assert "Internal server error" in response["body"]
        assert response["headers"]["Content-Type"] == "application/json"

    def test_get_photos_empty_list(self, photo_handler, mock_photo_service):
        mock_photo_service.get_photos.return_value = []

        response = photo_handler.get_photos()
        assert response["statusCode"] == 200
        assert response["body"] == []
        assert response["headers"]["Content-Type"] == "application/json" 
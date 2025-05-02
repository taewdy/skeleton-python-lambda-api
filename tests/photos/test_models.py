import pytest
from src.api.exceptions import ValidationError
from src.photos.models import Photo


def test_photo_from_dict():
    # Arrange
    data = {
        "albumId": 1,
        "id": 1,
        "title": "test photo",
        "url": "http://example.com/photo.jpg",
        "thumbnailUrl": "http://example.com/thumb.jpg",
    }

    # Act
    photo = Photo.from_dict(data)

    # Assert
    assert photo.album_id == 1
    assert photo.id == 1
    assert photo.title == "test photo"
    assert photo.url == "http://example.com/photo.jpg"
    assert photo.thumbnail_url == "http://example.com/thumb.jpg"


def test_photo_from_dict_missing_field():
    # Arrange
    data = {
        "id": 1,
        "title": "test photo",
        "url": "http://example.com/photo.jpg",
        "thumbnailUrl": "http://example.com/thumb.jpg",
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Photo.from_dict(data)
    
    assert exc_info.value.message.startswith("Missing required field")
    assert exc_info.value.details["field"] == "albumId"


def test_photo_from_dict_invalid_type():
    # Arrange
    data = {
        "albumId": "not_an_int",
        "id": 1,
        "title": "test photo",
        "url": "http://example.com/photo.jpg",
        "thumbnailUrl": "http://example.com/thumb.jpg",
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Photo.from_dict(data)
    
    assert exc_info.value.message == "Invalid data format"


class TestPhoto:
    def test_photo_creation(self):
        data = {
            "id": 1,
            "title": "Test Photo",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumb.jpg"
        }
        photo = Photo(**data)
        assert photo.id == 1
        assert photo.title == "Test Photo"
        assert photo.url == "https://example.com/photo.jpg"
        assert photo.thumbnail_url == "https://example.com/thumb.jpg"

    def test_photo_creation_with_missing_fields(self):
        data = {
            "id": 1,
            "title": "Test Photo"
        }
        with pytest.raises(ValueError) as exc_info:
            Photo(**data)
        assert "Missing required fields" in str(exc_info.value)

    def test_photo_creation_with_invalid_urls(self):
        data = {
            "id": 1,
            "title": "Test Photo",
            "url": "not-a-url",
            "thumbnailUrl": "not-a-url"
        }
        with pytest.raises(ValueError) as exc_info:
            Photo(**data)
        assert "Invalid URL format" in str(exc_info.value)

    def test_photo_creation_with_empty_title(self):
        data = {
            "id": 1,
            "title": "",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumb.jpg"
        }
        with pytest.raises(ValueError) as exc_info:
            Photo(**data)
        assert "Title cannot be empty" in str(exc_info.value)

    def test_photo_creation_with_invalid_id(self):
        data = {
            "id": -1,
            "title": "Test Photo",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumb.jpg"
        }
        with pytest.raises(ValueError) as exc_info:
            Photo(**data)
        assert "ID must be a positive integer" in str(exc_info.value)

    def test_photo_to_dict(self):
        data = {
            "id": 1,
            "title": "Test Photo",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumb.jpg"
        }
        photo = Photo(**data)
        assert photo.to_dict() == data 
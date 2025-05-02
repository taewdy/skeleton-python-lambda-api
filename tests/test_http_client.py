import pytest
from unittest.mock import Mock, patch
from src.infrastructure.http.client import HTTPClient


@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {"test": "data"}
    mock.raise_for_status.return_value = None
    return mock


@pytest.fixture
def http_client():
    return HTTPClient("https://api.example.com")


def test_get_success(http_client, mock_response):
    with patch("requests.Session.get", return_value=mock_response):
        result = http_client.get("/test")
        assert result == {"test": "data"}


def test_get_error(http_client):
    with patch("requests.Session.get", side_effect=Exception("API Error")):
        with pytest.raises(Exception):
            http_client.get("/test") 
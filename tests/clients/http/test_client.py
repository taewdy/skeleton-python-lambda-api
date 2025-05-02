import pytest
from unittest.mock import Mock, patch
from src.clients.http.client import HTTPClient, HTTPError
import requests


@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {"test": "data"}
    mock.ok = True
    return mock


@pytest.fixture
def http_client():
    return HTTPClient("https://api.example.com")


class TestHTTPClient:
    def test_initialization(self):
        base_url = "https://api.example.com"
        client = HTTPClient(base_url)
        assert client.base_url == base_url
        assert isinstance(client.session, Mock)

    def test_get_success(self, http_client, mock_response):
        with patch("requests.Session.get", return_value=mock_response):
            result = http_client.get("/test")
            assert result == {"test": "data"}

    def test_get_with_query_params(self, http_client, mock_response):
        with patch("requests.Session.get", return_value=mock_response) as mock_get:
            http_client.get("/test", params={"key": "value"})
            mock_get.assert_called_once_with(
                "https://api.example.com/test",
                params={"key": "value"}
            )

    def test_get_http_error(self, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        
        with patch("requests.Session.get", return_value=mock_response):
            with pytest.raises(HTTPError) as exc_info:
                http_client.get("/test")
            
            assert exc_info.value.status_code == 404
            assert "HTTP 404 error" in exc_info.value.message
            assert exc_info.value.response is None

    def test_get_http_error_with_response(self, http_client):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.text = '{"error": "Bad Request"}'
        mock_response.json.return_value = {"error": "Bad Request"}
        
        with patch("requests.Session.get", return_value=mock_response):
            with pytest.raises(HTTPError) as exc_info:
                http_client.get("/test")
            
            assert exc_info.value.status_code == 400
            assert exc_info.value.response == {"error": "Bad Request"}

    def test_get_network_error(self, http_client):
        with patch("requests.Session.get", side_effect=Exception("Network Error")):
            with pytest.raises(HTTPError) as exc_info:
                http_client.get("/test")
            
            assert "Network error" in exc_info.value.message
            assert exc_info.value.status_code is None
            assert exc_info.value.response is None

    def test_get_invalid_json(self, http_client):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.side_effect = ValueError("Invalid JSON")
        
        with patch("requests.Session.get", return_value=mock_response):
            with pytest.raises(HTTPError) as exc_info:
                http_client.get("/test")
            
            assert "Invalid JSON response" in exc_info.value.message
            assert exc_info.value.status_code is None
            assert exc_info.value.response is None

    def test_get_timeout(self, http_client):
        with patch("requests.Session.get", side_effect=requests.exceptions.Timeout("Request timed out")):
            with pytest.raises(HTTPError) as exc_info:
                http_client.get("/test")
            
            assert "Network error" in exc_info.value.message
            assert "Request timed out" in str(exc_info.value.message)

    def test_get_connection_error(self, http_client):
        with patch("requests.Session.get", side_effect=requests.exceptions.ConnectionError("Connection refused")):
            with pytest.raises(HTTPError) as exc_info:
                http_client.get("/test")
            
            assert "Network error" in exc_info.value.message
            assert "Connection refused" in str(exc_info.value.message) 
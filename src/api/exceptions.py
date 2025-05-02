from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict


class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, status_code: int, message: str, details: Dict[str, Any] = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ExternalServiceError(APIError):
    """Exception for errors from external services."""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(500, message, details)


class ValidationError(APIError):
    """Exception for validation errors."""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(400, message, details)


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handler for APIError exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
            }
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handler for FastAPI's HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "details": {},
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "details": {"type": type(exc).__name__},
            }
        }
    ) 
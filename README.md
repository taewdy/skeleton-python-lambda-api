# Python Lambda API Project

A Python-based Lambda API project that follows clean architecture principles and best practices.

## Project Structure

```
src/
├── api/                    # FastAPI application
│   ├── __init__.py
│   ├── app.py             # FastAPI application definition
│   └── exceptions.py      # Custom exceptions and handlers
├── clients/               # External service clients
│   └── http/             # HTTP client implementation
│       ├── __init__.py
│       └── client.py
├── photos/               # Photos feature module
│   ├── __init__.py
│   ├── models.py        # Data models
│   ├── services.py      # Business logic
│   └── handlers.py      # Lambda handlers
└── __init__.py

tests/
├── photos/              # Tests for photos feature
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_handlers.py
└── __init__.py

```

## Features

- Clean Architecture with clear separation of concerns
- Dependency Injection for better testability
- Type hints for better code maintainability
- Unit tests with pytest
- CI/CD pipeline with Terraform
- Local development with FastAPI
- Comprehensive error handling

## Error Handling

The project implements a robust error handling system following these principles:

### Error Hierarchy

1. **Base Exceptions**:
   - `APIError`: Base exception for all API errors
   - `HTTPError`: Base exception for HTTP client errors

2. **Specific Exceptions**:
   - `ExternalServiceError`: For errors from external services
   - `ValidationError`: For input validation errors

### Error Response Format

All errors follow a consistent JSON format:
```json
{
  "error": {
    "message": "Error message",
    "details": {
      "type": "error_type",
      "status_code": 500,
      "additional": "information"
    }
  }
}
```

### Error Handling Layers

1. **HTTP Client Layer**:
   - Handles network and HTTP-specific errors
   - Provides detailed error information including status codes
   - Example: `HTTPError` with status code and response

2. **Service Layer**:
   - Transforms low-level errors into domain-specific errors
   - Adds context to errors
   - Example: `ExternalServiceError` with service-specific details

3. **API Layer**:
   - Global exception handlers
   - Consistent error response format
   - Proper HTTP status codes

### Best Practices

1. **Specific Error Types**:
   ```python
   try:
       result = some_function()
   except SpecificError as e:
       # Handle specific error
   except AnotherError as e:
       # Handle another error
   ```

2. **Error Documentation**:
   ```python
   def some_function() -> Result:
       """
       Raises:
           SpecificError: When something specific goes wrong
           AnotherError: When something else goes wrong
       """
   ```

3. **Error Context**:
   - Include relevant details in error messages
   - Provide actionable information
   - Log appropriate error levels

4. **Error Propagation**:
   - Let errors propagate to appropriate handlers
   - Transform errors at each layer
   - Maintain error context

### Example Error Handling

```python
# HTTP Client
try:
    response = http_client.get("/photos")
except HTTPError as e:
    # Handle HTTP-specific errors
    raise ExternalServiceError(
        f"Failed to fetch photos: {e.message}",
        {"status_code": e.status_code, "response": e.response}
    )

# Service Layer
try:
    photos = photo_service.get_photos()
except ExternalServiceError as e:
    # Handle service errors
    return {"error": e.message, "details": e.details}
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest
```

## Local Development

The project includes a FastAPI application for local development and testing.

### Running the Local Server

1. Start the development server:
```bash
python run_local.py
```

2. Access the API:
- API endpoint: `http://localhost:8000/photos`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

3. Test with curl:
```bash
curl http://localhost:8000/photos
```

### Benefits of Local Development

- Hot-reloading during development
- Built-in OpenAPI documentation
- Easy debugging
- Type validation and serialization
- CORS support out of the box

## API Endpoints

### GET /photos
Retrieves a list of photos from an external API.

Response:
```json
[
  {
    "albumId": 1,
    "id": 1,
    "title": "accusamus beatae ad facilis cum similique qui sunt",
    "url": "https://via.placeholder.com/600/92c952",
    "thumbnailUrl": "https://via.placeholder.com/150/92c952"
  }
]
```

## Development

### Adding New Features

1. Create a new feature module under `src/` (e.g., `src/users/`)
2. Implement models, services, and handlers
3. Add corresponding tests
4. Update the README with new endpoints

### Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src
```

## Deployment

The project uses Terraform for infrastructure as code. See the `terraform/` directory for deployment configurations.

### AWS Lambda Deployment

The project is configured for AWS Lambda deployment with:
- API Gateway integration
- IAM roles and permissions
- Environment variables

To deploy:
1. Configure AWS credentials
2. Initialize Terraform:
```bash
cd infrastructure
terraform init
```
3. Apply the configuration:
```bash
terraform apply
```

## License

MIT 
# Python Lambda API Project

A Python-based Lambda API project that follows clean architecture principles and best practices.

## Project Structure

```
src/
├── api/                    # FastAPI application
│   ├── __init__.py
│   └── app.py             # FastAPI application definition
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
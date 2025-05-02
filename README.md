# Python Lambda API Project

A Python-based Lambda API project that follows clean architecture principles and best practices.

## Project Structure

```
src/
├── clients/                 # External service clients
│   └── http/               # HTTP client implementation
│       ├── __init__.py
│       └── client.py
├── photos/                 # Photos feature module
│   ├── __init__.py
│   ├── models.py          # Data models
│   ├── services.py        # Business logic
│   └── handlers.py        # Lambda handlers
└── __init__.py

tests/
├── photos/                # Tests for photos feature
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

## License

MIT 
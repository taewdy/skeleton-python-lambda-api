# Photos API Lambda Function

A serverless API built with AWS Lambda and API Gateway that fetches photos from JSONPlaceholder API.

## Project Structure

```
.
├── src/                    # Source code
│   └── photos/            # Photos domain package
│       ├── __init__.py    # Package initialization
│       ├── http_client.py # HTTP client for external API calls
│       ├── models.py      # Data models
│       ├── services.py    # Business logic
│       └── handlers.py    # Lambda handlers
├── tests/                 # Test files
├── infrastructure/        # Terraform configuration
├── .github/workflows/     # CI/CD pipeline
├── requirements.txt       # Python dependencies
└── pyproject.toml         # Project configuration
```

### Structure Rationale

The project follows a domain-driven structure under `src/photos/` rather than a deeper nested structure. This approach was chosen because:

1. **Single Domain Focus**: All components are part of the same domain (photos)
2. **Clear Relationships**: Components are closely related and have clear dependencies
3. **Simplicity**: The codebase is relatively small and focused
4. **Pythonic**: Follows Python's "flat is better than nested" principle
5. **Maintainability**: Shorter import paths and easier navigation

#### When to Consider Deeper Nesting

A more nested structure might be appropriate when:
- Multiple distinct domains exist (e.g., photos, users, auth)
- Complex subsystems within a domain
- Large codebases with many related components
- Need to group related functionality

Example of a more nested structure for larger projects:
```
src/
├── photos/
│   ├── client/
│   │   └── http_client.py
│   ├── models/
│   │   └── photo.py
│   ├── services/
│   │   └── photo_service.py
│   └── handlers/
│       └── photo_handler.py
├── users/
│   ├── models/
│   ├── services/
│   └── handlers/
└── common/
    ├── utils/
    └── exceptions/
```

## Features

- Fetches photos from JSONPlaceholder API
- Clean architecture with separation of concerns
- Unit tests with pytest
- Code coverage reporting
- Linting with black, flake8, and mypy
- CI/CD pipeline with GitHub Actions
- Infrastructure as Code with Terraform

## Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run linters:
   ```bash
   black src tests
   flake8 src tests
   mypy src
   ```

## Deployment

The project is configured with GitHub Actions for CI/CD. The pipeline:

1. Runs tests and linters
2. Checks code coverage
3. Deploys to AWS using Terraform

To deploy manually:

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

## API Endpoints

- `GET /photos`: Returns a list of photos from JSONPlaceholder API

## Dependencies

- Python 3.9+
- AWS Lambda
- AWS API Gateway
- Terraform
- GitHub Actions 
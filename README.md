# Tratrouble Backend

Tratrouble is a mobile app for collecting feedback about public transportation in the Berlin/Brandenburg region. This repository contains the Django backend API for the Tratrouble application.

## Overview

The Tratrouble backend provides REST API endpoints for:

- **Email Verification**: Users can submit their email address to receive a verification link
- **Token Management**: Secure token generation and validation for authenticated requests
- **Feedback Submission**: Users can submit feedback about bus trips including line, destination, and geolocation
- **Admin Interface**: Django admin panel for managing feedback and user data

## Features

- Email-based authentication without storing email-token associations
- HMAC-based token generation for security
- Token expiration (1 hour)
- Support for both web and mobile app verification flows
- Environment variable configuration for deployment flexibility

## API Endpoints

- `POST /api/submit-email/` - Submit email for verification
- `GET /api/verify-email/?token=<token>` - Verify email via link
- `POST /api/check-token/` - Check if token is valid and verified
- `POST /api/submit-feedback/` - Submit feedback about a bus trip
- `POST /api/bad-json/` - Submit JSON data (for testing/development)

## Prerequisites

- Python 3.8+
- Django 5.2
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/jogojapan/tratroubleBackend.git
cd tratroubleBackend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create configuration files:
   - Copy `tratroubleBackend/email_credentials.py` and add your SMTP credentials
   - Copy `tratroubleBackend/email_config.py` and configure your domain

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Docker Deployment


### Build Script Usage

The most convenient way of building a docker image and having the git commit id included as a version string is to use the build script we provide:

This script builds the `tratrouble-backend` Docker image with a tag based on the current Git commit hash. It supports optional tagging with a namespace and the `:latest` tag.

#### Options

- `--namespace <name>`  
  Sets the Docker namespace (e.g., `jogojapan`).  
  Default: none (builds as `tratrouble-backend:<tag>`)

- `--latest`  
  Also builds and tags the image as `:latest`.

#### Examples

Build with Git commit tag only:
```bash
./build.sh
# Result: tratrouble-backend:3cee798
```

Build with namespace:
```bash
./build.sh --namespace myspace
# Result: myspace/tratrouble-backend:3cee798
```

Build with namespace and latest tag:
```bash
./build.sh --namespace myspace --latest
# Results:
# - myspace/tratrouble-backend:3cee798
# - myspace/tratrouble-backend:latest
```

> ✅ The script automatically uses the short Git commit hash (e.g., `3cee798`) as the version tag. Ensure you're in a Git repository when running the script. [^1]

[^1]: [Docker Build](https://docs.docker.com/reference/cli/docker/buildx/build/) (100%)

### Running with Docker

```bash
docker run -p 8000:8000 \
  -e TRATROUBLE_EMAIL_HOST=your-smtp-host \
  -e TRATROUBLE_EMAIL_PORT=587 \
  -e TRATROUBLE_EMAIL_HOST_USER=your-username \
  -e TRATROUBLE_EMAIL_HOST_PASSWORD=your-password \
  -e TRATROUBLE_DEFAULT_FROM_EMAIL=your-email@example.com \
  -e TRATROUBLE_EMAIL_VERIFICATION_DOMAIN=your-domain.com \
  -e TRATROUBLE_EMAIL_VERIFICATION_APP_NAME=com.example.app \
  tratrouble-backend:latest
```

### Running with Docker Compose

1. Create a `.env` file with your configuration:
```env
TRATROUBLE_EMAIL_HOST=your-smtp-host
TRATROUBLE_EMAIL_PORT=587
TRATROUBLE_EMAIL_HOST_USER=your-username
TRATROUBLE_EMAIL_HOST_PASSWORD=your-password
TRATROUBLE_DEFAULT_FROM_EMAIL=your-email@example.com
TRATROUBLE_EMAIL_VERIFICATION_DOMAIN=your-domain.com
TRATROUBLE_EMAIL_VERIFICATION_APP_NAME=com.example.app
```

2. Start the services:
```bash
docker-compose up -d
```

3. Stop the services:
```bash
docker-compose down
```

### Running with Podman

Podman is a drop-in replacement for Docker. Use the same commands:

```bash
podman build -t tratrouble-backend:latest .

podman run -p 8000:8000 \
  -e TRATROUBLE_EMAIL_HOST=your-smtp-host \
  -e TRATROUBLE_EMAIL_PORT=587 \
  -e TRATROUBLE_EMAIL_HOST_USER=your-username \
  -e TRATROUBLE_EMAIL_HOST_PASSWORD=your-password \
  -e TRATROUBLE_DEFAULT_FROM_EMAIL=your-email@example.com \
  -e TRATROUBLE_EMAIL_VERIFICATION_DOMAIN=your-domain.com \
  -e TRATROUBLE_EMAIL_VERIFICATION_APP_NAME=com.example.app \
  tratrouble-backend:latest
```

Or with Podman Compose:
```bash
podman-compose up -d
```

## Container User and Permissions

The Tratrouble backend container runs as a non-root user for security:

- **User ID (UID)**: 1000
- **Group ID (GID)**: 100

### Volume Permissions

When mapping volumes for the database and logs, ensure the host directories have the correct permissions so the container user can read and write to them.

#### Option 1: Create directories with correct ownership (Recommended)

```bash
# Create the directories
mkdir -p ./data ./logs

# Set ownership to UID 1000 and GID 100
chown 1000:100 ./data ./logs

# Set permissions (755 allows owner to read/write/execute)
chmod 755 ./data ./logs
```

#### Option 2: Use Docker volume driver

Instead of bind mounts, use Docker named volumes which handle permissions automatically:

```yaml
volumes:
  data:
  logs:

services:
  web:
    volumes:
      - data:/code/data
      - logs:/code/logs
```

#### Option 3: Run with user mapping (Podman)

If using Podman, you can map the container user to your host user:

```bash
podman run --userns=keep-id \
  -v ./data:/code/data \
  -v ./logs:/code/logs \
  tratrouble-backend:latest
```

### Troubleshooting Permission Issues

If you encounter "Permission denied" errors:

1. Check the ownership of your mounted directories:
   ```bash
   ls -ld ./data ./logs
   ```

2. Verify the permissions:
   ```bash
   ls -la ./data ./logs
   ```

3. Fix permissions if needed:
   ```bash
   chown 1000:100 ./data ./logs
   chmod 755 ./data ./logs
   ```

## Environment Variables

All configuration can be provided via environment variables with the `TRATROUBLE_` prefix:

### Server Configuration

- `TRATROUBLE_ALLOWED_HOSTS` - Comma-separated list of allowed hosts (default: `localhost,127.0.0.1`)
- `TRATROUBLE_DEBUG` - Enable debug mode (default: `True`)
- `TRATROUBLE_SECRET_KEY` - Django secret key for production (default: insecure development key)
- `TRATROUBLE_CORS_ALLOWED_ORIGINS` - Comma-separated list of CORS allowed origins (default: `http://localhost:3000,http://localhost:8000`)

### Email Configuration

- `TRATROUBLE_EMAIL_HOST` - SMTP server hostname
- `TRATROUBLE_EMAIL_PORT` - SMTP server port (default: 587)
- `TRATROUBLE_EMAIL_HOST_USER` - SMTP username
- `TRATROUBLE_EMAIL_HOST_PASSWORD` - SMTP password
- `TRATROUBLE_EMAIL_USE_TLS` - Use TLS for SMTP (default: True)
- `TRATROUBLE_DEFAULT_FROM_EMAIL` - From email address for sending emails
- `TRATROUBLE_EMAIL_VERIFICATION_DOMAIN` - Domain for web verification links
- `TRATROUBLE_EMAIL_VERIFICATION_APP_NAME` - App scheme for mobile verification links

### Example Configuration

For local development:
```bash
export TRATROUBLE_ALLOWED_HOSTS=localhost,127.0.0.1
export TRATROUBLE_DEBUG=True
export TRATROUBLE_CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

For production:
```bash
export TRATROUBLE_ALLOWED_HOSTS=api.example.com,example.com
export TRATROUBLE_DEBUG=False
export TRATROUBLE_SECRET_KEY=your-secure-secret-key-here
export TRATROUBLE_CORS_ALLOWED_ORIGINS=https://app.example.com,https://example.com
```

## Database

The application uses SQLite by default for development. For production, consider migrating to PostgreSQL by updating the `DATABASES` setting in `settings.py`.

## Admin Interface

Access the Django admin panel at `http://localhost:8000/admin/` with superuser credentials.

To create a superuser:
```bash
python manage.py createsuperuser
```

## Project Structure

```
tratroubleBackend/
├── feedback/                 # Main feedback app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── urls.py              # App URL routing
│   └── migrations/          # Database migrations
├── tratroubleBackend/        # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── server_config.py     # Server configuration (domain, debug, CORS)
│   ├── email_config.py      # Email configuration
│   └── email_credentials.py # SMTP credentials
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
└── docker-compose.yml       # Docker Compose configuration
```

## Contributing

Contributions are welcome! Please ensure all code follows Django best practices and includes appropriate error handling.

## License

This project is part of the Tratrouble initiative for improving public transportation feedback in Berlin/Brandenburg. We make our code available under the MIT license.

## Support

For issues or questions, please open an issue on the GitHub repository.

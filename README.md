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

### Building the Docker Image

```bash
docker build -t tratrouble-backend:latest .
```

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

## Environment Variables

All configuration can be provided via environment variables with the `TRATROUBLE_` prefix:

- `TRATROUBLE_EMAIL_HOST` - SMTP server hostname
- `TRATROUBLE_EMAIL_PORT` - SMTP server port (default: 587)
- `TRATROUBLE_EMAIL_HOST_USER` - SMTP username
- `TRATROUBLE_EMAIL_HOST_PASSWORD` - SMTP password
- `TRATROUBLE_EMAIL_USE_TLS` - Use TLS for SMTP (default: True)
- `TRATROUBLE_DEFAULT_FROM_EMAIL` - From email address for sending emails
- `TRATROUBLE_EMAIL_VERIFICATION_DOMAIN` - Domain for web verification links
- `TRATROUBLE_EMAIL_VERIFICATION_APP_NAME` - App scheme for mobile verification links

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

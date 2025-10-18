# Use an official Python runtime
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Accept Git commit hash as a build argument
ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=$GIT_COMMIT

# Expose port
EXPOSE 8000

# Run the Django development server (or use Gunicorn in production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tratroubleBackend.wsgi:application"]

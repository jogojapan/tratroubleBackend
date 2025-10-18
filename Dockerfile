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

# Create necessary directories with proper ownership and permissions
RUN mkdir -p /code/logs /code/data && \
    chown -R 1000:100 /code && \
    chmod 755 /code && \
    chmod 755 /code/logs && \
    chmod 755 /code/data

# Create a non-root user to run the application
RUN groupadd -g 100 appgroup && \
    useradd -m -u 1000 -g 100 appuser && \
    chown -R 1000:100 /code

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run migrations and start the application
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --access-logfile - --error-logfile - tratroubleBackend.wsgi:application"]

#!/bin/bash
set -e  # Exit on any error

# Get the short Git commit hash
GIT_VERSION=$(git rev-parse --short HEAD)

echo "Building Docker image with version: $GIT_VERSION"

# Build the image, passing the commit hash as a build argument
docker build \
  --build-arg GIT_COMMIT=$GIT_VERSION \
  -t tratrouble-backend:$GIT_VERSION \
  .

echo "Image built successfully: my-django-app:$GIT_VERSION"

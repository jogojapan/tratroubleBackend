#!/bin/bash
set -e  # Exit on any error

[ -z "${BUILD_PREFIX:-}" ] && BUILD_PREFIX=""

# Get the short Git commit hash
GIT_VERSION=$(git rev-parse --short HEAD)

echo "Building Docker image with version: $GIT_VERSION"

# Build the image, passing the commit hash as a build argument
docker build \
  --build-arg GIT_COMMIT=$GIT_VERSION \
  -t $BUILD_PREFIX/tratrouble-backend:$GIT_VERSION \
  .

echo "Image built successfully: tratrouble-backend:$GIT_VERSION"

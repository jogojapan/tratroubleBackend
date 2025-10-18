#!/bin/bash
set -e  # Exit on any error

# Default values
BUILD_LATEST=false
NAMESPACE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --latest)
      BUILD_LATEST=true
      shift
      ;;
    --namespace)
      if [[ -n "$2" ]]; then
        NAMESPACE="$2/"
        shift 2
      else
        echo "Error: --namespace requires a value."
        exit 1
      fi
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Remove trailing slash from NAMESPACE if present
NAMESPACE="${NAMESPACE%/}"

# Get the short Git commit hash
GIT_VERSION=$(git rev-parse --short HEAD)

echo "Building Docker image with version: $GIT_VERSION"

# Build the versioned image
docker build \
  --build-arg GIT_COMMIT=$GIT_VERSION \
  -t ${NAMESPACE}tratrouble-backend:$GIT_VERSION \
  .

echo "Image built successfully: ${NAMESPACE}tratrouble-backend:$GIT_VERSION"

# Optionally build the :latest image
if [ "$BUILD_LATEST" = true ]; then
  echo "Building latest image: ${NAMESPACE}tratrouble-backend:latest"
  docker build \
    --build-arg GIT_COMMIT=$GIT_VERSION \
    -t ${NAMESPACE}tratrouble-backend:latest \
    .
  echo "Latest image built successfully: ${NAMESPACE}tratrouble-backend:latest"
fi

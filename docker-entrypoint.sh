#!/bin/bash
set -e

# This script is an entry point for a Docker container.
# It performs environment variable checks, waits for PostgreSQL to be ready,
# optionally runs tests, starts a documentation server, and finally starts the FastAPI server.

# Check if required environment variables are set
if [ -z "${POSTGRES_SERVER}" ] || [ -z "${POSTGRES_PORT}" ]; then
    echo "Error: POSTGRES_SERVER or POSTGRES_PORT is not set."
    exit 1
fi

# Check if the `pg_isready` command is available
if ! command -v pg_isready &> /dev/null; then
    echo "Error: pg_isready command not found. Please install PostgreSQL client tools."
    exit 1
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
until pg_isready -h ${POSTGRES_SERVER} -p ${POSTGRES_PORT} -U ${POSTGRES_USER}; do
    sleep 1
done
echo "PostgreSQL is up and running!"

# If the first argument is "pytest", run tests
if [ "$1" = "pytest" ]; then
    echo "Running tests..."
    # Pass all additional arguments to pytest
    exec pytest "${@:2}"
fi

# Start the Sphinx documentation server in the background if documentation exists
if [ -d "docs/_build/html" ]; then
    echo "Starting Sphinx documentation server on port 8080..."
    python3 -m http.server 8080 --directory docs/_build/html &
else
    echo "Documentation not found. Skipping documentation server."
    echo "To generate documentation, run: 'make html' in the 'docs' directory."
fi

# Start the FastAPI server
echo "Starting FastAPI server on port 8000..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
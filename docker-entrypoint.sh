#!/bin/bash
set -e

# Check PostgreSQL availability
echo "Waiting for PostgreSQL to start..."
until nc -z ${POSTGRES_SERVER} ${POSTGRES_PORT}; do
    sleep 1
done
echo "PostgreSQL is up and running!"

# Start the API server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Start the documentation server
if [ -d "docs/_build/html" ]; then
    cd docs/_build/html && python -m http.server 8080
else
    echo "Documentation not found. Skipping documentation server."
fi
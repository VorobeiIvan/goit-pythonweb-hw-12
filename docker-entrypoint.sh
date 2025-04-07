#!/bin/bash
set -e

# Перевірка змінних середовища
if [ -z "${POSTGRES_SERVER}" ] || [ -z "${POSTGRES_PORT}" ]; then
    echo "Error: POSTGRES_SERVER or POSTGRES_PORT is not set."
    exit 1
fi

# Перевірка наявності pg_isready
if ! command -v pg_isready &> /dev/null; then
    echo "Error: pg_isready command not found. Please install PostgreSQL client tools."
    exit 1
fi

# Перевірка доступності PostgreSQL
echo "Waiting for PostgreSQL to start..."
until pg_isready -h ${POSTGRES_SERVER} -p ${POSTGRES_PORT} -U ${POSTGRES_USER}; do
    sleep 1
done
echo "PostgreSQL is up and running!"

# Якщо запускається для тестів, виконуємо pytest
if [ "$1" = "pytest" ]; then
    echo "Running tests..."
    exec pytest "${@:2}"
fi

# Запуск сервера документації (у фоновому режимі)
if [ -d "docs/_build/html" ]; then
    echo "Starting Sphinx documentation server on port 8080..."
    python3 -m http.server 8080 --directory docs/_build/html &
else
    echo "Documentation not found. Skipping documentation server."
    echo "To generate documentation, run: 'make html' in the 'docs' directory."
fi

# Запуск сервера API
echo "Starting FastAPI server on port 8000..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
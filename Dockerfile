FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    make \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Build documentation (optional)
RUN if [ -d "docs" ]; then cd docs && make html; else echo "Docs directory not found. Skipping documentation build."; fi

# Expose ports for API and documentation (if needed)
EXPOSE 8000 8080

# Copy and set permissions for entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Set entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

# Команда за замовчуванням
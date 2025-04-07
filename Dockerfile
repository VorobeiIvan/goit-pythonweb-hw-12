# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for the application
RUN apt-get update && apt-get install -y \
    curl \  
    make \  
    netcat-openbsd \  
    postgresql-client \  
    && rm -rf /var/lib/apt/lists/*  

# Copy the Python dependencies file into the container
COPY requirements.txt .

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable to include the application directory
ENV PYTHONPATH=/app

# Copy all application files into the container
COPY . .

# Build documentation if the "docs" directory exists (optional step)
RUN if [ -d "docs" ]; then \
        cd docs && make html; \
    else \
        echo "Docs directory not found. Skipping documentation build."; \
    fi

# Expose ports for the API (8000) and documentation (8080, if applicable)
EXPOSE 8000 8080

# Copy the entrypoint script to a directory in the PATH and set executable permissions
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Default command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Set the entrypoint script to be executed as the container's entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
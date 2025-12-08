
# Use Python 3.9 Slim Bookworm (Debian 12) for stable package repositories
FROM python:3.9-slim-bookworm

# Install system dependencies
# - OpenJDK 17 for Spark
# - build-essential and libmysqlclient-dev for mysqlclient
# - procps for general utilities
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set Environment Variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt /app/backend/requirements.txt
COPY scripts/requirements.txt /app/scripts/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r scripts/requirements.txt

# Copy the rest of the application
COPY . /app/

# Set Python path so scripts can find backend modules
ENV PYTHONPATH=/app/backend

# Default command (can be overridden)
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]

# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create backend directory and copy application files
RUN mkdir -p /app/backend
COPY . /app/backend/

# Expose the port the app runs on
EXPOSE 5000

# Note: The following environment variables must be provided when running the container:
# - SUPABASE_URL
# - SUPABASE_KEY
# - REDIS_URL (optional)
# - REDIS_TOKEN (optional)
# - SECRET_KEY

# Command to run the application using the correct module path
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:create_app()"] 
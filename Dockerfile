# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY user_display_optimized.py .
COPY user_display_original.py .
COPY tests/ tests/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command runs tests
CMD ["pytest", "tests/", "--cov=user_display_optimized", "--cov-report=term-missing", "-v"]

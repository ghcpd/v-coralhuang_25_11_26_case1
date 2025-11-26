# Simple cross-platform-friendly image using Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cache-friendly)
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Default command runs tests with coverage
CMD ["bash", "-c", "pytest -q --cov=user_display_optimized --cov-report=term-missing tests"]

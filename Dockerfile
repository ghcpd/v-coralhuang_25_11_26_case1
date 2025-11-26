FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY user_display_optimized.py .
COPY tests/ ./tests/

# Set default command to run tests
CMD ["pytest", "tests/", "--cov=user_display_optimized", "--cov-report=term-missing", "--cov-fail-under=78", "-v"]

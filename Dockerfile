FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app

RUN pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-fail-under=85

CMD ["bash", "run.sh"]

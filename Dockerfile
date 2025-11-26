FROM python:3.10-slim

WORKDIR /app

# Avoid installing venv files into container
COPY requirements.txt /app/
COPY . /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["bash", "test.sh"]

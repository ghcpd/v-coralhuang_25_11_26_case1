FROM python:3.11-slim
WORKDIR /app

# Copy project files
COPY . /app

# Prepare minimal venv inside container and install pinned deps
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

CMD ["bash", "run.sh"]

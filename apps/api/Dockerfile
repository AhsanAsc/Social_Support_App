# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-eng \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip && \
    pip install -e .

COPY apps/api /app/apps/api
COPY services /app/services

EXPOSE 8080
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8080"]

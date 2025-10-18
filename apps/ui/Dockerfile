FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml /app/
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -e .
COPY apps/ui /app/apps/ui
EXPOSE 8501
CMD ["streamlit","run","apps/ui/Home.py","--server.port=8501","--server.address=0.0.0.0"]

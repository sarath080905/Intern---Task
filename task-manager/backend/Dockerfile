# ==============================
# Dockerfile for backend API
# ==============================
# Use a slim Python image for smaller deployment size.
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and enable stdout/stderr buffering.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_URL=sqlite:////app/data/task_manager.db

RUN mkdir -p /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

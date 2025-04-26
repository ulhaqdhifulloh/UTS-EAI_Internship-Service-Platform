# Gunakan image Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install FastAPI dan httpx
RUN pip install fastapi uvicorn httpx

# Copy source code
COPY main.py .

# Jalankan server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

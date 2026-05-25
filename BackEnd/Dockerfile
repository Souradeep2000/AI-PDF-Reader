# 1. Use official lightweight Python image
FROM python:3.11-slim

# 2. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Set working directory
WORKDIR /workspace

# 4. Copy requirements first for better caching
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Cleanup build tools
# RUN apt-get purge -y --auto-remove build-essential gcc

# 6. Copy application
COPY . .

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Run FastAPI with auto reload
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
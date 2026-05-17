# 1. Use the official lightweight Python image
FROM python:3.11-slim

# 2. Install Tesseract OCR AND system build essentials
# Some of your packages (like cffi, cryptography, greenlet, gevent) may require compiling C-extensions during install.
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Set work directory
WORKDIR /workspace

# 4. Upgrade pip and copy requirements first to cache heavy ML installations
COPY requirements.txt .

# We use --no-cache-dir because torch and transformers download huge wheel files (.whl). 
# If we don't clear the cache, your image size will double.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Clean up compilation tools to shrink the final image size
RUN apt-get purge -y --auto-remove build-essential gcc

# 6. Copy the rest of your application code
COPY . .

# 7. Expose FastAPI's default port
EXPOSE 8000

# 8. Run Uvicorn pointing to your app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
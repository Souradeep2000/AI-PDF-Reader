#!/bin/bash
set -e

# 1. Start PostgreSQL server in the background
echo "Starting PostgreSQL..."
mkdir -p /var/run/postgresql
chown -R postgres:postgres /var/run/postgresql /var/lib/postgresql/data
su - postgres -c "/usr/lib/postgresql/17/bin/pg_ctl -D /var/lib/postgresql/data -l /var/log/postgresql.log start"

# Wait for Postgres to accept connections
until su - postgres -c "pg_isready" 2>/dev/null; do
  echo "Waiting for database to boot..."
  sleep 1
done

# Initialize the vector extension if not present
su - postgres -c "psql -d ai_study_platform -c 'CREATE EXTENSION IF NOT EXISTS vector;'"

# 2. Start Ollama in the background
echo "Starting Ollama..."
ollama serve > /var/log/ollama.log 2>&1 &

# Wait for Ollama to wake up
until curl -s http://127.0.0.1:11434 >/dev/null; do
  echo "Waiting for Ollama engine..."
  sleep 1
done

# Pre-pull your lightweight model so it's ready instantly
echo "Pulling Ollama model..."
ollama pull phi3:mini

# 3. Start FastAPI application on Hugging Face's mandatory port (7860)
echo "Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 7860
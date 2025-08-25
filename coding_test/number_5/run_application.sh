#!/bin/bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

curl http://localhost:11434

ollama pull nomic-embed-text
ollama pull gemma3:12b

echo "Starting frontend..."
uv run -m streamlit run frontend/main.py --server.port 8501 &
echo "Frontend started"

echo "Starting backend..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
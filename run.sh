#!/usr/bin/env bash
# Script to launch both FastAPI and Streamlit concurrently

echo "=========================================================="
echo " Starting Smart Resume & Portfolio Parser System"
echo "=========================================================="

# Start FastAPI backend in background
echo "[1/2] Starting FastAPI Backend on http://localhost:8000..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait briefly for FastAPI to initialize
sleep 2

# Start Streamlit frontend
echo "[2/2] Starting Streamlit Frontend on http://localhost:8501..."
python -m streamlit run frontend/app.py --server.port 8501 --server.headless true &
FRONTEND_PID=$!

echo ""
echo "=========================================================="
echo " Both servers are running!"
echo " - Streamlit UI: http://localhost:8501"
echo " - FastAPI API & Docs: http://localhost:8000/docs"
echo " Press Ctrl+C to terminate both servers."
echo "=========================================================="

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait

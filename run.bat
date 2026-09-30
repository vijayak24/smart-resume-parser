@echo off
echo ==========================================================
echo  Starting Smart Resume & Portfolio Parser System (Windows)
echo ==========================================================

echo [1/2] Starting FastAPI Backend on port 8000...
start "FastAPI Backend" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Streamlit Frontend on port 8501...
start "Streamlit Frontend" cmd /k "python -m streamlit run frontend/app.py --server.port 8501 --server.headless true"

echo.
echo ==========================================================
echo  Both servers are launching!
echo  - Streamlit UI: http://localhost:8501
echo  - FastAPI Docs: http://localhost:8000/docs
echo ==========================================================
pause

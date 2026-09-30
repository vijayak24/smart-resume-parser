import os
import sys
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp_engine import analyze_resume, get_embedding_model, get_spacy_model

app = FastAPI(
    title="Smart Automated Resume & Portfolio Parser API",
    description="Backend API for semantic resume matching and skill gap identification using SentenceTransformers and spaCy.",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend (default port 8501) and other clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Smart Resume & Portfolio Parser API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "port": 8000
    }


@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(..., description="PDF Resume file"),
    job_description: str = Form(..., description="Target Job Description text")
):
    """
    Accepts a PDF resume and a Job Description text string.
    Returns semantic match percentage, matched skills, and missing keywords.
    """
    # 1. Validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a valid .pdf file."
        )

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    if len(job_description.strip()) < 30:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short. Please provide a detailed job posting."
        )

    # 2. Read PDF bytes
    try:
        pdf_bytes = await file.read()
        if len(pdf_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF file is empty."
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error reading uploaded file: {str(e)}"
        )

    # 3. Analyze using NLP Engine
    try:
        result = analyze_resume(pdf_bytes, job_description)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing resume with NLP Engine: {str(e)}"
        )

    if not result.get("success", False):
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Failed to parse resume text.")
        )

    return JSONResponse(status_code=200, content=result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

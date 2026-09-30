<div align="center">

# 📄 Smart Automated Resume & Portfolio Parser

An AI-powered resume and portfolio analysis platform that evaluates candidate resumes against job descriptions using dense semantic embeddings and natural language processing.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

[![Open Web App](https://img.shields.io/badge/🚀_Open_Web_App-Streamlit_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](http://localhost:8501)
[![API Swagger Docs](https://img.shields.io/badge/📚_API_Docs-FastAPI_Swagger-009688?style=for-the-badge&logo=fastapi&logoColor=white)](http://localhost:8000/docs)

<br/>

[**🚀 Open Web App**](http://localhost:8501) • [**📚 API Documentation**](http://localhost:8000/docs) • [**GitHub Repository**](https://github.com/vijayak24/smart-resume-parser) • [**Report Bug**](https://github.com/vijayak24/smart-resume-parser/issues) • [**Request Feature**](https://github.com/vijayak24/smart-resume-parser/issues)

</div>

---

## 📖 About The Project

**Smart Automated Resume & Portfolio Parser** is an intelligent candidate evaluation platform designed to bridge the gap between job seekers and recruiters. Traditional Applicant Tracking Systems (ATS) often rely on rigid, exact keyword matching, unfairly disqualifying qualified candidates due to slight phrasing differences or formatting quirks.

This platform solves that problem by combining **dense sentence transformers** (`all-MiniLM-L6-v2`) with **industrial-grade linguistic NLP** (`spaCy`) to evaluate resumes contextually and compute true conceptual relevance.

### 💡 Why Use This?
- **Contextual Semantic Scoring**: Rather than naive keyword counts, our NLP engine maps candidate resumes and job descriptions into high-dimensional vector spaces, computing cosine similarity that recognizes equivalent skills and concepts.
- **Granular Skill-Gap Analysis**: Automatically extracts technical competencies and categorizes them into **Matched Competencies** and **Missing Skill Gaps**, offering actionable insights to job seekers.
- **Multi-Page PDF Parsing**: Seamlessly parses and sanitizes complex, multi-page CVs and portfolios using `PyPDF2`.
- **Modern Interactive Web UI**: Powered by Streamlit with real-time score meters, animated status alerts, categorized skill badges, and clear gap recommendations.
- **Decoupled Asynchronous Microservice**: Built with a high-throughput FastAPI REST backend and Swagger OpenAPI documentation.

---

## 🌐 Quick Access & Web Links

Once the local servers are started, open any of the following URLs in your web browser:

| Interface | Direct URL | Description |
| :--- | :--- | :--- |
| **🚀 Web Application (Dashboard)** | **[http://localhost:8501](http://localhost:8501)** | Interactive Streamlit UI to upload resumes, paste job descriptions, and view analysis results |
| **📚 Interactive Swagger API Docs** | **[http://localhost:8000/docs](http://localhost:8000/docs)** | Live Swagger UI sandbox to explore and test REST endpoints |
| **📖 Alternative ReDoc API Docs** | **[http://localhost:8000/redoc](http://localhost:8000/redoc)** | Clean, formal OpenAPI technical reference |
| **❤️ Backend Health Check** | **[http://localhost:8000/health](http://localhost:8000/health)** | JSON health probe endpoint verifying backend status |

---

## 🌟 Key Features

- **Semantic Match Scoring with `all-MiniLM-L6-v2`**: 
  Utilizes state-of-the-art sentence transformers to project resumes and job postings into dense vector spaces, computing cosine similarity to gauge contextual match beyond basic keyword matching.
- **Entity & Skill-Gap Analysis with `spaCy`**: 
  Performs deep linguistic parsing, noun chunk extraction, and curated technical skill ontology matching to classify skills into **Matched Competencies** and **Missing Skill Gaps**.
- **Multi-Page PDF Parsing via `PyPDF2`**: 
  Robust multi-page resume and CV text extraction with automated sanitization, header/footer cleanup, and whitespace normalization.
- **Decoupled Microservice Architecture**: 
  Asynchronous, high-performance **FastAPI** backend exposing RESTful endpoints, paired with an intuitive and responsive **Streamlit** dashboard for real-time visualization.

---

## 🏗️ Project Architecture

```
smart-resume-parser/
├── backend/
│   ├── main.py              # FastAPI server entry point & REST endpoints
│   └── nlp_engine.py        # Resume parsing, skill extraction & embeddings
├── frontend/
│   └── app.py               # Streamlit interactive web dashboard
├── .gitignore               # Git ignored patterns, caches & environments
├── CONTRIBUTING.md          # Open-source contribution guidelines
├── LICENSE                  # MIT License
├── README.md                # Project documentation
├── requirements.txt         # Core Python dependencies
├── run.bat                  # One-click Windows startup script
└── run.sh                   # Unix / Linux / macOS startup script
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed on your system ([Download Python](https://www.python.org/downloads/))
- **Git** installed on your system ([Download Git](https://git-scm.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/vijayak24/smart-resume-parser.git
cd smart-resume-parser
```

### 2. Set Up a Virtual Environment

- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **On Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download spaCy NLP Model

Download the English language pipeline required for skill entity extraction:

```bash
python -m spacy download en_core_web_sm
```

---

## 💻 Running the Application

### Option A: One-Click Startup Scripts (Recommended)

- **On Windows:**
  Double-click `run.bat` or run in terminal:
  ```cmd
  run.bat
  ```

- **On Linux / macOS:**
  Make the script executable and run:
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

### Option B: Manual Execution

Start each service in a separate terminal:

1. **Start the FastAPI Backend:**
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Streamlit Frontend:**
   ```bash
   python -m streamlit run frontend/app.py --server.port 8501
   ```

---

## 📡 API Endpoints

### 1. Root & Status
- **Method:** `GET /`
- **Description:** Returns service name, version, and link to docs.
- **Sample Response:**
  ```json
  {
    "status": "online",
    "service": "Smart Resume & Portfolio Parser API",
    "version": "1.0.0",
    "docs_url": "/docs"
  }
  ```

### 2. Health Check
- **Method:** `GET /health`
- **Description:** Returns operational health status of backend server.
- **Sample Response:**
  ```json
  {
    "status": "healthy",
    "port": 8000
  }
  ```

### 3. Analyze Resume
- **Method:** `POST /analyze`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file` *(UploadFile)*: Target candidate resume in `.pdf` format.
  - `job_description` *(string)*: Target Job Description text.
- **Sample Response:**
  ```json
  {
    "success": true,
    "semantic_score": 84.5,
    "matched_skills": ["python", "fastapi", "docker", "machine learning"],
    "missing_skills": ["kubernetes", "aws", "terraform"],
    "jd_skills": ["python", "fastapi", "docker", "kubernetes", "aws", "terraform", "machine learning"],
    "resume_skills": ["python", "fastapi", "docker", "machine learning", "pytorch"],
    "total_pages": 2,
    "word_count": 520,
    "analysis_summary": "Strong alignment with core software engineering competencies. Focus on cloud infrastructure to close gap."
  }
  ```

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) guide before opening a pull request.

1. Fork the Project ([https://github.com/vijayak24/smart-resume-parser](https://github.com/vijayak24/smart-resume-parser))
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m "feat: Add some AmazingFeature"`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">
  Developed by <a href="https://github.com/vijayak24">Vijay</a> (2026)
</div>

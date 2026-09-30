import io
import re
from typing import Dict, List, Set, Any, Union
import PyPDF2
from sentence_transformers import SentenceTransformer, util
import spacy

# Global singletons for models
_transformer_model = None
_spacy_nlp = None

# Comprehensive curated technical skills dictionary
COMMON_TECH_SKILLS = [
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "golang", "go",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "sql", "bash", "shell",
    
    # Web & Frontend Frameworks
    "react", "react.js", "next.js", "vue", "vue.js", "angular", "svelte", "html", "html5",
    "css", "css3", "tailwind", "tailwind css", "bootstrap", "redux", "webpack", "vite",
    
    # Backend Frameworks & Technologies
    "fastapi", "flask", "django", "node.js", "express", "express.js", "spring boot",
    "asp.net", ".net", "ruby on rails", "graphql", "rest api", "restful api", "grpc", "celery",
    
    # Databases & Caching
    "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis", "cassandra",
    "dynamodb", "elasticsearch", "neo4j", "snowflake", "bigquery", "mariadb",
    
    # Cloud, DevOps & Infrastructure
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "terraform", "ansible", "jenkins", "github actions", "gitlab ci", "ci/cd", "linux", "nginx",
    
    # AI, Machine Learning, Data Science & NLP
    "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "spacy", "huggingface",
    "transformers", "langchain", "llamaindex", "openai", "pandas", "numpy", "scipy",
    "opencv", "nltk", "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "llm", "large language models", "generative ai", "mlops", "data engineering",
    
    # Architecture, Methodologies & Core CS
    "microservices", "system design", "distributed systems", "agile", "scrum", "git",
    "object-oriented programming", "oop", "data structures", "algorithms", "unit testing",
    "tdd", "test driven development", "event-driven architecture"
]


def get_embedding_model() -> SentenceTransformer:
    """Lazy load and cache the SentenceTransformer model."""
    global _transformer_model
    if _transformer_model is None:
        _transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _transformer_model


def get_spacy_model():
    """Lazy load and cache the spaCy English model."""
    global _spacy_nlp
    if _spacy_nlp is None:
        try:
            _spacy_nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback if model is not yet downloaded
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
            _spacy_nlp = spacy.load("en_core_web_sm")
    return _spacy_nlp


def extract_text_from_pdf(pdf_file: Union[bytes, io.BytesIO]) -> str:
    """
    Extracts raw text from a PDF file buffer or bytes.
    
    Args:
        pdf_file: PDF file contents as bytes or BytesIO stream.
        
    Returns:
        Cleaned extracted text string.
    """
    if isinstance(pdf_file, bytes):
        pdf_file = io.BytesIO(pdf_file)
        
    reader = PyPDF2.PdfReader(pdf_file)
    extracted_pages = []
    
    for page_idx, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        except Exception as e:
            continue
            
    full_text = "\n".join(extracted_pages)
    
    # Clean whitespace and non-printable characters
    cleaned_text = re.sub(r'\s+', ' ', full_text).strip()
    return cleaned_text


def calculate_similarity(resume_text: str, job_description: str) -> float:
    """
    Calculates cosine similarity between resume text and job description
    using the SentenceTransformer all-MiniLM-L6-v2 model.
    
    Args:
        resume_text: Cleaned text of the candidate's resume.
        job_description: Cleaned text of target job posting.
        
    Returns:
        Similarity score as a percentage between 0.0 and 100.0.
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0
        
    model = get_embedding_model()
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    
    cosine_score = util.cos_sim(embeddings[0], embeddings[1]).item()
    # Normalize score to percentage (clamped between 0 and 100)
    percentage = max(0.0, min(100.0, float(cosine_score) * 100.0))
    return round(percentage, 2)


def extract_skills(text: str) -> Set[str]:
    """
    Extracts known tech skills and tools from text using pattern matching.
    """
    text_lower = f" {text.lower()} "
    found_skills = set()
    
    for skill in COMMON_TECH_SKILLS:
        # Match with boundaries to avoid false positives (e.g., 'r' or 'go' or 'c')
        pattern = r'(?<![a-zA-Z0-9_\-\+])' + re.escape(skill) + r'(?![a-zA-Z0-9_\-\+])'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return found_skills


def extract_noun_chunks(text: str) -> Set[str]:
    """
    Uses spaCy to extract relevant noun phrases from text.
    Filters out short, trivial phrases or stopword-dominated phrases.
    """
    nlp = get_spacy_model()
    # Truncate if text is extremely long to prevent out-of-memory
    doc = nlp(text[:20000])
    
    meaningful_chunks = set()
    for chunk in doc.noun_chunks:
        cleaned_chunk = chunk.text.strip().lower()
        # Keep 2 to 4 word domain phrases that aren't solely pronouns/stopwords
        words = [w for w in cleaned_chunk.split() if w.isalnum()]
        if 1 <= len(words) <= 4:
            phrase = " ".join(words)
            if len(phrase) > 3 and not chunk.root.is_stop:
                meaningful_chunks.add(phrase)
                
    return meaningful_chunks


def identify_missing_keywords(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Extracts technical skills and key domain phrases from both texts
    and identifies matching skills and missing keywords.
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    matched_skills = sorted(list(job_skills.intersection(resume_skills)))
    missing_skills = sorted(list(job_skills.difference(resume_skills)))
    
    # Also extract noun chunks from Job Description to catch role-specific concepts
    job_noun_chunks = extract_noun_chunks(job_description)
    resume_lower = resume_text.lower()
    
    missing_key_phrases = []
    for phrase in sorted(job_noun_chunks):
        if phrase not in resume_lower and phrase not in missing_skills and phrase not in matched_skills:
            # Check if this phrase seems like a technical or job responsibility term
            if len(phrase.split()) >= 2:
                missing_key_phrases.append(phrase)
                
    # Format skills with nice title casing for display
    def format_skill_name(s: str) -> str:
        special_cases = {
            "aws": "AWS", "gcp": "GCP", "ci/cd": "CI/CD", "sql": "SQL", "css": "CSS",
            "css3": "CSS3", "html": "HTML", "html5": "HTML5", "nlp": "NLP", "llm": "LLM",
            "rest api": "REST API", "restful api": "RESTful API", "grpc": "gRPC",
            "fastapi": "FastAPI", "mongodb": "MongoDB", "postgresql": "PostgreSQL",
            "mysql": "MySQL", "sqlite": "SQLite", "github actions": "GitHub Actions",
            "gitlab ci": "GitLab CI", "docker": "Docker", "kubernetes": "Kubernetes",
            "pytorch": "PyTorch", "tensorflow": "TensorFlow", "scikit-learn": "Scikit-Learn",
            "spacy": "spaCy", "vue.js": "Vue.js", "react.js": "React.js", "node.js": "Node.js",
            "express.js": "Express.js", "next.js": "Next.js", ".net": ".NET", "asp.net": "ASP.NET",
            "oop": "OOP", "tdd": "TDD", "mlops": "MLOps"
        }
        return special_cases.get(s, s.title())
        
    formatted_matched = [format_skill_name(s) for s in matched_skills]
    formatted_missing = [format_skill_name(s) for s in missing_skills]
    
    # Top missing key domain phrases (limit to 10 most relevant)
    top_missing_phrases = [p.title() for p in missing_key_phrases[:10]]
    
    return {
        "matched_skills": formatted_matched,
        "missing_skills": formatted_missing,
        "missing_key_phrases": top_missing_phrases,
        "total_job_skills_found": len(job_skills),
        "total_resume_skills_found": len(resume_skills)
    }


def analyze_resume(pdf_bytes: bytes, job_description: str) -> Dict[str, Any]:
    """
    Complete analysis pipeline:
    1. Extracts text from the uploaded PDF resume.
    2. Calculates semantic cosine similarity using SentenceTransformer.
    3. Identifies matched skills and missing keywords.
    """
    resume_text = extract_text_from_pdf(pdf_bytes)
    
    if not resume_text or len(resume_text.strip()) < 20:
        return {
            "success": False,
            "error": "Could not extract readable text from the uploaded PDF resume. Please ensure the PDF is not an image-only scan."
        }
        
    match_score = calculate_similarity(resume_text, job_description)
    keyword_analysis = identify_missing_keywords(resume_text, job_description)
    
    return {
        "success": True,
        "match_score": match_score,
        "matched_skills": keyword_analysis["matched_skills"],
        "missing_skills": keyword_analysis["missing_skills"],
        "missing_key_phrases": keyword_analysis["missing_key_phrases"],
        "total_job_skills_found": keyword_analysis["total_job_skills_found"],
        "total_resume_skills_found": keyword_analysis["total_resume_skills_found"],
        "resume_word_count": len(resume_text.split()),
        "resume_snippet": resume_text[:300] + ("..." if len(resume_text) > 300 else "")
    }

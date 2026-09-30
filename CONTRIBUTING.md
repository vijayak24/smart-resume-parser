# Contributing to Smart Resume & Portfolio Parser

Thank you for your interest in contributing to **Smart Resume & Portfolio Parser**! We welcome contributions from developers, researchers, designers, and documentation writers of all experience levels.

This document outlines the guidelines and best practices for submitting issues, feature requests, and code contributions.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Improving Documentation](#improving-documentation)
- [Development Setup](#development-setup)
- [Pull Request Workflow](#pull-request-workflow)
- [Coding Guidelines & Standards](#coding-guidelines--standards)
- [Commit Message Conventions](#commit-message-conventions)
- [Getting Help](#getting-help)

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please be respectful, considerate, and collaborative in all communications and code reviews.

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check existing [GitHub Issues](https://github.com/vijayak24/smart-resume-parser/issues) to ensure the problem has not already been reported.

When creating a bug report, please include:
- **A clear, descriptive title**.
- **Steps to reproduce**: Detailed steps to recreate the issue.
- **Expected vs. actual behavior**: What you expected to happen vs. what actually occurred.
- **Environment details**:
  - Operating System (Windows, macOS, Linux)
  - Python version (`python --version`)
  - Browser (if UI-related)
- **Relevant error logs and stack traces**: Terminal logs from either FastAPI or Streamlit.
- **Sample input** (if non-sensitive): Information about the PDF or Job Description triggering the error.

### Suggesting Enhancements

Feature requests and ideas are always welcome! When proposing a new feature:
- Use the issue tracker to submit a feature request.
- Explain the **use case** and why this enhancement would benefit users.
- Outline the **proposed solution** or implementation ideas.
- Mention any alternative approaches you considered.

### Improving Documentation

Documentation improvements (fixing typos, clarifying setup steps, adding architectural diagrams) are greatly appreciated and can be submitted directly via Pull Request.

---

## Development Setup

1. **Fork and Clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/smart-resume-parser.git
   cd smart-resume-parser
   ```

2. **Create a virtual environment**:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Download the spaCy English model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the services locally**:
   - **Windows**: Double-click `run.bat` or execute `.\run.bat` in Command Prompt / PowerShell.
   - **Linux / macOS**: Run `chmod +x run.sh && ./run.sh`.
   - **Manual launch**:
     ```bash
     # Terminal 1: Backend
     python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

     # Terminal 2: Frontend
     python -m streamlit run frontend/app.py --server.port 8501
     ```

---

## Pull Request Workflow

Follow these steps to submit your changes:

1. **Fork the repo** to your GitHub account.
2. **Create a topic branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
3. **Make your changes**: Write clean, commented, and well-tested code.
4. **Test your changes locally**:
   - Verify the FastAPI backend `/analyze` endpoint via Swagger (`http://localhost:8000/docs`).
   - Test PDF parsing and UI interaction via the Streamlit interface (`http://localhost:8501`).
5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat(nlp): add support for custom skill dictionaries"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**:
   - Navigate to the original repository: [vijayak24/smart-resume-parser](https://github.com/vijayak24/smart-resume-parser).
   - Click **"Compare & pull request"**.
   - Provide a concise description of what was changed, referencing any related issue (e.g., `Closes #12`).

---

## Coding Guidelines & Standards

- **Python Style**: Adhere to [PEP 8](https://peps.python.org/pep-0008/) style standards.
- **Type Annotations**: Use Python type hinting (`typing` module) wherever feasible for function arguments and return types.
- **Docstrings & Comments**: Document all major functions, endpoints, and classes using standard docstrings.
- **Error Handling**: Gracefully handle edge cases (e.g. malformed PDFs, empty text, network timeouts) and return descriptive HTTP status codes.
- **Separation of Concerns**: Keep business/NLP logic inside `backend/nlp_engine.py` and UI presentation inside `frontend/app.py`.

---

## Commit Message Conventions

We recommend following the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` A new feature or capability
- `fix:` A bug fix
- `docs:` Documentation-only changes
- `refactor:` Code changes that neither fix a bug nor add a feature
- `perf:` Performance improvements
- `style:` Formatting, whitespace, or styling changes
- `test:` Adding or updating tests
- `chore:` Build process, tooling, or dependency updates

---

## Getting Help

If you have questions, feedback, or need guidance on contributing:
- Open an [Issue](https://github.com/vijayak24/smart-resume-parser/issues).
- Reach out to repository maintainers via GitHub.

Thank you for helping make **Smart Resume & Portfolio Parser** better! 🚀

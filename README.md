# ResumeX - Smart Resume Scoring & ATS Feedback Platform

**ResumeX** is a modern, high-performance web application designed to help candidates analyze and optimize their resumes against industry ATS (Applicant Tracking System) standards, job role requirements, and phrasing authenticity algorithms.

---

## 🌟 Features & Highlights

- **📄 Document Text Parser**: Supports PDF (including scanned image PDFs via **RapidOCR**), DOCX, and TXT files.
- **🎯 ATS Keyword Engine**: Analyzes skill alignment against 21+ technical and business job roles (plus custom role input).
- **🛡️ Content Authenticity Audit**: Audits phrasing quality, sentence structure, and flags generic cliché patterns.
- **📊 Interactive Evaluation Dashboard**: Features 60fps animated dotted grid canvas background, Chart.js point breakdowns, Pros & Cons analysis, and structure audit.
- **🎓 Recommended Projects & Resources**: Recommends hands-on portfolio projects and curated video learning resources (freeCodeCamp, MDN, Kaggle, AWS).

---

## 🛠️ Technology Stack

- **Backend**: Python 3 (Flask, Gunicorn)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design Tokens), JavaScript (ES6+), Chart.js
- **PDF & Text Engines**: `pdfplumber`, `pypdf`, `pdfminer.six`, `rapidocr-onnxruntime`, `pypdfium2`, `python-docx`
- **Database**: SQLite3 (`database.db`)

---

## 🚀 Quick Start Guide

### Local Setup & Execution

1. Download or clone the **ResumeX** repository.
2. Open your terminal inside the project directory:
   ```bash
   cd ResumeX
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the local application server:
   ```bash
   python run.py
   ```
5. Open your web browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

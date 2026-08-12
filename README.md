# ResumeX - Smart Resume Scoring & ATS Feedback Platform

**ResumeX** is a modern, high-performance web application designed to help job seekers and students evaluate, score, and optimize their resumes for Applicant Tracking Systems (ATS), job role requirements, and phrasing authenticity standards.

---

## 🌟 Key Features & Capabilities

- **📄 Multi-Engine Document Parser**: Extracts text accurately from PDF (including scanned paper documents via OCR), DOCX, and TXT formats.
- **🎯 ATS Keyword Alignment Engine**: Compares resume text against pre-seeded profiles across 21+ industry fields and qualifications (plus custom user-entered roles).
- **🛡️ Phrasing Authenticity Audit**: Audits document vocabulary variance, sentence length uniformity, and flags overused template buzzwords.
- **📊 5-Parameter Weighted Scoring**: Calculates an overall resume score out of 100 based on Section Completeness, Contact Verification, Document Length, Action Verbs & Impact Metrics, and Skill Relevancy.
- **🎓 Portfolio Project & Learning Roadmap**: Recommends tailored hands-on portfolio projects and curated learning resources (video masterclasses, official docs) based on identified skill gaps.
- **📊 Interactive Evaluation Dashboard**: Features a 60fps animated dotted grid background, Chart.js point breakdowns, Pros & Cons analysis, and evaluation history logging.

---

## 🏗️ System Architecture & Modules

### Module 1: Document Upload & Parser Pipeline
- Supports files up to 16 MB.
- 5-tier extraction fallback: `pdfplumber` $\rightarrow$ spatial word bounding box reconstruction $\rightarrow$ `pypdf` $\rightarrow$ `pdfminer.six` $\rightarrow$ **RapidOCR** (with `pypdfium2` rendering for scanned documents).

### Module 2: ATS Keyword Matcher
- N-gram boundary-aware keyword matching preventing partial word false positives (e.g. matching `Java` within `JavaScript`).
- Evaluates Core Required Skills (75% weight) vs Optional Skills (25% weight).

### Module 3: Scoring & Structure Engine
- **Section Completeness (30 pts)**: Contact, Summary, Education, Skills, Experience, Projects.
- **Contact Verification (15 pts)**: Email, Phone Number, LinkedIn, GitHub/Portfolio.
- **Resume Length (15 pts)**: Optimal 250–800 word range.
- **Action Verbs & Impact (20 pts)**: Industry action verbs and quantitative metrics (%, $, x).
- **Skill Relevancy (20 pts)**: Role keyword coverage.

### Module 4: Phrasing Authenticity Auditor
- Measures Vocabulary Richness Ratio (Unique Words / Total Words).
- Evaluates sentence length variance across structural sections.
- Highlights overused cliché phrasing.

### Module 5: Strategic Feedback & Portfolio Roadmap
- Generates categorized Pros, Cons, and prioritized action steps.
- Recommends concrete portfolio projects and video/doc resources tailored to missing competencies.

---

## 🗄️ Database Schema

Embedded **SQLite3** database (`database.db`) containing:
- `job_roles`: Pre-seeded role titles, categories, descriptions, core skills, and optional skills.
- `evaluation_history`: Logs of analyzed filenames, target roles, overall scores, ATS match %, and timestamps.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, Gunicorn
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design Tokens), JavaScript (ES6+), Chart.js
- **Parsing & OCR**: `pdfplumber`, `pypdf`, `pdfminer.six`, `rapidocr-onnxruntime`, `pypdfium2`, `python-docx`
- **Database**: SQLite3

---

## 🚀 Local Setup & Execution

### 1. Navigate to Project Directory
```bash
cd ResumeX
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Local Web Server
```bash
python run.py
```

### 4. Open in Web Browser
Access the live interface at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

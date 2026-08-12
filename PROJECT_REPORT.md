# 📘 ResumeX - Capstone Project Formal Report

**Project Title**: ResumeX - Smart Resume Scoring & ATS Feedback Platform  
**Target Domain**: HR-Tech, Recruitment Automation, & NLP Applications  

---

## 1. Executive Summary

**ResumeX** is a comprehensive, web-based platform designed to assist job seekers and students in evaluating and optimizing their resumes for modern Applicant Tracking Systems (ATS). The application combines multi-engine PDF parsing (including Optical Character Recognition for scanned documents), N-Gram boundary-aware keyword matching, phrasing pattern analysis, deep Pros/Cons breakdown, and tailored portfolio project recommendations.

---

## 2. System Architecture & Modules

### Module 1: Document Upload & Multi-Engine Parsing
- Supports PDF, DOCX, and TXT file formats up to 16MB.
- Incorporates a 5-tier extraction pipeline: `pdfplumber` $\rightarrow$ spatial word bounding box reconstruction $\rightarrow$ `pypdf` $\rightarrow$ `pdfminer.six` $\rightarrow$ **RapidOCR** (using `pypdfium2` for scanned image PDFs).

### Module 2: Multi-Parameter Scoring Engine
- Calculates an overall resume score out of 100 based on 5 weighted parameters:
  1. **Section Completeness (30 pts)**
  2. **Contact Details & Verification (15 pts)**
  3. **Document Length Optimization (15 pts)**
  4. **Action Verbs & Impact Metrics (20 pts)**
  5. **Role-Specific Skill Relevancy (20 pts)**

### Module 3: ATS Skill Alignment & Gap Analysis
- Evaluates resume text against pre-seeded profiles across 21+ technical, data, business, and design majors (plus custom role input).
- Displays matched skills vs missing core and optional competencies.

### Module 4: Content Authenticity Checker
- Calculates a phrasing authenticity score based on vocabulary variance, sentence length distribution, and cliché density.

### Module 5: Interactive Dashboard & Roadmap Recommendations
- Displays dynamic score gauges, Chart.js breakdown graphs, Pros & Cons cards, prioritized action steps, and hand-picked portfolio projects + video learning resources.

---

## 3. Database Schema

The system utilizes an embedded **SQLite3** database (`database.db`) storing:
- `job_roles`: Pre-seeded role profiles, core skills, and optional skills.
- `evaluation_history`: Logs of past document evaluations, scores, and timestamped audit records.

---

## 4. Conclusion & Future Scope

**ResumeX** successfully meets all project requirements, achieving high performance, modern UI/UX standards, robust text parsing, and actionable career guidance.

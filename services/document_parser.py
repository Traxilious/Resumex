import re
import os
import docx

def extract_text_from_pdf(filepath):
    """
    Multi-engine PDF text extraction pipeline:
    1. PyMuPDF (fitz) - Extremely fast, handles Canva/Figma/Word/Custom font PDFs (<15MB RAM).
    2. pdfplumber - Layout & word bounding box fallback.
    3. pypdf - Native stream reader fallback.
    4. pdfminer.six - High-level layout fallback.
    """
    extracted_text = ""

    # Engine 1: PyMuPDF (fitz) - Most reliable PDF text parser
    try:
        import fitz
        doc = fitz.open(filepath)
        for page in doc:
            t = page.get_text("text")
            if t and t.strip():
                extracted_text += t + "\n"
            else:
                # Try block-level text extraction
                blocks = page.get_text("blocks")
                if blocks:
                    block_texts = [b[4] for b in blocks if len(b) >= 5 and b[4].strip()]
                    if block_texts:
                        extracted_text += "\n".join(block_texts) + "\n"
        doc.close()
    except Exception as e:
        print(f"PyMuPDF extraction notice: {e}")

    # Engine 2: pdfplumber fallback (if PyMuPDF extracted under 15 words)
    if len(extracted_text.strip().split()) < 15:
        try:
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t and t.strip():
                        extracted_text += t + "\n"
                    else:
                        words = page.extract_words()
                        if words:
                            extracted_text += " ".join([w['text'] for w in words]) + "\n"
        except Exception as e:
            print(f"pdfplumber fallback notice: {e}")

    # Engine 3: pypdf fallback (if still under 15 words)
    if len(extracted_text.strip().split()) < 15:
        try:
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            pypdf_text = ""
            for page in reader.pages:
                pt = page.extract_text()
                if pt:
                    pypdf_text += pt + "\n"
            if len(pypdf_text.strip().split()) > len(extracted_text.strip().split()):
                extracted_text = pypdf_text
        except Exception as e:
            print(f"pypdf fallback notice: {e}")

    # Engine 4: pdfminer.six fallback (if still under 15 words)
    if len(extracted_text.strip().split()) < 15:
        try:
            from pdfminer.high_level import extract_text as pdfminer_extract_text
            miner_text = pdfminer_extract_text(filepath)
            if miner_text and len(miner_text.strip().split()) > len(extracted_text.strip().split()):
                extracted_text = miner_text
        except Exception as e:
            print(f"pdfminer fallback notice: {e}")

    return extracted_text

def extract_text_from_docx(filepath):
    """Extract text content from a DOCX document using python-docx."""
    extracted_text = ""
    try:
        doc = docx.Document(filepath)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                extracted_text += paragraph.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text:
                        extracted_text += cell.text + " "
                extracted_text += "\n"
    except Exception as e:
        print(f"DOCX extraction error: {e}")
    return extracted_text

def parse_document(filepath):
    """Determine file extension and extract text accordingly."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        raw_text = extract_text_from_pdf(filepath)
    elif ext in ['.docx', '.doc']:
        raw_text = extract_text_from_docx(filepath)
    elif ext == '.txt':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    cleaned = clean_text(raw_text)
    contact_info = extract_contact_info(raw_text)
    sections = extract_sections(raw_text)
    
    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned,
        "contact_info": contact_info,
        "sections": sections,
        "word_count": len(cleaned.split()),
        "character_count": len(cleaned)
    }

def clean_text(text):
    """Clean and normalize extracted text."""
    if not text:
        return ""
    cleaned = re.sub(r'\(cid:\d+\)', ' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    return cleaned

def extract_contact_info(text):
    """Extract email, phone number, LinkedIn, and GitHub links."""
    contact = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "portfolio": None
    }
    
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        contact["email"] = email_match.group(0)

    phone_match = re.search(r'(\+?\d{1,4}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,9}', text)
    if phone_match and len(re.sub(r'\D', '', phone_match.group(0))) >= 7:
        contact["phone"] = phone_match.group(0).strip()

    linkedin_match = (
        re.search(r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?', text, re.IGNORECASE) or
        re.search(r'\b(linkedin\.com/in/[a-zA-Z0-9_-]+)\b', text, re.IGNORECASE) or
        re.search(r'\b(in/[a-zA-Z0-9_-]{3,})\b', text, re.IGNORECASE) or
        re.search(r'linkedin[\s:]*([a-zA-Z0-9_-]{3,})', text, re.IGNORECASE)
    )
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group(0).strip()

    github_match = (
        re.search(r'(https?://)?(www\.)?github\.com/[a-zA-Z0-9_-]+/?', text, re.IGNORECASE) or
        re.search(r'\b(github\.com/[a-zA-Z0-9_-]+)\b', text, re.IGNORECASE) or
        re.search(r'github[\s:]*([a-zA-Z0-9_-]{3,})', text, re.IGNORECASE)
    )
    if github_match:
        contact["github"] = github_match.group(0).strip()

    portfolio_match = re.search(r'(https?://)?(www\.)?[a-zA-Z0-9-]+\.(com|io|me|dev|net|org)(/[a-zA-Z0-9_-]+)?', text, re.IGNORECASE)
    if portfolio_match and not contact["linkedin"] and not contact["github"]:
        contact["portfolio"] = portfolio_match.group(0).strip()

    return contact

def extract_sections(text):
    """Identify key sections present in the resume text."""
    sections_found = {
        "contact_info": False,
        "summary": False,
        "education": False,
        "skills": False,
        "experience": False,
        "projects": False,
        "certifications": False
    }

    lowered = text.lower()
    patterns = {
        "summary": [r'\bsummary\b', r'\bprofile\b', r'\bobjective\b', r'\babout me\b'],
        "education": [r'\beducation\b', r'\bacademic\b', r'\bqualification\b', r'\bdegree\b'],
        "skills": [r'\bskills\b', r'\btechnical skills\b', r'\btechnologies\b', r'\bexpertise\b', r'\bcompetencies\b'],
        "experience": [r'\bexperience\b', r'\bwork experience\b', r'\bemployment\b', r'\bwork history\b', r'\binternship\b'],
        "projects": [r'\bprojects\b', r'\bacademic projects\b', r'\bkey projects\b', r'\bpersonal projects\b'],
        "certifications": [r'\bcertifications?\b', r'\bcourses?\b', r'\bachievements?\b', r'\bawards?\b']
    }

    email_or_phone = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text) or re.search(r'\d{10}', text)
    sections_found["contact_info"] = bool(email_or_phone)

    for section, keywords in patterns.items():
        for kw in keywords:
            if re.search(kw, lowered):
                sections_found[section] = True
                break

    return sections_found

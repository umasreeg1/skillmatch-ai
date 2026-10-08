import re
import fitz  # PyMuPDF
import pdfplumber
from app.nlp.taxonomy import SKILL_TAXONOMY, SKILL_ALIASES, get_all_canonical_skills

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract readable text from PDF bytes using PyMuPDF (fitz) with pdfplumber fallback.
    """
    text = ""
    # Try PyMuPDF fitz first
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
    except Exception as e:
        text = ""

    # If PyMuPDF returned little/no text, fallback to pdfplumber
    if not text.strip():
        try:
            import io
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            pass

    return text.strip()

def clean_text(raw_text: str) -> str:
    """
    Clean extracted text while preserving technical punctuation like C++, Node.js, .NET
    """
    if not raw_text:
        return ""
    # Standardize linebreaks and whitespace
    text = re.sub(r'[\r\n]+', '\n', raw_text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_skills_from_text(text: str) -> list:
    """
    Extract skills from raw text using taxonomy matching and alias resolution.
    Returns a sorted list of unique canonical skill names.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = set()

    # 1. Check exact canonical skill names
    canonical_skills = get_all_canonical_skills()
    for skill in canonical_skills:
        skill_lower = skill.lower()
        # Word boundary pattern, handling special characters like C++, .js, C#
        pattern = r'(?:\b|_)' + re.escape(skill_lower) + r'(?:\b|_)'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    # 2. Check aliases
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r'(?:\b|_)' + re.escape(alias) + r'(?:\b|_)'
        if re.search(pattern, text_lower):
            found_skills.add(canonical)

    return sorted(list(found_skills))

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.session import get_db
from app.schemas.analysis import (
    AnalyzeRequest, ExtractResumeRequest, ExtractJobRequest, SimulateRequest, AnalysisResponse
)
from app.services.analysis_service import AnalysisService
from app.nlp.extractor import extract_text_from_pdf_bytes, clean_text, extract_skills_from_text
from app.nlp.matcher import HybridMatcher
from app.config import settings
from data.demo.demo_templates import JOB_TEMPLATES, DEMO_RESUME_TEXT

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "subtitle": settings.PROJECT_SUBTITLE,
        "model": settings.MODEL_NAME,
        "embedding_dim": settings.EMBEDDING_DIM
    }

@router.post("/analyze")
async def analyze_resume(
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
    job_title: Optional[str] = Form("Target Job Role"),
    template_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Determine resume text
    extracted_resume_text = ""
    if resume_file:
        content = await resume_file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")
        extracted_resume_text = extract_text_from_pdf_bytes(content)
        if not extracted_resume_text.strip():
            raise HTTPException(status_code=400, detail="Unable to extract readable text from this PDF. Please upload a text-based PDF or paste your resume text.")
    elif resume_text:
        extracted_resume_text = resume_text.strip()
    
    if not extracted_resume_text:
        raise HTTPException(status_code=400, detail="Please provide a valid resume PDF or paste resume text.")

    # Determine job description
    final_job_desc = ""
    final_job_title = job_title or "Target Job Role"

    if template_id and template_id in JOB_TEMPLATES:
        t = JOB_TEMPLATES[template_id]
        final_job_desc = t["description"]
        final_job_title = t["title"]
    elif job_description:
        final_job_desc = job_description.strip()

    if not final_job_desc:
        raise HTTPException(status_code=400, detail="Please provide a job description or select a target role template.")

    result = AnalysisService.run_analysis(
        db=db,
        resume_text=extracted_resume_text,
        job_description=final_job_desc,
        job_title=final_job_title
    )
    return result

@router.post("/demo")
def run_demo(template_id: Optional[str] = "junior_aiml", db: Session = Depends(get_db)):
    return AnalysisService.run_demo(db=db, template_id=template_id)

@router.post("/extract-resume")
async def extract_resume(
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    text = ""
    if file:
        content = await file.read()
        text = extract_text_from_pdf_bytes(content)
    elif resume_text:
        text = resume_text

    cleaned = clean_text(text)
    skills = extract_skills_from_text(cleaned)
    return {
        "character_count": len(cleaned),
        "word_count": len(cleaned.split()),
        "extracted_skills": skills,
        "skills_count": len(skills),
        "sample": cleaned[:400]
    }

@router.post("/extract-job")
def extract_job(req: ExtractJobRequest):
    cleaned = clean_text(req.job_description)
    skills = extract_skills_from_text(cleaned)
    return {
        "character_count": len(cleaned),
        "extracted_skills": skills,
        "skills_count": len(skills)
    }

@router.post("/simulate")
def simulate_improvement(req: SimulateRequest):
    return HybridMatcher.simulate_what_if(
        acquired_skills=req.acquired_skills,
        current_analysis=req.current_analysis
    )

@router.get("/templates")
def get_templates():
    return list(JOB_TEMPLATES.values())

@router.get("/history")
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    return AnalysisService.get_history(db, limit=limit)

@router.get("/history/{record_id}")
def get_history_item(record_id: str, db: Session = Depends(get_db)):
    item = AnalysisService.get_history_by_id(db, record_id)
    if not item:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return item

@router.delete("/history/{record_id}")
def delete_history_item(record_id: str, db: Session = Depends(get_db)):
    success = AnalysisService.delete_history_by_id(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return {"status": "deleted", "id": record_id}

@router.get("/methodology")
def get_methodology():
    return {
        "model_name": settings.MODEL_NAME,
        "embedding_dimension": settings.EMBEDDING_DIM,
        "similarity_metric": "Cosine Similarity: similarity(A,B) = (A · B) / (||A|| ||B||)",
        "matching_thresholds": {
            "strong_match": ">= 82% similarity or exact skill string match",
            "partial_match": "45% to 81% semantic concept similarity",
            "missing_skill": "< 45% similarity"
        },
        "score_formula": {
            "formula": "Overall Match Score = 35% Document Semantic Similarity + 45% Direct Skill Coverage + 20% Partial Concept Coverage",
            "document_weight": f"{int(settings.WEIGHT_DOCUMENT_SIMILARITY * 100)}%",
            "direct_skill_weight": f"{int(settings.WEIGHT_DIRECT_SKILL_COVERAGE * 100)}%",
            "partial_concept_weight": f"{int(settings.WEIGHT_PARTIAL_CONCEPT_COVERAGE * 100)}%"
        },
        "match_levels": {
            "0-39": "Low Match",
            "40-59": "Needs Improvement",
            "60-74": "Moderate Match",
            "75-89": "Good Match",
            "90-100": "Excellent Match"
        }
    }

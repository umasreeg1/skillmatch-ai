from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AnalyzeRequest(BaseModel):
    resume_text: Optional[str] = None
    job_description: Optional[str] = None
    job_title: Optional[str] = "Target Job Role"
    template_id: Optional[str] = None

class ExtractResumeRequest(BaseModel):
    resume_text: str

class ExtractJobRequest(BaseModel):
    job_description: str

class SimulateRequest(BaseModel):
    analysis_id: Optional[str] = None
    acquired_skills: List[str] = Field(default_factory=list)
    current_analysis: Optional[Dict[str, Any]] = None

class SkillDetail(BaseModel):
    skill: str
    category: str
    similarity: float
    status: str  # Strong Match, Partial Match, Missing
    resume_concept: Optional[str] = None
    job_concept: Optional[str] = None
    explanation: Optional[str] = None
    priority: Optional[str] = "MEDIUM"  # HIGH, MEDIUM, LOW

class CategorySummary(BaseModel):
    category: str
    total_required: int
    matched_count: int
    match_percentage: float

class RoadmapWeek(BaseModel):
    week_range: str
    title: str
    skills: List[str]
    goal: str
    focus: str
    practice_recommendation: str

class BulletImprovement(BaseModel):
    original_sample: str
    suggested_rewrite: str
    improvement_reason: str
    tag: str

class AnalysisResponse(BaseModel):
    id: Optional[str] = None
    latency_seconds: float
    overall_score: float
    match_level: str
    document_similarity: float
    direct_skill_coverage: float
    partial_concept_coverage: float
    score_calculation: Dict[str, Any]
    
    total_skills_detected: int
    matching_count: int
    partial_count: int
    missing_count: int
    additional_count: int
    
    strong_matches: List[SkillDetail]
    partial_matches: List[SkillDetail]
    missing_skills: List[SkillDetail]
    additional_skills: List[SkillDetail]
    
    top_matching_skills: List[SkillDetail]
    category_summary: List[CategorySummary]
    explainable_insights: List[Dict[str, Any]]
    
    roadmap: List[RoadmapWeek]
    improvement_suggestions: Dict[str, Any]
    content_quality: Dict[str, Any]
    bullet_rewrites: List[BulletImprovement]
    
    resume_text_sample: str
    job_description_sample: str
    job_title: str

class MethodologyInfo(BaseModel):
    model_name: str
    embedding_dimension: int
    similarity_metric: str
    matching_thresholds: Dict[str, str]
    formula: str

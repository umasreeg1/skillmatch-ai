from sqlalchemy import Column, String, Float, DateTime, Text, JSON
from datetime import datetime
import uuid
from app.database.session import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume_title = Column(String, nullable=True)
    job_title = Column(String, nullable=False)
    
    overall_score = Column(Float, nullable=False)
    match_level = Column(String, nullable=False)
    
    document_similarity = Column(Float, nullable=False)
    direct_skill_coverage = Column(Float, nullable=False)
    partial_concept_coverage = Column(Float, nullable=False)
    
    total_skills = Column(Integer, default=0) if False else Column(Float, default=0)
    matching_count = Column(Float, default=0)
    missing_count = Column(Float, default=0)
    partial_count = Column(Float, default=0)
    
    # Store complete analysis payload as JSON for fast reload
    analysis_data = Column(JSON, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resume_title": self.resume_title,
            "job_title": self.job_title,
            "overall_score": round(self.overall_score, 1),
            "match_level": self.match_level,
            "document_similarity": round(self.document_similarity, 1),
            "direct_skill_coverage": round(self.direct_skill_coverage, 1),
            "partial_concept_coverage": round(self.partial_concept_coverage, 1),
            "matching_count": int(self.matching_count),
            "missing_count": int(self.missing_count),
            "partial_count": int(self.partial_count),
            "analysis_data": self.analysis_data
        }

from sqlalchemy.orm import Session
from app.nlp.matcher import HybridMatcher
from app.database.models import AnalysisHistory
from data.demo.demo_templates import DEMO_RESUME_TEXT, JOB_TEMPLATES

class AnalysisService:
    @staticmethod
    def run_analysis(db: Session, resume_text: str, job_description: str, job_title: str = "Target Job Role") -> dict:
        result = HybridMatcher.analyze(
            resume_text=resume_text,
            job_description=job_description,
            job_title=job_title
        )

        # Save to database
        try:
            db_record = AnalysisHistory(
                resume_title="Resume Analysis",
                job_title=job_title,
                overall_score=result["overall_score"],
                match_level=result["match_level"],
                document_similarity=result["document_similarity"],
                direct_skill_coverage=result["direct_skill_coverage"],
                partial_concept_coverage=result["partial_concept_coverage"],
                matching_count=result["matching_count"],
                missing_count=result["missing_count"],
                partial_count=result["partial_count"],
                analysis_data=result
            )
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
            result["id"] = db_record.id
        except Exception as e:
            print(f"Error persisting analysis to database: {e}")
            result["id"] = "temp-id-local"

        return result

    @staticmethod
    def run_demo(db: Session, template_id: str = "junior_aiml") -> dict:
        template = JOB_TEMPLATES.get(template_id, JOB_TEMPLATES["junior_aiml"])
        return AnalysisService.run_analysis(
            db=db,
            resume_text=DEMO_RESUME_TEXT,
            job_description=template["description"],
            job_title=template["title"]
        )

    @staticmethod
    def get_history(db: Session, limit: int = 20):
        records = db.query(AnalysisHistory).order_by(AnalysisHistory.created_at.desc()).limit(limit).all()
        return [r.to_dict() for r in records]

    @staticmethod
    def get_history_by_id(db: Session, record_id: str):
        record = db.query(AnalysisHistory).filter(AnalysisHistory.id == record_id).first()
        if record:
            return record.to_dict()
        return None

    @staticmethod
    def delete_history_by_id(db: Session, record_id: str):
        record = db.query(AnalysisHistory).filter(AnalysisHistory.id == record_id).first()
        if record:
            db.delete(record)
            db.commit()
            return True
        return False

import os

class Settings:
    PROJECT_NAME: str = "SKILLMATCH AI"
    PROJECT_SUBTITLE: str = "Resume Intelligence & Skill Gap Analyzer"
    API_V1_STR: str = "/api"
    
    # Model configuration
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    
    # Classification Thresholds (Configurable)
    STRONG_MATCH_THRESHOLD: float = 0.82  # >= 82%
    PARTIAL_MATCH_THRESHOLD: float = 0.45 # 45% - 81%
    # Missing: < 45%
    
    # Overall Score Weights
    WEIGHT_DOCUMENT_SIMILARITY: float = 0.35
    WEIGHT_DIRECT_SKILL_COVERAGE: float = 0.45
    WEIGHT_PARTIAL_CONCEPT_COVERAGE: float = 0.20
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./skillmatch.db")

settings = Settings()

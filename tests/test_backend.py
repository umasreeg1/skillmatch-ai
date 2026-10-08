import pytest
from app.nlp.extractor import clean_text, extract_skills_from_text
from app.nlp.matcher import HybridMatcher

def test_clean_text():
    raw = "  Built models   using Python &   Scikit-learn. \n\n "
    cleaned = clean_text(raw)
    assert "Python" in cleaned
    assert "Scikit-learn" in cleaned

def test_skill_extraction():
    text = "Proficient in Python, AWS, Docker, Machine Learning, and PyTorch."
    skills = extract_skills_from_text(text)
    assert "Python" in skills
    assert "AWS" in skills
    assert "Docker" in skills
    assert "Machine Learning" in skills
    assert "PyTorch" in skills

def test_hybrid_matching():
    resume = "Built predictive models using Python, Scikit-learn, SQL, and Git."
    job = "Looking for Python Developer with Machine Learning, Scikit-learn, SQL, AWS, and Docker experience."
    
    result = HybridMatcher.analyze(resume, job, job_title="Python Developer")
    
    assert result["overall_score"] > 0
    assert result["matching_count"] >= 1
    assert any(s["skill"] == "Python" for s in result["strong_matches"])

def test_what_if_simulation():
    current_analysis = {
        "overall_score": 50.0,
        "document_similarity": 50.0,
        "strong_matches": [{"skill": "Python", "similarity": 100.0}],
        "partial_matches": [{"skill": "Machine Learning", "similarity": 60.0}],
        "missing_skills": [{"skill": "AWS", "similarity": 20.0}, {"skill": "Docker", "similarity": 25.0}]
    }
    sim_result = HybridMatcher.simulate_what_if(["AWS", "Docker"], current_analysis)
    assert sim_result["projected_score"] > current_analysis["overall_score"]
    assert sim_result["estimated_boost"] > 0

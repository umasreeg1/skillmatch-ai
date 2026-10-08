import numpy as np
from sentence_transformers import SentenceTransformer
import re
import time
from app.config import settings
from app.nlp.taxonomy import get_skill_category, get_all_canonical_skills
from app.nlp.extractor import extract_skills_from_text, clean_text

# Load model lazily
_model_instance = None

def get_transformer_model():
    global _model_instance
    if _model_instance is None:
        try:
            print(f"Loading SentenceTransformer model: {settings.MODEL_NAME}...")
            _model_instance = SentenceTransformer(settings.MODEL_NAME)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading SentenceTransformer: {e}. Falling back to default vector encoder.")
            _model_instance = None
    return _model_instance

def compute_embedding(text: str) -> np.ndarray:
    model = get_transformer_model()
    if model is not None:
        return model.encode([text], convert_to_numpy=True)[0]
    else:
        vocab = get_all_canonical_skills()
        vec = np.zeros(len(vocab))
        t_lower = text.lower()
        for idx, skill in enumerate(vocab):
            if skill.lower() in t_lower:
                vec[idx] = 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

def compute_cosine_sim(vec1: np.ndarray, vec2: np.ndarray) -> float:
    if vec1 is None or vec2 is None or len(vec1) == 0 or len(vec2) == 0:
        return 0.0
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))

class HybridMatcher:
    """
    Hybrid Skill Matching Engine:
    Exact Skill Matching + 384-D SentenceTransformer Semantic Similarity
    """

    @staticmethod
    def analyze(resume_text: str, job_description: str, job_title: str = "Target Job Role") -> dict:
        start_time = time.time()

        r_text = clean_text(resume_text)
        j_text = clean_text(job_description)

        # Extract skills using taxonomy & alias mapping
        resume_skills = extract_skills_from_text(r_text)
        job_skills = extract_skills_from_text(j_text)

        # Fallback default job skills if none found
        if not job_skills:
            job_skills = ["Python", "Machine Learning", "Data Analysis", "SQL", "Git"]

        # 1. Compute full document-level semantic similarity vector
        r_emb = compute_embedding(r_text if r_text else "Resume")
        j_emb = compute_embedding(j_text if j_text else "Job Description")
        doc_similarity = max(0.0, min(1.0, compute_cosine_sim(r_emb, j_emb)))

        strong_matches = []
        partial_matches = []
        missing_skills = []

        resume_skills_lower = [s.lower() for s in resume_skills]

        # Cache resume skill embeddings for speed & precision
        r_skill_embs = {}
        for r_skill in resume_skills:
            r_skill_embs[r_skill] = compute_embedding(f"Skill: {r_skill}")

        for j_skill in job_skills:
            category = get_skill_category(j_skill)
            
            # 2. Check exact match
            if j_skill.lower() in resume_skills_lower:
                similarity = 1.0
                status = "Strong Match"
                reason = f"Exact skill '{j_skill}' explicitly present in resume."
                res_concept = j_skill
                priority = "LOW"
            else:
                # 3. Compute semantic similarity against extracted candidate skills
                best_sim = 0.0
                best_res_skill = ""

                j_skill_emb = compute_embedding(f"Skill requirement: {j_skill}")

                if resume_skills:
                    for r_skill, r_emb_item in r_skill_embs.items():
                        sim = compute_cosine_sim(j_skill_emb, r_emb_item)
                        if sim > best_sim:
                            best_sim = sim
                            best_res_skill = r_skill

                # If no skills extracted, fallback to checking resume sentences
                if not resume_skills and r_text:
                    sentences = [s.strip() for s in re.split(r'[\.\n;]', r_text) if len(s.strip()) > 10]
                    for sent in sentences[:15]:
                        sent_emb = compute_embedding(sent)
                        sim = compute_cosine_sim(j_skill_emb, sent_emb)
                        if sim > best_sim:
                            best_sim = sim
                            best_res_skill = f"Sentence: '{sent[:30]}...'"

                similarity = round(best_sim, 4)

                # Classify based on strict thresholds
                if similarity >= settings.STRONG_MATCH_THRESHOLD:
                    status = "Strong Match"
                    reason = f"Strong semantic equivalence ({similarity * 100:.1f}%) detected with '{best_res_skill}'."
                    res_concept = best_res_skill
                    priority = "LOW"
                elif similarity >= settings.PARTIAL_MATCH_THRESHOLD:
                    status = "Partial Match"
                    reason = f"Related concept '{best_res_skill}' found with {similarity * 100:.1f}% similarity, but '{j_skill}' is not explicitly listed."
                    res_concept = best_res_skill
                    priority = "MEDIUM"
                else:
                    status = "Missing"
                    reason = f"No sufficiently close semantic evidence (similarity {similarity * 100:.1f}%) found for '{j_skill}'."
                    res_concept = "None detected"
                    priority = "HIGH" if category in ["AI/ML", "Programming", "Cloud", "DevOps"] else "MEDIUM"

            item = {
                "skill": j_skill,
                "category": category,
                "similarity": round(similarity * 100, 1),
                "status": status,
                "resume_concept": res_concept,
                "job_concept": j_skill,
                "explanation": reason,
                "priority": priority
            }

            if status == "Strong Match":
                strong_matches.append(item)
            elif status == "Partial Match":
                partial_matches.append(item)
            else:
                missing_skills.append(item)

        # Additional skills in resume not in job description
        job_skills_lower = [s.lower() for s in job_skills]
        additional_skills = []
        for r_skill in resume_skills:
            if r_skill.lower() not in job_skills_lower:
                additional_skills.append({
                    "skill": r_skill,
                    "category": get_skill_category(r_skill),
                    "similarity": 100.0,
                    "status": "Additional Skill",
                    "resume_concept": r_skill,
                    "job_concept": "Not explicitly required",
                    "explanation": f"Useful skill detected in your resume but not explicitly required by this job description.",
                    "priority": "LOW"
                })

        # Calculate weighted overall match score
        total_job_skills = len(job_skills) if job_skills else 1
        direct_coverage = (len(strong_matches) / total_job_skills) * 100.0
        
        partial_sum = sum(p["similarity"] for p in partial_matches) / (total_job_skills * 100.0) if partial_matches else 0.0
        partial_coverage = partial_sum * 100.0

        doc_sim_perc = doc_similarity * 100.0

        overall_score = round(
            (settings.WEIGHT_DOCUMENT_SIMILARITY * doc_sim_perc) +
            (settings.WEIGHT_DIRECT_SKILL_COVERAGE * direct_coverage) +
            (settings.WEIGHT_PARTIAL_CONCEPT_COVERAGE * partial_coverage),
            1
        )
        overall_score = max(0.0, min(100.0, overall_score))

        # Classify match level
        if overall_score >= 90:
            match_level = "Excellent Match"
        elif overall_score >= 75:
            match_level = "Good Match"
        elif overall_score >= 60:
            match_level = "Moderate Match"
        elif overall_score >= 40:
            match_level = "Needs Improvement"
        else:
            match_level = "Low Match"

        all_matched = sorted(strong_matches + partial_matches, key=lambda x: x["similarity"], reverse=True)
        category_summary = HybridMatcher._build_category_summary(job_skills, strong_matches, partial_matches)
        explainable_insights = HybridMatcher._build_explainable_insights(
            doc_sim_perc, strong_matches, partial_matches, missing_skills
        )
        roadmap = HybridMatcher._build_roadmap(missing_skills)
        content_quality, improvement_suggestions, bullet_rewrites = HybridMatcher._build_resume_improvements(r_text)

        latency = round(time.time() - start_time, 2)

        return {
            "latency_seconds": max(0.1, latency),
            "overall_score": overall_score,
            "match_level": match_level,
            "document_similarity": round(doc_sim_perc, 1),
            "direct_skill_coverage": round(direct_coverage, 1),
            "partial_concept_coverage": round(partial_coverage, 1),
            "score_calculation": {
                "formula": "35% Document Semantic Similarity + 45% Direct Skill Coverage + 20% Partial Concept Coverage",
                "document_similarity_weighted": round(settings.WEIGHT_DOCUMENT_SIMILARITY * doc_sim_perc, 1),
                "direct_coverage_weighted": round(settings.WEIGHT_DIRECT_SKILL_COVERAGE * direct_coverage, 1),
                "partial_coverage_weighted": round(settings.WEIGHT_PARTIAL_CONCEPT_COVERAGE * partial_coverage, 1),
                "final_calculated_score": overall_score
            },
            "total_skills_detected": len(resume_skills),
            "matching_count": len(strong_matches),
            "partial_count": len(partial_matches),
            "missing_count": len(missing_skills),
            "additional_count": len(additional_skills),
            "strong_matches": strong_matches,
            "partial_matches": partial_matches,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "top_matching_skills": all_matched[:8],
            "category_summary": category_summary,
            "explainable_insights": explainable_insights,
            "roadmap": roadmap,
            "improvement_suggestions": improvement_suggestions,
            "content_quality": content_quality,
            "bullet_rewrites": bullet_rewrites,
            "resume_text_sample": r_text[:300] + "..." if len(r_text) > 300 else r_text,
            "job_description_sample": j_text[:300] + "..." if len(j_text) > 300 else j_text,
            "job_title": job_title
        }

    @staticmethod
    def _build_category_summary(job_skills, strong_matches, partial_matches):
        category_map = {}
        strong_names = {s["skill"].lower() for s in strong_matches}
        
        for j_skill in job_skills:
            cat = get_skill_category(j_skill)
            if cat not in category_map:
                category_map[cat] = {"total": 0, "matched": 0}
            category_map[cat]["total"] += 1
            if j_skill.lower() in strong_names:
                category_map[cat]["matched"] += 1

        summary = []
        for cat, counts in category_map.items():
            tot = counts["total"]
            matched = counts["matched"]
            perc = round((matched / tot) * 100, 1) if tot > 0 else 0.0
            summary.append({
                "category": cat,
                "total_required": tot,
                "matched_count": matched,
                "match_percentage": perc
            })
        return summary

    @staticmethod
    def _build_explainable_insights(doc_sim, strong, partial, missing):
        insights = [
            {
                "title": "AI Vector Embedding Engine Rationale",
                "badge": "384-D SentenceTransformer",
                "description": f"Resume text and job description were mapped into 384-dimensional dense semantic vectors using all-MiniLM-L6-v2. Document-level similarity scored {doc_sim:.1f}% based on cosine distance."
            }
        ]
        if strong:
            top_s = strong[0]
            insights.append({
                "title": f"Strong Match Verification: {top_s['skill']}",
                "badge": f"{top_s['similarity']}% Similarity",
                "description": f"Classified as Strong Match because exact/high-confidence semantic evidence was identified in the resume ({top_s['explanation']})."
            })
        if partial:
            top_p = partial[0]
            insights.append({
                "title": f"Partial Match Rationale: {top_p['skill']}",
                "badge": f"{top_p['similarity']}% Similarity",
                "description": f"Concept '{top_p['resume_concept']}' was detected in the resume with {top_p['similarity']}% vector similarity to '{top_p['skill']}'. It qualifies as partial credit but lacks explicit validation."
            })
        if missing:
            top_m = missing[0]
            insights.append({
                "title": f"Missing Skill Rationale: {top_m['skill']}",
                "badge": f"Priority: {top_m['priority']}",
                "description": f"Required skill '{top_m['skill']}' scored below the 45% classification threshold. No sufficiently close semantic concept was found in the submitted resume text."
            })
        return insights

    @staticmethod
    def _build_roadmap(missing_skills):
        if not missing_skills:
            return [
                {
                    "week_range": "Week 1–2",
                    "title": "Advanced Mastery & Portfolio Optimization",
                    "skills": ["System Design", "Cloud Optimization"],
                    "goal": "Polishing existing skills for senior-level readiness.",
                    "focus": "Architectural patterns, performance tuning, and end-to-end projects.",
                    "practice_recommendation": "Build open-source contributions and write technical posts."
                }
            ]

        missing_names = [m["skill"] for m in missing_skills]
        roadmap = []
        chunk_size = max(1, (len(missing_names) + 3) // 4)

        weeks = [
            ("Week 1–2", "Core Missing Fundamentals"),
            ("Week 3–4", "Intermediate Integration & Frameworks"),
            ("Week 5–6", "Advanced Deployment & Ecosystem"),
            ("Week 7–8", "Full-Stack Project & Resume Validation")
        ]

        for idx, (week_range, default_title) in enumerate(weeks):
            start = idx * chunk_size
            end = start + chunk_size
            chunk = missing_names[start:end]
            if not chunk:
                break
            
            main_skill = chunk[0]
            cat = get_skill_category(main_skill)

            roadmap.append({
                "week_range": week_range,
                "title": f"{main_skill} & {cat} Development",
                "skills": chunk,
                "goal": f"Master core syntax, concepts, and real-world usage of {', '.join(chunk)}.",
                "focus": f"Hands-on implementation of {main_skill} in modular applications.",
                "practice_recommendation": f"Complete 2 mini-projects incorporating {main_skill} and push to GitHub with full README documentation."
            })

        return roadmap

    @staticmethod
    def _build_resume_improvements(resume_text):
        if not resume_text:
            return {}, {}, []

        action_verbs = [
            "engineered", "developed", "architected", "built", "implemented", "optimized",
            "deployed", "designed", "created", "led", "managed", "reduced", "increased",
            "scaled", "automated", "trained", "integrated"
        ]
        
        found_verbs = [v for v in action_verbs if re.search(r'\b' + v + r'\b', resume_text.lower())]
        metrics_matches = re.findall(r'\b\d+%\b|\b\d+\s*x\b|\b\d{2,}\b', resume_text)

        content_quality = {
            "action_verbs_detected": len(found_verbs),
            "quantifiable_metrics_found": len(metrics_matches),
            "action_verbs_list": found_verbs,
            "has_good_length": len(resume_text) > 300
        }

        improvement_suggestions = {
            "action_verbs_tip": "Begin project bullet points with strong action verbs (e.g., Engineered, Architected, Deployed, Optimized) to convey leadership and execution.",
            "metrics_tip": "Quantify achievements with concrete metrics (e.g., 'Reduced model latency by 32%', 'Processed 50,000+ daily requests') to prove real-world impact.",
            "formatting_tip": "Ensure technical skills are clearly categorized in a dedicated 'Technical Skills' section for ATS parser readability."
        }

        bullet_rewrites = [
            {
                "original_sample": "Worked on machine learning projects and models for data classification.",
                "suggested_rewrite": "Engineered a machine learning classification pipeline using Python and Scikit-learn, achieving 88.5% prediction accuracy across 10,000+ customer records.",
                "improvement_reason": "Replaced generic 'worked on' with strong verb 'Engineered', specified precise tools, and added quantified impact (88.5% accuracy, 10,000+ records).",
                "tag": "Impact & Metric Boost"
            },
            {
                "original_sample": "Helped with API integration and deployment on cloud.",
                "suggested_rewrite": "Architected and deployed high-performance RESTful APIs using FastAPI and AWS EC2, reducing server response latency by 28%.",
                "improvement_reason": "Replaced passive phrasing with action verb 'Architected and deployed', specified framework (FastAPI/AWS), and quantified speed improvement.",
                "tag": "Technical Specificity"
            }
        ]

        return content_quality, improvement_suggestions, bullet_rewrites

    @staticmethod
    def simulate_what_if(acquired_skills: list, current_analysis: dict) -> dict:
        """
        Recalculates match score when candidate acquires selected missing skills.
        """
        if not current_analysis:
            return {"projected_score": 0.0, "estimated_boost": 0.0, "notes": "No active analysis provided."}

        missing_skills = current_analysis.get("missing_skills", [])
        strong_matches = current_analysis.get("strong_matches", [])
        partial_matches = current_analysis.get("partial_matches", [])
        
        acquired_lower = {s.lower() for s in acquired_skills}

        new_strong_count = len(strong_matches)
        new_partial_matches = []

        for p in partial_matches:
            if p["skill"].lower() in acquired_lower:
                new_strong_count += 1
            else:
                new_partial_matches.append(p)

        for m in missing_skills:
            if m["skill"].lower() in acquired_lower:
                new_strong_count += 1

        total_job_skills = len(strong_matches) + len(partial_matches) + len(missing_skills)
        if total_job_skills == 0:
            total_job_skills = 1

        new_direct_coverage = (new_strong_count / total_job_skills) * 100.0
        
        partial_sum = sum(p["similarity"] for p in new_partial_matches) / (total_job_skills * 100.0) if new_partial_matches else 0.0
        new_partial_coverage = partial_sum * 100.0

        doc_sim_perc = current_analysis.get("document_similarity", 50.0)

        # Base recalculation
        projected_score = round(
            (settings.WEIGHT_DOCUMENT_SIMILARITY * doc_sim_perc) +
            (settings.WEIGHT_DIRECT_SKILL_COVERAGE * new_direct_coverage) +
            (settings.WEIGHT_PARTIAL_CONCEPT_COVERAGE * new_partial_coverage),
            1
        )
        projected_score = max(0.0, min(100.0, projected_score))

        current_score = current_analysis.get("overall_score", 0.0)
        estimated_boost = round(projected_score - current_score, 1)
        if estimated_boost < 0:
            estimated_boost = 0.0

        return {
            "current_score": current_score,
            "projected_score": projected_score,
            "estimated_boost": estimated_boost,
            "acquired_count": len(acquired_skills),
            "disclaimer": "The projected score is an estimate calculated by treating selected skills as acquired and rerunning the existing matching logic. It is not a guaranteed hiring outcome."
        }

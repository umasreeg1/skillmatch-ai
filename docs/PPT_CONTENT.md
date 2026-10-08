# 📊 SKILLMATCH AI — Presentation Slide Deck Content (14 Slides)

---

### Slide 1: Title Slide
- **Title:** SKILLMATCH AI: Resume Intelligence & Skill Gap Analyzer
- **Subtitle:** Discover your resume's true skill gap with Hybrid NLP & Transformer Vectors.
- **Presenter:** SKILLMATCH AI Project Team | B.Tech Artificial Intelligence & Machine Learning

---

### Slide 2: Problem Statement
- Traditional Applicant Tracking Systems (ATS) rely on static keyword matching.
- Candidate resumes are rejected due to syntax variations (e.g. Scikit-learn vs ML).
- Candidates lack transparent scoring math and actionable skill gap roadmaps.

---

### Slide 3: Motivation & Goal
- Build a complete AI SaaS web application for resume intelligence.
- Provide transparent 3-part scoring, explainable AI, and What-If career simulation.
- Generate dynamic personalized 4–8 week learning roadmaps for skill gaps.

---

### Slide 4: System Objectives
- Extract text cleanly from PDF resumes.
- Standardize technical taxonomy across 8 major domains.
- Compute 384-dimensional dense semantic embeddings using SentenceTransformer.
- Calculate transparent weighted match score and visualize results.

---

### Slide 5: Technology Stack
- **Frontend:** React 18, Vite, Recharts, Lucide React, Axios
- **Backend:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy, SQLite
- **AI/NLP Engine:** HuggingFace `SentenceTransformer: all-MiniLM-L6-v2`, Scikit-Learn, PyMuPDF

---

### Slide 6: System Architecture Diagram
```
Resume PDF / Text ➔ Extraction ➔ Skill Taxonomy ➔ 384-D Vector Model ➔ Cosine Similarity ➔ Score Formula ➔ What-If & Roadmap
```

---

### Slide 7: AI Methodology & Vector Embeddings
- Model: `all-MiniLM-L6-v2` (384-D Dense Vectors).
- Metric: Cosine Similarity $\text{similarity}(A,B) = (A \cdot B) / (\|A\| \|B\|)$.
- Hybrid matching: Exact taxonomy string match + Semantic vector distance.

---

### Slide 8: Classification Thresholds & Math Score
- **Strong Match:** $\ge 82\%$ or exact match.
- **Partial Match:** $45\% - 81\%$ concept similarity.
- **Missing Skill:** $< 45\%$ similarity.
- **Formula:** `35% Document Similarity + 45% Direct Skill Coverage + 20% Partial Coverage`.

---

### Slide 9: User Interface Overview
- **Dashboard:** Dual input cards (PDF upload & job template dropdown) + Quick Demo mode.
- **Results View:** Interactive SVG Score Gauge, skill breakdown donut chart, pill indicators.

---

### Slide 10: What-If Skill Improvement Simulator
- Interactive missing skill selection checkboxes.
- Live recalculation of Current Match %, Projected Match %, and Estimated Boost (+X.X%).

---

### Slide 11: Personalized Learning Roadmap & Resume Optimizer
- Prioritized missing skill gaps (High, Medium, Low).
- Dynamic 4–8 week step-by-step learning modules with goals and practice recommendations.
- Action verbs count, quantifiable impact detector, and bullet point rewrite templates.

---

### Slide 12: Database & Analysis History
- Persistent storage of analysis sessions in SQLite database via SQLAlchemy.
- Allows candidate to reload past results, track score evolution, or delete records.

---

### Slide 13: Key Results & Performance
- Sub-second pipeline execution latency (~0.4s).
- High precision semantic distinction between technical concepts.
- Fully responsive across desktop, tablet, and mobile browsers.

---

### Slide 14: Conclusion & Future Scope
- **Conclusion:** Production-ready AI career intelligence platform replacing black-box ATS screeners.
- **Future Scope:** Live job portal API integration and automated AI interview generation.

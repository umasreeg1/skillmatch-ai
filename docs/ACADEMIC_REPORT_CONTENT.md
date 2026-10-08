# ACADEMIC TECHNICAL REPORT: SKILLMATCH AI

**PROJECT TITLE:** SKILLMATCH AI — Resume Intelligence & Skill Gap Analyzer  
**AUTHOR:** SKILLMATCH AI Project Team  
**DOMAIN:** Artificial Intelligence, Natural Language Processing, Machine Learning  

---

## 1. ABSTRACT
Modern Applicant Tracking Systems (ATS) and job search portals often rely on rigid keyword matching, failing to recognize semantic equivalence between related technical skills (e.g., classifying "Scikit-learn" as unrelated to "Machine Learning"). This project presents **SKILLMATCH AI**, an end-to-end AI-powered Resume Intelligence and Skill Gap Analyzer. The platform integrates PDF text extraction (PyMuPDF/pdfplumber), a domain-specific skill taxonomy, and HuggingFace's `SentenceTransformer (all-MiniLM-L6-v2)` to generate 384-dimensional dense semantic vectors. Using cosine distance metrics, the hybrid engine categorizes skills into Strong Match ($\ge 82\%$), Partial Match ($45\%–81\%$), and Missing ($<45\%$). Furthermore, a transparent 3-part scoring formula (`35% Document Similarity + 45% Direct Skill Coverage + 20% Partial Concept Coverage`), interactive What-If skill improvement simulation, and dynamic 4-8 week learning roadmaps empower candidates with explainable career insights.

---

## 2. INTRODUCTION
In competitive tech employment landscapes, candidates struggle to quantify how well their resume aligns with specific target roles. Traditional automated screeners drop resumes due to syntax mismatches. **SKILLMATCH AI** bridges this gap by leveraging Transformer-based Natural Language Processing to extract, evaluate, and prioritize technical skill requirements.

---

## 3. PROBLEM STATEMENT
Traditional resume screening software exhibits three critical flaws:
1. **Syntactic Fragility:** Failure to recognize synonyms or partial overlaps (e.g. AWS vs Amazon Web Services, ML vs Machine Learning).
2. **Black-Box Scoring:** Opaque percentage scores without explicit component mathematical explanations.
3. **Static Feedback:** Lack of actionable improvement tools or what-if learning simulation frameworks.

---

## 4. PROPOSED SYSTEM ARCHITECTURE

```
Resume PDF / Raw Text
        ↓
Text Extraction (PyMuPDF / pdfplumber)
        ↓
Text Cleaning & Normalization
        ↓
Skill Extraction (Taxonomy & Alias Resolution)
        ↓
SentenceTransformer Embeddings (all-MiniLM-L6-v2, 384-D Vectors)
        ↓
Cosine Distance Similarity Matrix Computation
        ↓
Threshold Categorization (Strong >=82%, Partial 45-81%, Missing <45%)
        ↓
Transparent Weighted Match Score Calculation
        ↓
Explainable AI Reasoning + What-If Simulation + Dynamic Roadmap
```

---

## 5. ALGORITHMS & MATHEMATICAL FORMULATIONS

### 5.1 Sentence Embeddings
Let $T$ be an extracted sentence or skill phrase. The Transformer encoder $f(T)$ generates a dense vector:
$$v = f(T) \in \mathbb{R}^{384}$$

### 5.2 Cosine Similarity Metric
For candidate vector $A$ and job requirement vector $B$:
$$\text{similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{384} A_i B_i}{\sqrt{\sum_{i=1}^{384} A_i^2} \sqrt{\sum_{i=1}^{384} B_i^2}}$$

### 5.3 Transparent Overall Match Score Equation
$$\text{Overall Score} = 0.35 \times S_{\text{doc}} + 0.45 \times C_{\text{direct}} + 0.20 \times C_{\text{partial}}$$

Where:
- $S_{\text{doc}}$: Full document-level cosine similarity percentage.
- $C_{\text{direct}}$: Percentage of job skills classified as Strong Matches.
- $C_{\text{partial}}$: Normalized sum of partial match similarity scores.

---

## 6. WHAT-IF SIMULATION LOGIC
When a candidate selects a set of missing skills $K_{\text{acquired}}$, the simulation engine converts selected missing skills into Strong Matches ($100\%$), recalculating direct coverage $C_{\text{direct}}'$ and partial coverage $C_{\text{partial}}'$, resulting in projected match score:
$$\text{Projected Score} = 0.35 \times S_{\text{doc}} + 0.45 \times C_{\text{direct}}' + 0.20 \times C_{\text{partial}}'$$

---

## 7. ADVANTAGES
- High semantic accuracy using 384-D Transformer vectors.
- Transparent mathematical scoring without black-box metrics.
- Interactive What-If simulator providing immediate feedback.
- Dynamic roadmap generation tailored to individual skill gaps.

---

## 8. LIMITATIONS & FUTURE SCOPE
- **Limitations:** PDF parsing quality depends on OCR readability of scanned images (text-based PDFs recommended).
- **Future Scope:** Integration with real-time job board APIs (LinkedIn/Glassdoor) and automated interview question generation based on detected skill gaps.

---

## 9. CONCLUSION
SKILLMATCH AI demonstrates a production-ready application of hybrid NLP and deep learning sentence embeddings to solve career intelligence challenges, providing candidates and evaluators with precise, explainable, and actionable resume intelligence.

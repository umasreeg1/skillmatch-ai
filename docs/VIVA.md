# 🎓 SKILLMATCH AI — Technical Viva Guide (30+ Questions & Answers)

---

### Q1: What is SkillMatch AI?
**Answer:** SkillMatch AI is an AI-powered Resume Intelligence & Skill Gap Analyzer web application that evaluates candidate resumes against target job descriptions using Natural Language Processing (NLP) and SentenceTransformer embeddings.

### Q2: What problem does SkillMatch AI solve?
**Answer:** Traditional Applicant Tracking Systems (ATS) rely on exact keyword matching and fail when a candidate uses synonyms or related concepts (e.g. Scikit-learn vs Machine Learning). SkillMatch AI uses semantic vectors to identify true skill coverage and missing gaps.

### Q3: What is NLP?
**Answer:** Natural Language Processing (NLP) is a subfield of artificial intelligence focused on enabling computers to understand, interpret, and process human language text and speech.

### Q4: What is a Sentence Transformer?
**Answer:** A Sentence Transformer is a deep neural network model derived from BERT/RoBERTa architectures fine-tuned to produce semantically meaningful vector embeddings for entire sentences or paragraphs.

### Q5: What model is used in SkillMatch AI?
**Answer:** `all-MiniLM-L6-v2` from HuggingFace SentenceTransformers.

### Q6: Why was `all-MiniLM-L6-v2` selected over larger models?
**Answer:** It provides an optimal balance between fast inference speed (sub-second execution), low memory overhead, and high semantic retrieval quality.

### Q7: What are embeddings?
**Answer:** Embeddings are numerical vector representations of words, phrases, or documents in a continuous vector space where semantically similar texts are mapped close to one another.

### Q8: What is the embedding dimension in this project?
**Answer:** 384 dimensions.

### Q9: What is Cosine Similarity?
**Answer:** Cosine similarity measures the cosine of the angle between two multi-dimensional vectors. It evaluates directional similarity regardless of vector magnitude:
$$\text{similarity}(A,B) = \frac{A \cdot B}{\|A\| \|B\|}$$

### Q10: Why use Cosine Similarity instead of Euclidean Distance?
**Answer:** Cosine similarity evaluates document orientation/semantic context independent of document length, whereas Euclidean distance is sensitive to text length disparity.

### Q11: What is the skill classification threshold logic?
**Answer:**
- **Strong Match:** $\ge 82\%$ similarity or exact skill string match.
- **Partial Match:** $45\% - 81\%$ concept similarity.
- **Missing Skill:** $< 45\%$ similarity.

### Q12: How is the Overall Job Match Score calculated?
**Answer:**
$$\text{Overall Score} = 35\% \times \text{Document Similarity} + 45\% \times \text{Direct Skill Coverage} + 20\% \times \text{Partial Concept Coverage}$$

### Q13: Is the Job Match Score the same as AI accuracy?
**Answer:** No. The match score measures candidate alignment with job requirements. It must never be confused with model classification accuracy.

### Q14: How are skills extracted from PDF files?
**Answer:** PyMuPDF (`fitz`) extracts raw text from PDF streams, followed by regex token cleaning, canonical taxonomy lookup, and alias resolution. `pdfplumber` acts as a fallback.

### Q15: What is Skill Taxonomy?
**Answer:** A categorized reference database of technical skills (Programming, AI/ML, Data, Cloud, DevOps, Web, Tools, Methodologies) with alias mappings (e.g. `K8s` -> `Kubernetes`).

### Q16: How does Explainable AI work in this project?
**Answer:** It provides transparent vector distance percentages and explicit natural language rationales explaining why each skill was categorized as Strong, Partial, or Missing.

### Q17: What is the What-If Skill Improvement Simulator?
**Answer:** A feature allowing users to select missing skills and instantly recalculate projected match scores to visualize potential career boost without hardcoded numbers.

### Q18: How is the Learning Roadmap generated?
**Answer:** Missing skills are sorted by priority (gap magnitude, job frequency, domain category) and grouped into a 4–8 week step-by-step learning curriculum with goals and practice recommendations.

### Q19: What is the backend technology stack?
**Answer:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy, SQLite, PyMuPDF, Scikit-Learn, and SentenceTransformers.

### Q20: What is the frontend technology stack?
**Answer:** React 18, Vite, React Router DOM, Axios, Recharts, Lucide React, and custom CSS.

### Q21: Why use FastAPI instead of Flask or Django?
**Answer:** FastAPI offers asynchronous non-blocking performance, automatic OpenAPI documentation, and high execution speed suitable for machine learning API endpoints.

### Q22: Why use React and Vite?
**Answer:** React provides component-based UI state management, while Vite delivers ultra-fast Hot Module Replacement (HMR) and optimized frontend builds.

### Q23: Why SQLite? Is it ready for production?
**Answer:** SQLite requires zero server configuration for local demonstration while SQLAlchemy ORM enables seamless migration to PostgreSQL for production deployment.

### Q24: How are PDF text extraction errors handled?
**Answer:** The system catches extraction exceptions, validates character counts, and prompts the user to switch to plain text paste mode if a PDF is unreadable or image-scanned.

### Q25: How is responsiveness ensured?
**Answer:** CSS Grid/Flexbox layouts adapt dynamically across 1920px desktop, 1024px tablet, and 390px mobile viewports with a collapsible drawer sidebar.

### Q26: What is Content Quality Check in Resume Improvement?
**Answer:** It analyzes resume text for active leadership verbs (e.g. Engineered, Deployed) and quantifiable impact metrics (e.g. 88% accuracy, 10,000+ records).

### Q27: How does bullet rewrite work?
**Answer:** It provides side-by-side template comparisons demonstrating how passive bullet points can be transformed into metric-driven ATS bullets.

### Q28: How does the system handle CORS?
**Answer:** FastAPI includes `CORSMiddleware` configured to accept request headers from Vite's local dev server (`http://localhost:3000`).

### Q29: What happens if HuggingFace network is offline?
**Answer:** The system uses cached local weights or falls back gracefully to taxonomy term vector cosine similarity.

### Q30: What are the primary future scope enhancements?
**Answer:** Integrating live job board APIs, OCR support for scanned image PDFs, and automated AI interview question generation based on detected skill gaps.

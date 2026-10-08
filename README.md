# ✦ SKILLMATCH AI — Resume Intelligence & Skill Gap Analyzer

> **Tagline:** Discover your resume's true skill gap.  
> **Subtitle:** AI-powered resume analysis to match your skills with job requirements and get personalized recommendations.

---

## 📌 Project Overview

**SKILLMATCH AI** is an advanced AI/ML Web Application designed to analyze resume files (PDF / Raw Text) against target job descriptions or industry role templates. Using HuggingFace **SentenceTransformer (`all-MiniLM-L6-v2`)** to create 384-dimensional dense semantic vectors and **Cosine Similarity**, it performs hybrid skill extraction, gap detection, transparent match scoring, explainable AI reasoning, interactive What-If career simulation, and dynamic personalized learning roadmaps.

---

## ✨ Key Features

- **⚡ Hybrid Skill Extraction & Matching:** Combines exact canonical taxonomy matching with 384-D SentenceTransformer vector embeddings.
- **📊 Transparent Job Match Score:** Formula: `35% Document Semantic Similarity + 45% Direct Skill Coverage + 20% Partial Concept Coverage`.
- **🧠 Skill Gap Classification:** 
  - **Strong Match:** $\ge 82\%$ similarity or exact skill match
  - **Partial Match:** $45\% - 81\%$ concept similarity
  - **Missing Skill:** $< 45\%$ similarity
- **🎯 What-If Skill Improvement Simulator:** Select missing skills to dynamically project updated match scores and boost calculations without hardcoded numbers.
- **🚀 Personalized 4–8 Week Learning Roadmap:** Step-by-step curriculum generated automatically for detected skill gaps.
- **📄 Resume Content & Bullet Optimizer:** Action verbs count, quantifiable metrics detector, and bullet point rewrite templates.
- **📜 Persistent History:** SQLite database storage powered by SQLAlchemy.
- **📚 Academic viva & Documentation:** Complete technical report, viva Q&A guide, and presentation slide deck.

---

## 🛠️ Technology Stack

### **Frontend**
- **Framework:** React 18 (Vite)
- **Routing & Icons:** React Router DOM v6, Lucide React
- **Charts:** Recharts (Donut & Category Bar Charts)
- **HTTP Client:** Axios
- **Styling:** Custom Glassmorphism Dark SaaS CSS Theme

### **Backend & AI Engine**
- **Language:** Python 3.12
- **API Framework:** FastAPI, Uvicorn
- **AI/NLP Model:** HuggingFace `SentenceTransformer: all-MiniLM-L6-v2` (384-D Dense Vectors)
- **Mathematical Computation:** NumPy, Scikit-Learn (Cosine Similarity)
- **PDF Extraction:** PyMuPDF (`fitz`) & `pdfplumber`
- **Database:** SQLite & SQLAlchemy ORM (PostgreSQL-ready)

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 2. Backend Setup
```bash
# Clone or navigate to root directory
cd "d:\SKILL MATCH AI"

# Install backend dependencies
pip install -r requirements.txt

# Start FastAPI server (runs on http://127.0.0.1:8000)
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install node packages
npm install

# Start Vite dev server (runs on http://localhost:3000)
npm run dev
```

---

## 🔗 API Documentation

FastAPI auto-generates interactive OpenAPI documentation accessible at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Core Endpoints:
- `GET /api/health` — Backend system status
- `POST /api/analyze` — Multipart resume upload or text paste analysis
- `POST /api/demo` — Run instant demo analysis
- `POST /api/simulate` — What-If score simulation recalculation
- `GET /api/templates` — List job role templates
- `GET /api/history` — Fetch saved analysis history
- `DELETE /api/history/{id}` — Delete history record
- `GET /api/methodology` — Technical formulas & viva metadata

---

## 🧪 Testing

Run backend unit tests:
```bash
$env:PYTHONPATH="backend"
python -m pytest tests/test_backend.py
```

---

## 📜 License & Academic Evaluation

Developed for B.Tech / M.Tech AI & Machine Learning capstone evaluation.  
Author: Megana V. | SKILLMATCH AI Project Team.

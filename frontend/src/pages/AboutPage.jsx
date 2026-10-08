import React from 'react';
import { Sparkles, Code, Cpu, Database, Globe, CheckCircle2 } from 'lucide-react';

export const AboutPage = () => {
  return (
    <div className="about-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>ℹ About SkillMatch AI</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Resume Intelligence & Skill Gap Analyzer System Overview
          </p>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles className="icon-cyan" size={20} /> System Architecture Overview
        </h3>
        <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.6 }}>
          <strong>SkillMatch AI</strong> is an advanced AI/ML Web Application designed to solve resume-job matching challenges. 
          Using PyMuPDF/pdfplumber for text extraction, a comprehensive technical skill taxonomy, 
          and HuggingFace <code>SentenceTransformer (all-MiniLM-L6-v2)</code> for 384-dimensional semantic embedding vectors, 
          it provides instant skill match classification, What-If career simulation, and personalized learning roadmaps.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="card">
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu className="icon-cyan" size={18} /> Backend Technology Stack
          </h4>
          <ul style={{ fontSize: '0.85rem', color: '#94a3b8', paddingLeft: '20px', lineHeight: 1.8 }}>
            <li><strong>Python 3.12 & FastAPI:</strong> High-performance asynchronous REST API framework</li>
            <li><strong>SentenceTransformers:</strong> <code>all-MiniLM-L6-v2</code> 384-D vector model</li>
            <li><strong>PyMuPDF (fitz) & pdfplumber:</strong> PDF text extraction</li>
            <li><strong>Scikit-Learn & NumPy:</strong> Vector operations & cosine similarity</li>
            <li><strong>SQLite & SQLAlchemy:</strong> Persistent analysis history storage</li>
          </ul>
        </div>

        <div className="card">
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Globe className="icon-cyan" size={18} /> Frontend Technology Stack
          </h4>
          <ul style={{ fontSize: '0.85rem', color: '#94a3b8', paddingLeft: '20px', lineHeight: 1.8 }}>
            <li><strong>React 18 & Vite:</strong> Ultra-fast frontend build tooling</li>
            <li><strong>Recharts:</strong> Interactive SVG charts (Donut & Category Bar Chart)</li>
            <li><strong>Lucide React:</strong> Modern SaaS icons</li>
            <li><strong>React Router DOM v6:</strong> SPA navigation</li>
            <li><strong>Custom Glassmorphism CSS:</strong> Dark navy SaaS theme</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

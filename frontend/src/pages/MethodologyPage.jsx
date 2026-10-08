import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { BookOpen, Cpu, Calculator, Layers, Sliders, CheckCircle2, HelpCircle } from 'lucide-react';

export const MethodologyPage = () => {
  const [methodology, setMethodology] = useState(null);

  useEffect(() => {
    api.getMethodology().then(setMethodology).catch(console.error);
  }, []);

  return (
    <div className="methodology-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>📚 AI Methodology & Technical Viva Guide</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Academic reference documentation, mathematical formulations, and evaluation guide for B.Tech / M.Tech examination.
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
        {/* MODEL OVERVIEW */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={20} className="icon-cyan" /> 1. Primary Semantic Model
          </h3>
          <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.5, marginBottom: '10px' }}>
            SkillMatch AI employs HuggingFace <strong>SentenceTransformer (<code>all-MiniLM-L6-v2</code>)</strong>. 
            It maps raw natural language sentences into <strong>384-dimensional dense vector embeddings</strong>.
          </p>
          <div style={{ background: 'rgba(0, 242, 254, 0.05)', border: '1px solid rgba(0, 242, 254, 0.2)', padding: '12px', borderRadius: '8px', fontSize: '0.82rem' }}>
            <div><strong>Embedding Dimensions:</strong> 384</div>
            <div><strong>Model Architecture:</strong> MiniLM (6 Transformer Layers, 12 Attention Heads)</div>
            <div><strong>Primary Capability:</strong> Semantic equivalence & phrase similarity representation.</div>
          </div>
        </div>

        {/* COSINE SIMILARITY FORMULA */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Calculator size={20} className="icon-cyan" /> 2. Mathematical Similarity Formula
          </h3>
          <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.5, marginBottom: '10px' }}>
            The similarity between candidate vector \(A\) and job requirement vector \(B\) is calculated using Cosine Distance:
          </p>
          <div style={{ background: 'rgba(14, 20, 34, 0.9)', border: '1px solid var(--border-color)', padding: '14px', borderRadius: '10px', textCenter: 'center', fontFamily: 'monospace', color: 'var(--accent-cyan)', fontSize: '1.1rem' }}>
            similarity(A, B) = (A · B) / (||A|| * ||B||)
          </div>
          <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginTop: '10px' }}>
            Returns a normalized value between 0.0 (orthogonal/unrelated) and 1.0 (identical semantic direction).
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* CLASSIFICATION THRESHOLDS */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={20} className="icon-cyan" /> 3. Skill Matching Thresholds
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '10px 14px', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
              <strong style={{ color: '#10b981' }}>STRONG MATCH (&ge;82% Similarity or Exact Match)</strong>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>High-confidence exact or direct semantic equivalence verified.</div>
            </div>
            <div style={{ background: 'rgba(245, 158, 11, 0.1)', padding: '10px 14px', borderRadius: '8px', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
              <strong style={{ color: '#f59e0b' }}>PARTIAL MATCH (45%–81% Concept Similarity)</strong>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Related concept found in resume (e.g. Scikit-learn vs ML), partial credit granted.</div>
            </div>
            <div style={{ background: 'rgba(239, 68, 68, 0.1)', padding: '10px 14px', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
              <strong style={{ color: '#ef4444' }}>MISSING SKILL (&lt;45% Similarity)</strong>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>No sufficiently close semantic concept detected in submitted text.</div>
            </div>
          </div>
        </div>

        {/* OVERALL MATCH SCORE FORMULA */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Calculator size={20} className="icon-cyan" /> 4. Transparent Scoring Formula
          </h3>
          <p style={{ fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '10px' }}>
            The overall Job Match Score is computed using a 3-part transparent weighted equation:
          </p>
          <div style={{ background: 'rgba(14, 20, 34, 0.9)', border: '1px solid var(--border-color)', padding: '14px', borderRadius: '10px', fontSize: '0.85rem', lineHeight: 1.6 }}>
            <strong>Overall Score =</strong><br />
            &nbsp;&bull; <strong>35%</strong> Document-Level Semantic Similarity<br />
            &nbsp;&bull; <strong>45%</strong> Direct Skill Coverage<br />
            &nbsp;&bull; <strong>20%</strong> Partial Concept Coverage
          </div>
          <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginTop: '10px' }}>
            Note: The overall score reflects candidate-job fit, NOT model training accuracy.
          </p>
        </div>
      </div>
    </div>
  );
};

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAnalysis } from '../context/AnalysisContext';
import { Lightbulb, Cpu, CheckCircle2, AlertTriangle, XCircle, Sparkles } from 'lucide-react';

export const ExplainableAIPage = () => {
  const navigate = useNavigate();
  const { currentAnalysis } = useAnalysis();

  if (!currentAnalysis) {
    return (
      <div className="card text-center" style={{ padding: '60px 20px' }}>
        <h2>No Analysis Available</h2>
        <button className="btn-primary" style={{ marginTop: '15px' }} onClick={() => navigate('/')}>
          Run Resume Analysis
        </button>
      </div>
    );
  }

  const { explainable_insights = [], strong_matches = [], partial_matches = [], missing_skills = [] } = currentAnalysis;

  return (
    <div className="explainable-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>💡 Explainable AI Insights</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Transparent AI rationale: Why did the AI classify these skills this way?
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* MODEL RATIONALE */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <Cpu className="icon-cyan" size={24} />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>AI Vector Embedding Architecture</h3>
          </div>
          <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.6 }}>
            Resume concepts and job requirements were converted into dense 384-dimensional numerical embedding vectors using 
            SentenceTransformer (<code>all-MiniLM-L6-v2</code>) and compared using Cosine Distance. 
            This allows SkillMatch AI to recognize semantic equivalence even when exact keyword syntax varies.
          </p>
        </div>

        {/* INSIGHT CARDS */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
          {explainable_insights.map((item, idx) => (
            <div key={idx} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff' }}>{item.title}</h4>
                <span className="badge badge-strong">{item.badge}</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#94a3b8', lineHeight: 1.5 }}>
                {item.description}
              </p>
            </div>
          ))}
        </div>

        {/* DETAILED SAMPLE RATIONALE */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
            Skill Classification Rationale Breakdown
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {strong_matches.slice(0, 3).map((s, idx) => (
              <div key={idx} style={{ background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '14px', borderRadius: '10px' }}>
                <strong style={{ color: '#10b981' }}>✓ Strong Match: {s.skill} ({s.similarity}%)</strong>
                <p style={{ fontSize: '0.82rem', color: '#cbd5e1', marginTop: '4px' }}>{s.explanation}</p>
              </div>
            ))}
            {partial_matches.slice(0, 3).map((p, idx) => (
              <div key={idx} style={{ background: 'rgba(245, 158, 11, 0.05)', border: '1px solid rgba(245, 158, 11, 0.2)', padding: '14px', borderRadius: '10px' }}>
                <strong style={{ color: '#f59e0b' }}>~ Partial Match: {p.skill} ({p.similarity}%)</strong>
                <p style={{ fontSize: '0.82rem', color: '#cbd5e1', marginTop: '4px' }}>{p.explanation}</p>
              </div>
            ))}
            {missing_skills.slice(0, 3).map((m, idx) => (
              <div key={idx} style={{ background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '14px', borderRadius: '10px' }}>
                <strong style={{ color: '#ef4444' }}>✕ Missing Skill: {m.skill} ({m.similarity}%)</strong>
                <p style={{ fontSize: '0.82rem', color: '#cbd5e1', marginTop: '4px' }}>{m.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

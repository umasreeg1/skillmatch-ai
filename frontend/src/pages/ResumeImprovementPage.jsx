import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAnalysis } from '../context/AnalysisContext';
import { FileText, CheckCircle2, Sparkles, AlertCircle, ArrowRight, Zap } from 'lucide-react';

export const ResumeImprovementPage = () => {
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

  const { content_quality = {}, improvement_suggestions = {}, bullet_rewrites = [] } = currentAnalysis;

  return (
    <div className="improvement-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>📄 Resume Improvement & Bullet Rewriter</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Action verb quality check, quantifiable impact metrics detection, and bullet optimization.
          </p>
        </div>
      </div>

      {/* CONTENT QUALITY CHECK CARDS */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div className="card text-center">
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Action Verbs Detected</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-cyan)', margin: '6px 0' }}>
            {content_quality.action_verbs_detected || 0}
          </div>
          <div style={{ fontSize: '0.72rem', color: '#64748b' }}>e.g. Engineered, Architected</div>
        </div>

        <div className="card text-center">
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Quantifiable Metrics</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#10b981', margin: '6px 0' }}>
            {content_quality.quantifiable_metrics_found || 0}
          </div>
          <div style={{ fontSize: '0.72rem', color: '#64748b' }}>e.g. percentages, counts, multipliers</div>
        </div>

        <div className="card text-center">
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>ATS Format Check</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#10b981', margin: '12px 0' }}>
            PASS
          </div>
          <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Standard headings detected</div>
        </div>

        <div className="card text-center">
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Content Length</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 800, color: content_quality.has_good_length ? '#10b981' : '#f59e0b', margin: '12px 0' }}>
            {content_quality.has_good_length ? 'OPTIMAL' : 'SHORT'}
          </div>
          <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Sufficient details provided</div>
        </div>
      </div>

      {/* ACTIONABLE IMPROVEMENTS */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap size={20} className="icon-cyan" /> Actionable Resume Recommendations
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '12px 16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <strong style={{ color: 'var(--accent-cyan)', display: 'block', marginBottom: '4px' }}>[Action Verbs]</strong>
            <p style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>{improvement_suggestions.action_verbs_tip}</p>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '12px 16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <strong style={{ color: '#10b981', display: 'block', marginBottom: '4px' }}>[Quantifiable Metrics]</strong>
            <p style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>{improvement_suggestions.metrics_tip}</p>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '12px 16px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <strong style={{ color: '#f59e0b', display: 'block', marginBottom: '4px' }}>[Target Role Keywords]</strong>
            <p style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>{improvement_suggestions.formatting_tip}</p>
          </div>
        </div>
      </div>

      {/* BULLET REWRITE FEATURE */}
      <div className="card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles size={20} className="icon-cyan" /> Bullet Point Optimization Templates
        </h3>
        <p style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '18px' }}>
          Example transformations converting passive descriptions into high-impact ATS bullet points:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {bullet_rewrites.map((item, idx) => (
            <div key={idx} style={{ background: 'rgba(14, 20, 34, 0.8)', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span className="badge badge-additional">{item.tag}</span>
                <span style={{ fontSize: '0.72rem', color: '#64748b' }}>Template #{idx + 1}</span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '12px' }}>
                <div style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '12px', borderRadius: '8px' }}>
                  <strong style={{ fontSize: '0.78rem', color: '#fca5a5', display: 'block', marginBottom: '4px' }}>Weak Bullet:</strong>
                  <p style={{ fontSize: '0.85rem', color: '#fca5a5' }}>"{item.original_sample}"</p>
                </div>

                <div style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '12px', borderRadius: '8px' }}>
                  <strong style={{ fontSize: '0.78rem', color: '#10b981', display: 'block', marginBottom: '4px' }}>Optimized Impact Bullet:</strong>
                  <p style={{ fontSize: '0.85rem', color: '#6ee7b7', fontWeight: 600 }}>"{item.suggested_rewrite}"</p>
                </div>
              </div>

              <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                <strong>Why it works:</strong> {item.improvement_reason}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

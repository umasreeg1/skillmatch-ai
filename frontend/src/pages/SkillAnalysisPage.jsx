import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CategoryBarChart } from '../charts/CategoryBarChart';
import { useAnalysis } from '../context/AnalysisContext';
import { Brain, CheckCircle2, AlertTriangle, XCircle, PlusCircle, ArrowRight } from 'lucide-react';

export const SkillAnalysisPage = () => {
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

  const {
    category_summary = [],
    top_matching_skills = [],
    missing_skills = [],
    additional_skills = []
  } = currentAnalysis;

  return (
    <div className="skill-analysis-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>🧠 AI Skill Analysis & Categorization</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Domain category match percentages and ranked skill coverage breakdown.
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '25px' }}>
        {/* DOMAIN CATEGORY CHART */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '14px' }}>
            Domain Category Visualization
          </h3>
          <CategoryBarChart categorySummary={category_summary} />
        </div>

        {/* DOMAIN CATEGORY SUMMARY LIST */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '14px' }}>
            Category Coverage Details
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {category_summary.map((cat, idx) => (
              <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '0.88rem' }}>
                  <strong>{cat.category}</strong>
                  <span style={{ color: cat.match_percentage >= 75 ? '#10b981' : cat.match_percentage >= 45 ? '#f59e0b' : '#ef4444', fontWeight: 700 }}>
                    {cat.match_percentage}% ({cat.matched_count}/{cat.total_required} matched)
                  </span>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${cat.match_percentage}%`,
                    background: cat.match_percentage >= 75 ? '#10b981' : cat.match_percentage >= 45 ? '#f59e0b' : '#ef4444',
                    transition: 'width 0.8s ease'
                  }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* TOP MATCHING SKILLS */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#10b981', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle2 size={20} /> Ranked Top Matching Skills
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {top_matching_skills.map((skill, idx) => (
              <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', fontSize: '0.88rem' }}>
                  <span><strong>{skill.skill}</strong> <small style={{ color: '#94a3b8' }}>({skill.category})</small></span>
                  <span style={{ color: '#10b981', fontWeight: 700 }}>{skill.similarity}%</span>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${skill.similarity}%`, background: 'var(--gradient-primary)' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* MISSING & ADDITIONAL SKILLS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* MISSING */}
          <div className="card">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ef4444', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <XCircle size={20} /> Missing Required Skills
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {missing_skills.map((m, idx) => (
                <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(239, 68, 68, 0.05)', padding: '10px 14px', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                  <div>
                    <strong style={{ color: '#fca5a5' }}>{m.skill}</strong>
                    <span style={{ fontSize: '0.75rem', color: '#94a3b8', marginLeft: '10px' }}>Sim: {m.similarity}%</span>
                  </div>
                  <span className="badge badge-missing">{m.priority} PRIORITY</span>
                </div>
              ))}
            </div>
          </div>

          {/* ADDITIONAL */}
          <div className="card">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#3b82f6', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <PlusCircle size={20} /> Additional Candidate Skills
            </h3>
            <p style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '12px' }}>
              Useful technical skills detected in your resume but not explicitly required by this job description:
            </p>
            <div className="pill-grid">
              {additional_skills.map((add, idx) => (
                <span key={idx} className="badge badge-additional">
                  {add.skill} ({add.category})
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

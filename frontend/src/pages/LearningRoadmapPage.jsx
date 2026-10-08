import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAnalysis } from '../context/AnalysisContext';
import { Rocket, Target, BookOpen, CheckCircle2, Clock, Calendar } from 'lucide-react';

export const LearningRoadmapPage = () => {
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

  const { missing_skills = [], roadmap = [] } = currentAnalysis;

  return (
    <div className="roadmap-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>🎯 Skill Priorities & Learning Roadmap</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Tailored 4–8 week learning sequence generated dynamically for detected skill gaps.
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '24px' }}>
        {/* LEFT: MISSING SKILL PRIORITY CLASSIFICATION */}
        <div className="card">
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Target size={18} className="icon-cyan" /> Skill Priority Classification
          </h3>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '16px' }}>
            Prioritized by vector similarity gap and domain criticality:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {missing_skills.length > 0 ? (
              missing_skills.map((skill, idx) => (
                <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <strong style={{ fontSize: '0.9rem' }}>{skill.skill}</strong>
                    <span className={`badge ${skill.priority === 'HIGH' ? 'badge-missing' : 'badge-partial'}`}>
                      {skill.priority} PRIORITY
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    Category: {skill.category} • Match: {skill.similarity}%
                  </div>
                </div>
              ))
            ) : (
              <div style={{ color: '#10b981', padding: '15px' }}>
                No missing skill gaps detected!
              </div>
            )}
          </div>
        </div>

        {/* RIGHT: PERSONALIZED LEARNING ROADMAP */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Rocket size={20} className="icon-cyan" /> Personalized Skill Development Roadmap
          </h3>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '20px' }}>
            Step-by-step curriculum to close skill gaps and maximize job readiness:
          </p>

          <div className="roadmap-timeline">
            {roadmap.map((week, idx) => (
              <div key={idx} className="card roadmap-card" style={{ background: 'rgba(14, 20, 34, 0.6)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                  <span className="roadmap-week-tag"><Calendar size={14} /> {week.week_range}</span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Module {idx + 1}</span>
                </div>

                <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '8px', color: '#fff' }}>
                  {week.title}
                </h4>

                <div style={{ marginBottom: '10px' }}>
                  <strong style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)' }}>Target Skills:</strong>
                  <div className="pill-grid" style={{ marginTop: '4px' }}>
                    {week.skills.map((s, sIdx) => (
                      <span key={sIdx} className="badge badge-strong" style={{ background: 'rgba(0, 242, 254, 0.15)', color: 'var(--accent-cyan)', borderColor: 'rgba(0, 242, 254, 0.3)' }}>
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div style={{ fontSize: '0.82rem', color: '#cbd5e1', marginBottom: '8px' }}>
                  <strong>Goal:</strong> {week.goal}
                </div>

                <div style={{ fontSize: '0.82rem', color: '#cbd5e1', marginBottom: '10px' }}>
                  <strong>Focus:</strong> {week.focus}
                </div>

                <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '10px', fontSize: '0.78rem', color: '#94a3b8' }}>
                  <strong style={{ color: '#f59e0b' }}>💡 Practice Recommendation:</strong> {week.practice_recommendation}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

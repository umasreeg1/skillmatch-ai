import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ScoreGauge } from '../components/ScoreGauge';
import { SkillBreakdownDonut } from '../charts/SkillBreakdownDonut';
import { useAnalysis } from '../context/AnalysisContext';
import { CheckCircle2, AlertTriangle, XCircle, ArrowRight, Sparkles, Sliders, Rocket } from 'lucide-react';

export const ResultsPage = () => {
  const navigate = useNavigate();
  const { currentAnalysis } = useAnalysis();

  if (!currentAnalysis) {
    return (
      <div className="card text-center" style={{ padding: '60px 20px' }}>
        <h2>No Analysis Available Yet</h2>
        <p style={{ color: '#94a3b8', margin: '15px 0' }}>
          Please upload a resume or run demo mode from the dashboard to view your job match results.
        </p>
        <button className="btn-primary" onClick={() => navigate('/')}>
          Go to Dashboard
        </button>
      </div>
    );
  }

  const {
    overall_score,
    match_level,
    document_similarity,
    direct_skill_coverage,
    partial_concept_coverage,
    score_calculation,
    matching_count,
    missing_count,
    partial_count,
    additional_count,
    strong_matches,
    partial_matches,
    missing_skills,
    latency_seconds,
    job_title
  } = currentAnalysis;

  return (
    <div className="results-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>📊 AI JOB MATCH SCORE</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Target Role: <strong>{job_title}</strong> • Semantic Engine: <strong>SentenceTransformer (all-MiniLM-L6-v2)</strong> • Analyzed in {latency_seconds}s
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn-secondary" onClick={() => navigate('/simulator')}>
            <Sliders size={16} /> What-If Simulator
          </button>
          <button className="btn-primary" onClick={() => navigate('/roadmap')}>
            <Rocket size={16} /> Learning Roadmap
          </button>
        </div>
      </div>

      <div className="results-grid-top">
        {/* SCORE GAUGE CARD */}
        <div className="card score-card-center">
          <ScoreGauge score={overall_score} matchLevel={match_level} size={190} />
          
          <div className="score-stats-grid">
            <div className="stat-box">
              <div className="stat-num" style={{ color: '#10b981' }}>{matching_count}</div>
              <div className="stat-label">Matching</div>
            </div>
            <div className="stat-box">
              <div className="stat-num" style={{ color: '#f59e0b' }}>{partial_count}</div>
              <div className="stat-label">Partial</div>
            </div>
            <div className="stat-box">
              <div className="stat-num" style={{ color: '#ef4444' }}>{missing_count}</div>
              <div className="stat-label">Missing</div>
            </div>
            <div className="stat-box">
              <div className="stat-num" style={{ color: '#3b82f6' }}>{additional_count}</div>
              <div className="stat-label">Additional</div>
            </div>
          </div>
        </div>

        {/* SCORE CALCULATION BREAKDOWN */}
        <div className="card score-breakdown-card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '10px' }}>
            SCORE CALCULATION EXPLANATION
          </h3>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '14px' }}>
            Transparent weighted formula breakdown mapping candidate resume evidence against job requirements:
          </p>

          <div className="formula-box">
            <div className="formula-component">
              <span>35% Document Semantic Similarity:</span>
              <strong style={{ color: '#00f2fe' }}>{document_similarity}%</strong>
            </div>
            <div className="formula-component">
              <span>45% Direct Skill Coverage:</span>
              <strong style={{ color: '#10b981' }}>{direct_skill_coverage}%</strong>
            </div>
            <div className="formula-component">
              <span>20% Partial Concept Coverage:</span>
              <strong style={{ color: '#f59e0b' }}>{partial_concept_coverage}%</strong>
            </div>
          </div>

          <div style={{ background: 'rgba(0, 242, 254, 0.05)', border: '1px solid rgba(0, 242, 254, 0.2)', padding: '12px', borderRadius: '10px', marginTop: '14px', fontSize: '0.85rem' }}>
            <strong>Formula Weighted Total:</strong> {score_calculation?.document_similarity_weighted}% + {score_calculation?.direct_coverage_weighted}% + {score_calculation?.partial_coverage_weighted}% = <strong style={{ color: '#00f2fe' }}>{overall_score}%</strong>
          </div>
        </div>

        {/* DONUT CHART */}
        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '10px' }}>
            SKILL BREAKDOWN
          </h3>
          <SkillBreakdownDonut
            matching={matching_count}
            missing={missing_count}
            partial={partial_count}
            additional={additional_count}
          />
        </div>
      </div>

      {/* STRONG MATCHES */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#10b981', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={20} /> STRONG MATCHES (&ge;82% Similarity) ({strong_matches.length})
        </h3>
        <div className="pill-grid">
          {strong_matches.length > 0 ? (
            strong_matches.map((item, idx) => (
              <div key={idx} className="skill-pill-item badge-strong" title={item.explanation}>
                <span>{item.skill}</span>
                <small>({item.similarity}%)</small>
              </div>
            ))
          ) : (
            <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>No direct strong matches identified.</div>
          )}
        </div>
      </div>

      {/* PARTIAL MATCHES */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f59e0b', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <AlertTriangle size={20} /> PARTIAL MATCHES (45%–81% Concept Similarity) ({partial_matches.length})
        </h3>
        <div className="pill-grid">
          {partial_matches.length > 0 ? (
            partial_matches.map((item, idx) => (
              <div key={idx} className="skill-pill-item badge-partial" title={item.explanation}>
                <span>{item.skill}</span>
                <small>({item.similarity}% • {item.resume_concept})</small>
              </div>
            ))
          ) : (
            <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>No partial concept matches.</div>
          )}
        </div>
      </div>

      {/* MISSING SKILLS */}
      <div className="card">
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ef4444', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <XCircle size={20} /> MISSING SKILLS (&lt;45% Similarity) ({missing_skills.length})
        </h3>
        <div className="pill-grid">
          {missing_skills.length > 0 ? (
            missing_skills.map((item, idx) => (
              <div key={idx} className="skill-pill-item badge-missing" title={item.explanation}>
                <span>{item.skill}</span>
                <small>({item.similarity}% • {item.priority} Priority)</small>
              </div>
            ))
          ) : (
            <div style={{ color: '#10b981', fontSize: '0.85rem' }}>Awesome! No missing skills detected.</div>
          )}
        </div>
      </div>
    </div>
  );
};

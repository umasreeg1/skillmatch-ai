import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAnalysis } from '../context/AnalysisContext';
import { GitCompare, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';

export const ComparisonPage = () => {
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

  const { strong_matches = [], partial_matches = [], missing_skills = [], job_title } = currentAnalysis;
  const allComparisonItems = [...strong_matches, ...partial_matches, ...missing_skills];

  return (
    <div className="comparison-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>🔄 Resume vs Job Requirement Matrix</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            Side-by-side verification table of target job requirements against detected resume evidence.
          </p>
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <GitCompare size={20} className="icon-cyan" /> Job Skill Evidence Matrix ({job_title})
        </h3>

        <table className="custom-table">
          <thead>
            <tr>
              <th>Required Job Skill</th>
              <th>Category</th>
              <th>Resume Evidence / Concept</th>
              <th>Similarity Score</th>
              <th>Match Status</th>
            </tr>
          </thead>
          <tbody>
            {allComparisonItems.map((item, idx) => (
              <tr key={idx}>
                <td><strong>{item.skill}</strong></td>
                <td><span style={{ color: '#94a3b8' }}>{item.category}</span></td>
                <td>
                  <span style={{ color: item.status === 'Strong Match' ? '#10b981' : item.status === 'Partial Match' ? '#f59e0b' : '#ef4444' }}>
                    {item.resume_concept}
                  </span>
                </td>
                <td>
                  <strong>{item.similarity}%</strong>
                </td>
                <td>
                  {item.status === 'Strong Match' && <span className="badge badge-strong"><CheckCircle2 size={12} /> Strong Match</span>}
                  {item.status === 'Partial Match' && <span className="badge badge-partial"><AlertTriangle size={12} /> Partial Match</span>}
                  {item.status === 'Missing' && <span className="badge badge-missing"><XCircle size={12} /> Missing</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

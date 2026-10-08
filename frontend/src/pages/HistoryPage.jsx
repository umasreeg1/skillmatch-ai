import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAnalysis } from '../context/AnalysisContext';
import { History, Eye, Trash2, Calendar, Award } from 'lucide-react';

export const HistoryPage = () => {
  const navigate = useNavigate();
  const { history = [], loadHistoryItem, deleteHistoryItem } = useAnalysis();

  const handleView = async (id) => {
    await loadHistoryItem(id);
    navigate('/results');
  };

  return (
    <div className="history-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>📜 Analysis History</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            View previously saved resume analysis sessions stored securely in SQLite database.
          </p>
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <History size={20} className="icon-cyan" /> Past Analysis Records ({history.length})
        </h3>

        {history.length > 0 ? (
          <table className="custom-table">
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Target Job Role</th>
                <th>Overall Match Score</th>
                <th>Match Level</th>
                <th>Matching / Missing</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {history.map((record) => (
                <tr key={record.id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.82rem', color: '#94a3b8' }}>
                      <Calendar size={14} />
                      {record.created_at ? new Date(record.created_at).toLocaleString() : 'Recent'}
                    </div>
                  </td>
                  <td><strong>{record.job_title}</strong></td>
                  <td>
                    <span style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
                      {record.overall_score}%
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-strong">
                      {record.match_level}
                    </span>
                  </td>
                  <td>
                    <span style={{ color: '#10b981' }}>{record.matching_count} Match</span> / <span style={{ color: '#ef4444' }}>{record.missing_count} Missing</span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.78rem' }} onClick={() => handleView(record.id)}>
                        <Eye size={14} /> View Results
                      </button>
                      <button className="btn-secondary" style={{ padding: '6px 10px', color: '#ef4444' }} onClick={() => deleteHistoryItem(record.id)}>
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>
            No past analysis records found. Run an analysis on the Dashboard to save results!
          </div>
        )}
      </div>
    </div>
  );
};

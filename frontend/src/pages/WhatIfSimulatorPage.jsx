import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useAnalysis } from '../context/AnalysisContext';
import { Sliders, Sparkles, TrendingUp, CheckSquare, Info, RefreshCw } from 'lucide-react';

export const WhatIfSimulatorPage = () => {
  const navigate = useNavigate();
  const { currentAnalysis } = useAnalysis();

  const [selectedSkills, setSelectedSkills] = useState([]);
  const [simulationResult, setSimulationResult] = useState(null);
  const [simulating, setSimulating] = useState(false);

  // Extract list of missing & partial skills to simulate
  const availableSkillsToAcquire = React.useMemo(() => {
    if (!currentAnalysis) return [];
    const missing = (currentAnalysis.missing_skills || []).map(s => ({ skill: s.skill, category: s.category, sim: s.similarity, type: 'Missing' }));
    const partial = (currentAnalysis.partial_matches || []).map(s => ({ skill: s.skill, category: s.category, sim: s.similarity, type: 'Partial' }));
    return [...missing, ...partial];
  }, [currentAnalysis]);

  useEffect(() => {
    if (currentAnalysis) {
      runSimulation([]);
    }
  }, [currentAnalysis]);

  const toggleSkill = (skillName) => {
    const updated = selectedSkills.includes(skillName)
      ? selectedSkills.filter(s => s !== skillName)
      : [...selectedSkills, skillName];
    
    setSelectedSkills(updated);
    runSimulation(updated);
  };

  const runSimulation = async (acquired) => {
    if (!currentAnalysis) return;
    setSimulating(true);
    try {
      const res = await api.simulateImprovement(acquired, currentAnalysis);
      setSimulationResult(res);
      setSimulating(false);
    } catch (err) {
      setSimulating(false);
    }
  };

  if (!currentAnalysis) {
    return (
      <div className="card text-center" style={{ padding: '60px 20px' }}>
        <h2>No Analysis Available</h2>
        <p style={{ color: '#94a3b8', margin: '15px 0' }}>
          Please run a resume analysis first to launch the What-If Simulator.
        </p>
        <button className="btn-primary" onClick={() => navigate('/')}>
          Go to Dashboard
        </button>
      </div>
    );
  }

  const currentScore = currentAnalysis.overall_score;
  const projectedScore = simulationResult?.projected_score || currentScore;
  const boost = simulationResult?.estimated_boost || 0;

  return (
    <div className="simulator-container animate-fade-in">
      <div className="results-header-banner">
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>⚡ Skill Improvement Simulator</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
            What-If Analysis: Select missing skills you plan to acquire to see your estimated match score boost.
          </p>
        </div>
      </div>

      <div className="simulator-layout">
        {/* LEFT CHECKBOX LIST */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckSquare size={18} className="icon-cyan" />
            Select Skills You Plan To Learn & Acquire:
          </h3>
          <p style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '16px' }}>
            Check missing or partial skills below to dynamically project your updated match score:
          </p>

          <div className="missing-checkbox-list">
            {availableSkillsToAcquire.length > 0 ? (
              availableSkillsToAcquire.map((item, idx) => {
                const isSelected = selectedSkills.includes(item.skill);
                return (
                  <label key={idx} className={`checkbox-item ${isSelected ? 'selected' : ''}`}>
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => toggleSkill(item.skill)}
                    />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>
                        Acquire: <span style={{ color: 'var(--accent-cyan)' }}>{item.skill}</span>
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        Category: {item.category} • Current status: {item.type} ({item.sim}%)
                      </div>
                    </div>
                  </label>
                );
              })
            ) : (
              <div style={{ color: '#10b981', padding: '15px' }}>
                🎉 You already match all required job skills!
              </div>
            )}
          </div>
        </div>

        {/* RIGHT SIMULATION SCORE PROJECTION CARD */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card" style={{ textCenter: 'center', background: 'linear-gradient(180deg, rgba(20, 28, 46, 0.9) 0%, rgba(14, 20, 34, 0.95) 100%)', border: '1px solid var(--border-highlight)' }}>
            <div style={{ textTransform: 'uppercase', fontSize: '0.75rem', color: '#94a3b8', letterSpacing: '1px', marginBottom: '15px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
              <Sparkles size={14} className="icon-cyan" /> Simulation Projection
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', margin: '10px 0' }}>
              <div className="stat-box">
                <div className="stat-label">CURRENT MATCH</div>
                <div className="stat-num" style={{ color: '#94a3b8' }}>{currentScore}%</div>
              </div>

              <div className="stat-box" style={{ background: 'rgba(0, 242, 254, 0.08)', borderColor: 'rgba(0, 242, 254, 0.3)' }}>
                <div className="stat-label" style={{ color: 'var(--accent-cyan)' }}>PROJECTED MATCH</div>
                <div className="stat-num" style={{ color: 'var(--accent-cyan)' }}>{projectedScore}%</div>
              </div>
            </div>

            <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '12px', padding: '16px', margin: '15px 0', textCenter: 'center' }}>
              <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '4px' }}>ESTIMATED BOOST</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#10b981', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                <TrendingUp size={28} /> +{boost}%
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '4px' }}>
                Acquiring {selectedSkills.length} selected skill(s)
              </div>
            </div>

            <button
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center' }}
              onClick={() => runSimulation(selectedSkills)}
              disabled={simulating}
            >
              {simulating ? <RefreshCw className="spinner-icon" size={18} /> : <Sliders size={18} />}
              Recalculate Simulation
            </button>
          </div>

          <div className="card" style={{ fontSize: '0.78rem', color: '#94a3b8', lineHeight: 1.4 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#f59e0b', fontWeight: 700, marginBottom: '6px' }}>
              <Info size={14} /> SIMULATION NOTE
            </div>
            {simulationResult?.disclaimer || "The projected score is an estimate calculated by treating selected skills as acquired and rerunning the existing matching logic. It is not a guaranteed hiring or examination outcome."}
          </div>
        </div>
      </div>
    </div>
  );
};

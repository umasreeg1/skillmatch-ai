import React from 'react';
import { Loader2, Sparkles, Cpu } from 'lucide-react';

export const LoadingOverlay = ({ loadingStep }) => {
  return (
    <div className="loading-overlay">
      <div className="loading-card card">
        <div className="loading-icon-wrapper">
          <Loader2 className="spinner-icon" size={48} />
          <Cpu className="cpu-pulse-icon" size={24} />
        </div>
        <h3 className="loading-title">AI Processing Pipeline</h3>
        <p className="loading-step-text">{loadingStep || 'Executing NLP Analysis...'}</p>
        
        <div className="progress-bar-container">
          <div className="progress-bar-fill"></div>
        </div>

        <div className="model-badge">
          <Sparkles size={14} /> Model: SentenceTransformer (all-MiniLM-L6-v2) | 384-D Vectors
        </div>
      </div>
    </div>
  );
};

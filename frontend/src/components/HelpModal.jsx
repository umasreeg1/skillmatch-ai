import React from 'react';
import { X, Sparkles, BookOpen, Sliders, CheckCircle2, HelpCircle } from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';

export const HelpModal = () => {
  const { helpModalOpen, setHelpModalOpen } = useAnalysis();

  if (!helpModalOpen) return null;

  return (
    <div className="modal-overlay" onClick={() => setHelpModalOpen(false)}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Sparkles className="icon-glow" size={22} />
            <h2>SkillMatch AI Assistant & Project Guide</h2>
          </div>
          <button className="close-btn" onClick={() => setHelpModalOpen(false)}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <section className="help-section">
            <h3><HelpCircle size={18} /> How to run an analysis?</h3>
            <p>1. Go to <strong>Analyze Resume</strong> or <strong>Dashboard</strong>.</p>
            <p>2. Upload a PDF resume or paste raw resume text into Card 1.</p>
            <p>3. Select a Job Description Template (e.g. Junior AI/ML Engineer) or paste your target job posting into Card 2.</p>
            <p>4. Click <strong>✨ Analyze Resume</strong> or use <strong>✨ Try Demo</strong> for instant testing.</p>
          </section>

          <section className="help-section">
            <h3><Sparkles size={18} /> What AI model is used?</h3>
            <p>SkillMatch AI uses HuggingFace <strong>SentenceTransformer: <code>all-MiniLM-L6-v2</code></strong>. It converts resume text and job requirements into <strong>384-dimensional dense semantic vector embeddings</strong> and compares them using Cosine Distance.</p>
          </section>

          <section className="help-section">
            <h3><Sliders size={18} /> What-If Simulator</h3>
            <p>Select missing skills to dynamically recalculate your projected score and evaluate career growth options without modifying your actual resume.</p>
          </section>

          <section className="help-section">
            <h3><BookOpen size={18} /> Academic & Viva Guide</h3>
            <p>Check the <strong>Methodology</strong> page for exact scoring formulas, threshold definitions (Strong &ge;82%, Partial 45-81%, Missing &lt;45%), and 30+ Viva Questions with sample answers.</p>
          </section>
        </div>

        <div className="modal-footer">
          <button className="btn-primary" onClick={() => setHelpModalOpen(false)}>
            Got it, thanks!
          </button>
        </div>
      </div>
    </div>
  );
};

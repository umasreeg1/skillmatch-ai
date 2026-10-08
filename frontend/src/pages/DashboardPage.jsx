import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud,
  FileText,
  Sparkles,
  CheckCircle2,
  Zap,
  BarChart3,
  Lightbulb,
  Briefcase,
  Layers,
  ArrowRight,
  X
} from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';

export const DashboardPage = () => {
  const navigate = useNavigate();
  const { runAnalysis, runDemoMode, templates, currentAnalysis } = useAnalysis();

  const [resumeMode, setResumeMode] = useState('upload'); // 'upload' | 'paste'
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  
  const [jobMode, setJobMode] = useState('template'); // 'template' | 'paste'
  const [jobDescription, setJobDescription] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('junior_aiml');
  const [jobTitle, setJobTitle] = useState('Junior AI/ML Engineer');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (selected.size > 5 * 1024 * 1024) {
        alert('File size exceeds maximum 5MB limit.');
        return;
      }
      setFile(selected);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const selected = e.dataTransfer.files[0];
      if (selected.size > 5 * 1024 * 1024) {
        alert('File size exceeds maximum 5MB limit.');
        return;
      }
      setFile(selected);
    }
  };

  const handleTemplateSelect = (e) => {
    const templateId = e.target.value;
    setSelectedTemplate(templateId);
    const found = templates.find(t => t.id === templateId);
    if (found) {
      setJobTitle(found.title);
      setJobDescription(found.description);
    }
  };

  const handleAnalyze = async () => {
    try {
      if (resumeMode === 'upload' && !file && !resumeText) {
        alert('Please upload a PDF resume or switch to Paste Text mode.');
        return;
      }
      if (resumeMode === 'paste' && !resumeText.trim()) {
        alert('Please paste your resume text.');
        return;
      }

      await runAnalysis({
        file: resumeMode === 'upload' ? file : null,
        resumeText: resumeMode === 'paste' ? resumeText : null,
        jobDescription: jobMode === 'paste' ? jobDescription : null,
        jobTitle: jobTitle,
        templateId: jobMode === 'template' ? selectedTemplate : null
      });

      navigate('/results');
    } catch (err) {
      // Handled in context
    }
  };

  const handleDemoClick = async () => {
    try {
      await runDemoMode(selectedTemplate);
      navigate('/results');
    } catch (err) {
      // Handled in context
    }
  };

  return (
    <div className="dashboard-container animate-fade-in">
      {/* Hero Header */}
      <section className="hero-section">
        <h1 className="hero-title">
          Discover Your Resume's <span className="gradient-text">Skill Gap</span>
        </h1>
        <p className="hero-subtitle">
          AI-powered resume analysis to match your skills with job requirements and get personalized recommendations.
        </p>

        <div className="feature-indicators">
          <div className="feature-badge-card">
            <div className="feature-icon-wrapper">
              <Zap size={20} />
            </div>
            <div>
              <div className="feature-title">Accurate Skill Matching</div>
              <div className="feature-sub">NLP + Semantic AI</div>
            </div>
          </div>

          <div className="feature-badge-card">
            <div className="feature-icon-wrapper">
              <BarChart3 size={20} />
            </div>
            <div>
              <div className="feature-title">Detailed Gap Analysis</div>
              <div className="feature-sub">Identify missing skills</div>
            </div>
          </div>

          <div className="feature-badge-card">
            <div className="feature-icon-wrapper">
              <Lightbulb size={20} />
            </div>
            <div>
              <div className="feature-title">Personalized Roadmap</div>
              <div className="feature-sub">Learn the right skills</div>
            </div>
          </div>

          <div className="feature-badge-card">
            <div className="feature-icon-wrapper">
              <Briefcase size={20} />
            </div>
            <div>
              <div className="feature-title">Boost Career Opportunities</div>
              <div className="feature-sub">Be job-ready</div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Input Grid */}
      <div className="dashboard-grid">
        {/* CARD 1: YOUR RESUME */}
        <div className="card">
          <div className="card-header-tabs">
            <div className="card-title-text">
              <FileText size={18} className="icon-cyan" />
              <span>YOUR RESUME</span>
            </div>
            <div className="tab-btn-group">
              <button
                className={`tab-btn ${resumeMode === 'upload' ? 'active' : ''}`}
                onClick={() => setResumeMode('upload')}
              >
                Upload PDF
              </button>
              <button
                className={`tab-btn ${resumeMode === 'paste' ? 'active' : ''}`}
                onClick={() => setResumeMode('paste')}
              >
                Paste Text
              </button>
            </div>
          </div>

          {resumeMode === 'upload' ? (
            <div>
              {!file ? (
                <div
                  className="dropzone"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById('pdf-file-input').click()}
                >
                  <UploadCloud size={38} className="dropzone-icon" />
                  <div className="dropzone-title">Drag & Drop your resume here</div>
                  <div className="dropzone-desc">or Click to browse PDF (Max size: 5 MB)</div>
                  <input
                    type="file"
                    id="pdf-file-input"
                    accept=".pdf"
                    style={{ display: 'none' }}
                    onChange={handleFileChange}
                  />
                </div>
              ) : (
                <div className="file-status-box">
                  <div className="file-info">
                    <CheckCircle2 size={24} className="file-icon-check" />
                    <div>
                      <div className="file-name">{file.name}</div>
                      <div className="file-size">{(file.size / (1024 * 1024)).toFixed(2)} MB • Status: Ready to analyze</div>
                    </div>
                  </div>
                  <button className="remove-file-btn" onClick={() => setFile(null)} title="Remove file">
                    <X size={18} />
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div>
              <textarea
                rows={9}
                placeholder="Paste raw resume text here (e.g. skills, work experience, projects)..."
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
              />
              <div style={{ fontSize: '0.75rem', color: '#64748b', textAlign: 'right', marginTop: '4px' }}>
                Character count: {resumeText.length}
              </div>
            </div>
          )}
        </div>

        {/* CARD 2: TARGET JOB REQUIREMENT */}
        <div className="card">
          <div className="card-header-tabs">
            <div className="card-title-text">
              <Briefcase size={18} className="icon-cyan" />
              <span>TARGET JOB REQUIREMENT</span>
            </div>
            <div className="tab-btn-group">
              <button
                className={`tab-btn ${jobMode === 'template' ? 'active' : ''}`}
                onClick={() => setJobMode('template')}
              >
                Use Template
              </button>
              <button
                className={`tab-btn ${jobMode === 'paste' ? 'active' : ''}`}
                onClick={() => setJobMode('paste')}
              >
                Paste Job
              </button>
            </div>
          </div>

          {jobMode === 'template' ? (
            <div>
              <label style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '6px', display: 'block' }}>
                Select Predefined Job Role Template:
              </label>
              <select value={selectedTemplate} onChange={handleTemplateSelect} style={{ marginBottom: '12px' }}>
                {templates.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.title} ({t.category})
                  </option>
                ))}
              </select>
              <textarea
                rows={6}
                readOnly
                value={jobDescription || templates.find(t => t.id === selectedTemplate)?.description || ''}
                style={{ opacity: 0.85, background: 'rgba(0,0,0,0.2)' }}
              />
            </div>
          ) : (
            <div>
              <input
                type="text"
                placeholder="Job Title (e.g. Senior Data Scientist)"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <textarea
                rows={7}
                placeholder="Paste target job description requirements, responsibilities, and required skills here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
              <div style={{ fontSize: '0.75rem', color: '#64748b', textAlign: 'right', marginTop: '4px' }}>
                Character count: {jobDescription.length}
              </div>
            </div>
          )}
        </div>

        {/* QUICK OPTIONS CARD */}
        <div className="card quick-options-card">
          <div>
            <div className="card-title-text" style={{ marginBottom: '12px' }}>
              <Layers size={18} className="icon-cyan" />
              <span>QUICK OPTIONS</span>
            </div>
            
            <div className="quick-btn-list">
              <button className="btn-secondary quick-btn" onClick={handleDemoClick}>
                <Sparkles size={16} /> ✨ Try Demo Analysis
              </button>
              <button className="btn-secondary quick-btn" onClick={() => setJobMode('template')}>
                <FileText size={16} /> 📄 Select Role Template
              </button>
              <button
                className="btn-secondary quick-btn"
                onClick={() => {
                  setResumeMode('paste');
                  setResumeText("Python, Machine Learning, Scikit-learn, Pandas, NumPy, SQL, Git, GitHub, Jupyter");
                }}
              >
                <Layers size={16} /> 📁 Load Sample Resume
              </button>
            </div>
          </div>

          <div>
            <button className="btn-primary analyze-main-btn" onClick={handleAnalyze}>
              ✨ Analyze Resume <ArrowRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

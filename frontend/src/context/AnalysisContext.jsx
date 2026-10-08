import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AnalysisContext = createContext();

export const AnalysisProvider = ({ children }) => {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [history, setHistory] = useState([]);
  const [theme, setTheme] = useState(() => localStorage.getItem('sm_theme') || 'dark');
  const [helpModalOpen, setHelpModalOpen] = useState(false);

  useEffect(() => {
    localStorage.setItem('sm_theme', theme);
    if (theme === 'light') {
      document.body.classList.add('light-theme');
    } else {
      document.body.classList.remove('light-theme');
    }
  }, [theme]);

  useEffect(() => {
    fetchTemplates();
    fetchHistory();
  }, []);

  const fetchTemplates = async () => {
    try {
      const data = await api.getTemplates();
      setTemplates(data);
    } catch (err) {
      console.error('Failed to load templates:', err);
    }
  };

  const fetchHistory = async () => {
    try {
      const data = await api.getHistory();
      setHistory(data);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const simulateLoadingSteps = async (taskFn) => {
    setLoading(true);
    setError(null);
    const steps = [
      '📄 Parsing resume content & validating format...',
      '🧠 Extracting candidate skill taxonomy...',
      '🔎 Understanding job requirements & dependencies...',
      '🔗 Generating 384-dimensional semantic embeddings...',
      '📊 Computing cosine similarity matrix...',
      '🎯 Classifying skill gaps & threshold categories...',
      '🚀 Building personalized learning roadmap...'
    ];

    let currentIdx = 0;
    setLoadingStep(steps[0]);

    const interval = setInterval(() => {
      currentIdx++;
      if (currentIdx < steps.length) {
        setLoadingStep(steps[currentIdx]);
      }
    }, 350);

    try {
      const result = await taskFn();
      clearInterval(interval);
      setCurrentAnalysis(result);
      setLoading(false);
      fetchHistory(); // Refresh history
      return result;
    } catch (err) {
      clearInterval(interval);
      setLoading(false);
      const errMsg = err.response?.data?.detail || err.message || 'Analysis failed. Please check inputs and backend server.';
      setError(errMsg);
      throw err;
    }
  };

  const runAnalysis = async (params) => {
    return simulateLoadingSteps(() => api.analyzeResume(params));
  };

  const runDemoMode = async (templateId = 'junior_aiml') => {
    return simulateLoadingSteps(() => api.runDemo(templateId));
  };

  const deleteHistoryItem = async (id) => {
    try {
      await api.deleteHistoryItem(id);
      setHistory(prev => prev.filter(item => item.id !== id));
      if (currentAnalysis?.id === id) {
        setCurrentAnalysis(null);
      }
    } catch (err) {
      console.error('Failed to delete history item:', err);
    }
  };

  const loadHistoryItem = async (id) => {
    setLoading(true);
    try {
      const item = await api.getHistoryItem(id);
      setCurrentAnalysis(item.analysis_data);
      setLoading(false);
    } catch (err) {
      setLoading(false);
      setError('Could not load saved analysis.');
    }
  };

  return (
    <AnalysisContext.Provider
      value={{
        currentAnalysis,
        setCurrentAnalysis,
        loading,
        loadingStep,
        error,
        setError,
        templates,
        history,
        theme,
        toggleTheme,
        runAnalysis,
        runDemoMode,
        deleteHistoryItem,
        loadHistoryItem,
        helpModalOpen,
        setHelpModalOpen,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
};

export const useAnalysis = () => useContext(AnalysisContext);

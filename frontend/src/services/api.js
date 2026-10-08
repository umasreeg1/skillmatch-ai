import axios from 'axios';

const API_BASE = '/api';

export const api = {
  checkHealth: async () => {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  },

  getTemplates: async () => {
    const res = await axios.get(`${API_BASE}/templates`);
    return res.data;
  },

  runDemo: async (templateId = 'junior_aiml') => {
    const res = await axios.post(`${API_BASE}/demo?template_id=${templateId}`);
    return res.data;
  },

  analyzeResume: async ({ file, resumeText, jobDescription, jobTitle, templateId }) => {
    const formData = new FormData();
    if (file) {
      formData.append('resume_file', file);
    }
    if (resumeText) {
      formData.append('resume_text', resumeText);
    }
    if (jobDescription) {
      formData.append('job_description', jobDescription);
    }
    if (jobTitle) {
      formData.append('job_title', jobTitle);
    }
    if (templateId) {
      formData.append('template_id', templateId);
    }

    const res = await axios.post(`${API_BASE}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  simulateImprovement: async (acquiredSkills, currentAnalysis) => {
    const res = await axios.post(`${API_BASE}/simulate`, {
      acquired_skills: acquiredSkills,
      current_analysis: currentAnalysis,
    });
    return res.data;
  },

  getHistory: async () => {
    const res = await axios.get(`${API_BASE}/history`);
    return res.data;
  },

  getHistoryItem: async (id) => {
    const res = await axios.get(`${API_BASE}/history/${id}`);
    return res.data;
  },

  deleteHistoryItem: async (id) => {
    const res = await axios.delete(`${API_BASE}/history/${id}`);
    return res.data;
  },

  getMethodology: async () => {
    const res = await axios.get(`${API_BASE}/methodology`);
    return res.data;
  },
};

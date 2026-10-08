import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnalysisProvider } from './context/AnalysisContext';
import { MainLayout } from './layouts/MainLayout';
import { DashboardPage } from './pages/DashboardPage';
import { ResultsPage } from './pages/ResultsPage';
import { SkillAnalysisPage } from './pages/SkillAnalysisPage';
import { WhatIfSimulatorPage } from './pages/WhatIfSimulatorPage';
import { LearningRoadmapPage } from './pages/LearningRoadmapPage';
import { ExplainableAIPage } from './pages/ExplainableAIPage';
import { ResumeImprovementPage } from './pages/ResumeImprovementPage';
import { ComparisonPage } from './pages/ComparisonPage';
import { HistoryPage } from './pages/HistoryPage';
import { MethodologyPage } from './pages/MethodologyPage';
import { ModelEvaluationPage } from './pages/ModelEvaluationPage';
import { AboutPage } from './pages/AboutPage';

export const App = () => {
  return (
    <AnalysisProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="analyze" element={<DashboardPage />} />
            <Route path="results" element={<ResultsPage />} />
            <Route path="skills" element={<SkillAnalysisPage />} />
            <Route path="simulator" element={<WhatIfSimulatorPage />} />
            <Route path="roadmap" element={<LearningRoadmapPage />} />
            <Route path="improvements" element={<ResumeImprovementPage />} />
            <Route path="comparison" element={<ComparisonPage />} />
            <Route path="history" element={<HistoryPage />} />
            <Route path="methodology" element={<MethodologyPage />} />
            <Route path="evaluation" element={<ModelEvaluationPage />} />
            <Route path="about" element={<AboutPage />} />
          </Route>
        </Routes>
      </Router>
    </AnalysisProvider>
  );
};

export default App;

import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { TopBar } from '../components/TopBar';
import { HelpModal } from '../components/HelpModal';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { useAnalysis } from '../context/AnalysisContext';

export const MainLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { loading, loadingStep, error, setError } = useAnalysis();

  return (
    <div className="app-container">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      
      <div className="main-wrapper">
        <TopBar setMobileOpen={setMobileOpen} />
        
        {error && (
          <div className="error-banner card">
            <span>⚠️ {error}</span>
            <button className="dismiss-btn" onClick={() => setError(null)}>✕</button>
          </div>
        )}

        <main className="main-content">
          <Outlet />
        </main>
      </div>

      {loading && <LoadingOverlay loadingStep={loadingStep} />}
      <HelpModal />
    </div>
  );
};

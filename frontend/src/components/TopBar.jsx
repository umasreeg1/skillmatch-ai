import React, { useState } from 'react';
import { Moon, Sun, Bell, Menu, User, Sparkles, ChevronDown } from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';

export const TopBar = ({ setMobileOpen }) => {
  const { theme, toggleTheme, currentAnalysis } = useAnalysis();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <header className="topbar">
      <div className="topbar-left">
        <button className="mobile-toggle-btn" onClick={() => setMobileOpen(true)}>
          <Menu size={22} />
        </button>
        <div className="page-status-indicator">
          {currentAnalysis ? (
            <span className="status-badge ready">
              <span className="dot"></span>
              Match Score: <strong>{currentAnalysis.overall_score}%</strong> ({currentAnalysis.job_title})
            </span>
          ) : (
            <span className="status-badge idle">
              <span className="dot"></span>
              Ready to Analyze
            </span>
          )}
        </div>
      </div>

      <div className="topbar-right">
        <button className="icon-btn theme-toggle" onClick={toggleTheme} title="Toggle Theme">
          {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
        </button>

        <button className="icon-btn notification-btn" title="Notifications">
          <Bell size={18} />
          <span className="notification-badge"></span>
        </button>

        <div className="user-profile-menu">
          <div className="profile-trigger" onClick={() => setDropdownOpen(!dropdownOpen)}>
            <div className="user-avatar">M</div>
            <div className="user-info-text">
              <span className="user-name">Megana</span>
              <span className="user-role">Candidate / Evaluator</span>
            </div>
            <ChevronDown size={14} className="dropdown-chevron" />
          </div>

          {dropdownOpen && (
            <div className="profile-dropdown">
              <div className="dropdown-item header-info">
                <strong>Megana V.</strong>
                <small>megana@example.com</small>
              </div>
              <div className="dropdown-divider"></div>
              <div className="dropdown-item">
                <Sparkles size={16} /> 384-D Vector Engine
              </div>
              <div className="dropdown-item" onClick={() => { toggleTheme(); setDropdownOpen(false); }}>
                {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  BarChart3,
  Brain,
  Sliders,
  Rocket,
  GitCompare,
  BookOpen,
  Microscope,
  History,
  Info,
  HelpCircle,
  Sparkles,
  X
} from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';

export const Sidebar = ({ mobileOpen, setMobileOpen }) => {
  const { setHelpModalOpen } = useAnalysis();

  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Analyze Resume', path: '/analyze', icon: FileText },
    { label: 'Results', path: '/results', icon: BarChart3 },
    { label: 'Skill Analysis', path: '/skills', icon: Brain },
    { label: 'What-If Simulator', path: '/simulator', icon: Sliders },
    { label: 'Learning Roadmap', path: '/roadmap', icon: Rocket },
    { label: 'Comparison', path: '/comparison', icon: GitCompare },
    { label: 'Methodology', path: '/methodology', icon: BookOpen },
    { label: 'Model Evaluation', path: '/evaluation', icon: Microscope },
    { label: 'Analysis History', path: '/history', icon: History },
    { label: 'About Project', path: '/about', icon: Info },
  ];

  const handleLinkClick = () => {
    if (setMobileOpen) setMobileOpen(false);
  };

  return (
    <aside className={`sidebar ${mobileOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <div className="brand-title">
          <Sparkles className="brand-icon" />
          <span>SKILLMATCH <span className="highlight">AI</span></span>
        </div>
        <div className="brand-subtitle">Resume Intelligence & Skill Gap Analyzer</div>
        {setMobileOpen && (
          <button className="mobile-close-btn" onClick={() => setMobileOpen(false)}>
            <X size={20} />
          </button>
        )}
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={handleLinkClick}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-bottom">
        <div className="ai-assistant-card" onClick={() => setHelpModalOpen(true)}>
          <div className="assistant-header">
            <HelpCircle size={20} className="assistant-icon" />
            <span className="assistant-title">AI Assistant</span>
          </div>
          <p className="assistant-desc">Need help with analysis, methodology or viva setup? Ask me anything.</p>
          <button className="assistant-btn">Project Help & Info</button>
        </div>
      </div>
    </aside>
  );
};

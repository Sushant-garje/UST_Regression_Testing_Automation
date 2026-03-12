import React from 'react'
import { Moon, Sun, Upload, BarChart3, Settings } from 'lucide-react'
import './Header.css'

function Header({ theme, onThemeToggle, onUploadClick, onVisualizationClick }) {
  return (
    <header className="header">
      <div className="header-left">
        <div className="logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="6" fill="url(#gradient)" />
            <path d="M8 16L14 10L20 16L14 22L8 16Z" fill="white" opacity="0.9" />
            <path d="M14 10L20 16L26 10L20 4L14 10Z" fill="white" opacity="0.7" />
            <defs>
              <linearGradient id="gradient" x1="0" y1="0" x2="32" y2="32">
                <stop offset="0%" stopColor="#2563eb" />
                <stop offset="100%" stopColor="#7c3aed" />
              </linearGradient>
            </defs>
          </svg>
          <div className="logo-text">
            <h1>VLSI Regression Copilot</h1>
            <span className="logo-subtitle">AI-Powered Test Optimization</span>
          </div>
        </div>
      </div>

      <div className="header-right">
        <button 
          className="header-btn" 
          onClick={onUploadClick}
          title="Upload Files"
        >
          <Upload size={20} />
          <span>Upload</span>
        </button>

        <button 
          className="header-btn" 
          onClick={onVisualizationClick}
          title="View Analytics"
        >
          <BarChart3 size={20} />
          <span>Analytics</span>
        </button>

        <button 
          className="header-btn" 
          onClick={onThemeToggle}
          title="Toggle Theme"
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        <button className="header-btn" title="Settings">
          <Settings size={20} />
        </button>
      </div>
    </header>
  )
}

export default Header

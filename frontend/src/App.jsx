import React, { useState, useEffect } from 'react'

import ChatInterface from './components/ChatInterface'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import FileUploadModal from './components/FileUploadModal'
import VisualizationPanel from './components/VisualizationPanel'
import SelectedTestsDisplay from './SelectedTestsDisplay'
import './App.css'

function App() {
  const [theme, setTheme] = useState('dark')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [uploadModalOpen, setUploadModalOpen] = useState(false)
  const [visualizationOpen, setVisualizationOpen] = useState(false)
  const [currentFiles, setCurrentFiles] = useState([])
  const [optimizationResults, setOptimizationResults] = useState(null)
  const [chatHistory, setChatHistory] = useState([])

  useEffect(() => {
    document.body.className = theme
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  const handleFileUpload = (files) => {
    setCurrentFiles(files)
    setUploadModalOpen(false)
  }

  const handleOptimizationComplete = (results) => {
    setOptimizationResults(results)
    setVisualizationOpen(true)
  }

  // Fetch files from backend on mount
  useEffect(() => {
    async function fetchFiles() {
      try {
        const res = await fetch('/api/files');
        if (res.ok) {
          const data = await res.json();
          setCurrentFiles(data.files.map(name => ({ name })));
        }
      } catch (err) {
        // Optionally handle error
      }
    }
    fetchFiles();
  }, []);

  return (
    <div className="app">
      <Header 
        theme={theme}
        onThemeToggle={toggleTheme}
        onUploadClick={() => setUploadModalOpen(true)}
        onVisualizationClick={() => setVisualizationOpen(!visualizationOpen)}
      />
      <div className="app-body">
        <Sidebar 
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          currentFiles={currentFiles}
          chatHistory={chatHistory}
        />
        <div className="main-content">
          <ChatInterface 
            theme={theme}
            currentFiles={currentFiles}
            onOptimizationComplete={handleOptimizationComplete}
            chatHistory={chatHistory}
            setChatHistory={setChatHistory}
          />
          {/* Show selected test cases table below chat interface */}
          <div style={{marginTop: '2rem'}}>
            <SelectedTestsDisplay />
          </div>
          {visualizationOpen && optimizationResults && (
            <VisualizationPanel 
              results={optimizationResults}
              onClose={() => setVisualizationOpen(false)}
            />
          )}
        </div>
      </div>
      {uploadModalOpen && (
        <FileUploadModal 
          onClose={() => setUploadModalOpen(false)}
          onUpload={handleFileUpload}
        />
      )}
    </div>
  )
}

export default App;

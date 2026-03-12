import React from 'react'
import { ChevronLeft, ChevronRight, FileText, MessageSquare, Clock } from 'lucide-react'
import './Sidebar.css'

function Sidebar({ isOpen, onToggle, currentFiles, chatHistory }) {
  const recentChats = chatHistory.slice(-5).reverse()

  return (
    <>
      <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <button className="sidebar-toggle" onClick={onToggle}>
          {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
        </button>

        {isOpen && (
          <div className="sidebar-content">
            <section className="sidebar-section">
              <h3 className="sidebar-title">
                <FileText size={16} />
                Current Files
              </h3>
              <div className="sidebar-list">
                {currentFiles.length === 0 ? (
                  <div className="sidebar-empty">
                    No files uploaded yet
                  </div>
                ) : (
                  currentFiles.map((file, idx) => (
                    <div key={idx} className="sidebar-item">
                      <FileText size={14} />
                      <span className="sidebar-item-text">{file.name}</span>
                      <span className="sidebar-item-badge">
                        {(file.size / 1024).toFixed(1)}KB
                      </span>
                    </div>
                  ))
                )}
              </div>
            </section>

            <section className="sidebar-section">
              <h3 className="sidebar-title">
                <Clock size={16} />
                Recent Chats
              </h3>
              <div className="sidebar-list">
                {recentChats.length === 0 ? (
                  <div className="sidebar-empty">
                    No chat history yet
                  </div>
                ) : (
                  recentChats.map((chat, idx) => (
                    <div key={idx} className="sidebar-item clickable">
                      <MessageSquare size={14} />
                      <span className="sidebar-item-text">
                        {chat.message.substring(0, 30)}...
                      </span>
                    </div>
                  ))
                )}
              </div>
            </section>

            <section className="sidebar-section">
              <h3 className="sidebar-title">Quick Actions</h3>
              <div className="quick-actions">
                <button className="quick-action-btn">
                  Analyze Test Suite
                </button>
                <button className="quick-action-btn">
                  Find Redundant Tests
                </button>
                <button className="quick-action-btn">
                  Optimize Resources
                </button>
                <button className="quick-action-btn">
                  Generate Report
                </button>
              </div>
            </section>
          </div>
        )}
      </div>
    </>
  )
}

export default Sidebar

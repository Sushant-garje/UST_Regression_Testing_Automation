import React, { useState } from 'react'
import { X, BarChart3, PieChart, TrendingUp } from 'lucide-react'
import { 
  BarChart, Bar, PieChart as RePieChart, Pie, Cell,
  LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer 
} from 'recharts'
import './VisualizationPanel.css'

const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444']

function VisualizationPanel({ results, onClose }) {
  const [activeTab, setActiveTab] = useState('overview')

  const { ranked_tests, summary } = results

  // Prepare data for charts
  const priorityData = [
    { name: 'P0 (Critical)', value: ranked_tests.filter(t => t.action === 'run_first').length },
    { name: 'P1 (High)', value: ranked_tests.filter(t => t.action === 'run_early').length },
    { name: 'P2 (Medium)', value: ranked_tests.filter(t => t.action === 'run_normal').length },
    { name: 'P3 (Low)', value: ranked_tests.filter(t => t.action === 'run_late').length }
  ]

  const coverageData = ranked_tests.slice(0, 10).map(test => ({
    name: test.testcase_id.substring(0, 15) + '...',
    coverage: test.coverage,
    score: test.score * 100
  }))

  const runtimeData = ranked_tests.slice(0, 10).map(test => ({
    name: test.testcase_id.substring(0, 15) + '...',
    runtime: test.runtime_seconds
  }))

  return (
    <div className="visualization-panel">
      <div className="panel-header">
        <h2>Analytics Dashboard</h2>
        <button className="panel-close" onClick={onClose}>
          <X size={20} />
        </button>
      </div>

      <div className="panel-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          <BarChart3 size={16} />
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'distribution' ? 'active' : ''}`}
          onClick={() => setActiveTab('distribution')}
        >
          <PieChart size={16} />
          Distribution
        </button>
        <button 
          className={`tab ${activeTab === 'trends' ? 'active' : ''}`}
          onClick={() => setActiveTab('trends')}
        >
          <TrendingUp size={16} />
          Trends
        </button>
      </div>

      <div className="panel-content">
        {activeTab === 'overview' && (
          <div className="charts-grid">
            <div className="chart-card">
              <h3>Top 10 Tests by Coverage</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={coverageData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="name" stroke="var(--text-muted)" />
                  <YAxis stroke="var(--text-muted)" />
                  <Tooltip 
                    contentStyle={{ 
                      background: 'var(--bg-secondary)', 
                      border: '1px solid var(--border)',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <Bar dataKey="coverage" fill="#2563eb" name="Coverage %" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>Priority Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <RePieChart>
                  <Pie
                    data={priorityData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {priorityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </RePieChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {activeTab === 'distribution' && (
          <div className="charts-grid">
            <div className="chart-card full-width">
              <h3>Runtime Distribution (Top 10 Tests)</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={runtimeData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="name" stroke="var(--text-muted)" angle={-45} textAnchor="end" height={100} />
                  <YAxis stroke="var(--text-muted)" label={{ value: 'Runtime (s)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip 
                    contentStyle={{ 
                      background: 'var(--bg-secondary)', 
                      border: '1px solid var(--border)',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="runtime" fill="#10b981" name="Runtime (seconds)" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {activeTab === 'trends' && (
          <div className="charts-grid">
            <div className="chart-card full-width">
              <h3>Score vs Coverage Trend</h3>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={coverageData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="name" stroke="var(--text-muted)" />
                  <YAxis stroke="var(--text-muted)" />
                  <Tooltip 
                    contentStyle={{ 
                      background: 'var(--bg-secondary)', 
                      border: '1px solid var(--border)',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="coverage" stroke="#2563eb" name="Coverage %" />
                  <Line type="monotone" dataKey="score" stroke="#10b981" name="Score" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default VisualizationPanel

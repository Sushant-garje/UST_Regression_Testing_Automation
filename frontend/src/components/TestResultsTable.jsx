import React, { useState } from 'react'
import { ChevronDown, ChevronUp, Download } from 'lucide-react'
import './TestResultsTable.css'

function TestResultsTable({ results }) {
  const [expanded, setExpanded] = useState(false)
  const [sortBy, setSortBy] = useState('priority_rank')
  const [sortOrder, setSortOrder] = useState('asc')

  const { ranked_tests, summary } = results

  const displayTests = expanded ? ranked_tests : ranked_tests.slice(0, 10)

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('asc')
    }
  }

  const sortedTests = [...displayTests].sort((a, b) => {
    const aVal = a[sortBy]
    const bVal = b[sortBy]
    const multiplier = sortOrder === 'asc' ? 1 : -1
    return (aVal > bVal ? 1 : -1) * multiplier
  })

  const getActionBadge = (action) => {
    const badges = {
      'run_first': { class: 'badge-critical', text: 'P0' },
      'run_early': { class: 'badge-high', text: 'P1' },
      'run_normal': { class: 'badge-medium', text: 'P2' },
      'run_late': { class: 'badge-low', text: 'P3' }
    }
    return badges[action] || badges['run_normal']
  }

  const exportToCSV = () => {
    const headers = ['Rank', 'Test ID', 'Score', 'Priority', 'Coverage', 'Runtime', 'Pass Rate']
    const rows = ranked_tests.map(test => [
      test.priority_rank,
      test.testcase_id,
      test.score.toFixed(4),
      test.action,
      test.coverage.toFixed(2),
      test.runtime_seconds.toFixed(2),
      (test.pass_rate * 100).toFixed(1)
    ])
    
    const csv = [headers, ...rows].map(row => row.join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'regression_results.csv'
    a.click()
  }

  return (
    <div className="test-results-table">
      <div className="table-header">
        <div className="table-summary">
          <div className="summary-item">
            <span className="summary-label">Total Tests:</span>
            <span className="summary-value">{summary.total_tests}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Selected:</span>
            <span className="summary-value success">{summary.selected}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Excluded:</span>
            <span className="summary-value warning">{summary.excluded}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Optimization:</span>
            <span className="summary-value">{(summary.optimization_ratio * 100).toFixed(0)}%</span>
          </div>
        </div>
        <button className="export-btn" onClick={exportToCSV}>
          <Download size={16} />
          Export CSV
        </button>
      </div>

      <div className="table-container">
        <table className="results-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('priority_rank')}>Rank</th>
              <th onClick={() => handleSort('testcase_id')}>Test ID</th>
              <th onClick={() => handleSort('score')}>Score</th>
              <th onClick={() => handleSort('action')}>Priority</th>
              <th onClick={() => handleSort('coverage')}>Coverage</th>
              <th onClick={() => handleSort('runtime_seconds')}>Runtime</th>
              <th onClick={() => handleSort('pass_rate')}>Pass Rate</th>
            </tr>
          </thead>
          <tbody>
            {sortedTests.map((test, idx) => {
              const badge = getActionBadge(test.action)
              return (
                <tr key={idx}>
                  <td className="rank-cell">#{test.priority_rank}</td>
                  <td className="test-id-cell">{test.testcase_id}</td>
                  <td className="score-cell">{test.score.toFixed(4)}</td>
                  <td className="priority-cell">
                    <span className={`priority-badge ${badge.class}`}>
                      {badge.text}
                    </span>
                  </td>
                  <td>{test.coverage.toFixed(1)}%</td>
                  <td>{test.runtime_seconds.toFixed(1)}s</td>
                  <td>{(test.pass_rate * 100).toFixed(0)}%</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {ranked_tests.length > 10 && (
        <button 
          className="expand-btn"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? (
            <>
              <ChevronUp size={16} />
              Show Less
            </>
          ) : (
            <>
              <ChevronDown size={16} />
              Show All {ranked_tests.length} Tests
            </>
          )}
        </button>
      )}
    </div>
  )
}

export default TestResultsTable

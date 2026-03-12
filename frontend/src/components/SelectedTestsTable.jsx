import React from 'react';
import './SelectedTestsTable.css';

function SelectedTestsTable({ tests }) {
  if (!tests || tests.length === 0) {
    return <div className="selected-tests-table-empty">No selected test cases to display.</div>;
  }

  // Display only a subset of columns for clarity
  const columns = [
    'testcase_id', 'module_name', 'coverage', 'runtime_seconds', 'action', 'pass_rate'
  ];

  return (
    <div className="selected-tests-table-wrapper">
      <h3>Selected Test Cases (Top 50% by Coverage & Runtime)</h3>
      <table className="selected-tests-table">
        <thead>
          <tr>
            {columns.map(col => <th key={col}>{col.replace('_', ' ').toUpperCase()}</th>)}
          </tr>
        </thead>
        <tbody>
          {tests.map((test, idx) => (
            <tr key={idx}>
              {columns.map(col => <td key={col}>{test[col]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SelectedTestsTable;

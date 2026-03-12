import React, { useEffect, useState } from 'react';
import SelectedTestsTable from './components/SelectedTestsTable';

function SelectedTestsDisplay() {
  const [tests, setTests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchSelectedTests() {
      try {
        const res = await fetch('/api/selected-tests');
        if (!res.ok) throw new Error('Failed to fetch selected test cases');
        const data = await res.json();
        setTests(data.tests);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchSelectedTests();
  }, []);

  if (loading) return <div>Loading selected test cases...</div>;
  if (error) return <div style={{color: 'red'}}>Error: {error}</div>;

  return <SelectedTestsTable tests={tests} />;
}

export default SelectedTestsDisplay;

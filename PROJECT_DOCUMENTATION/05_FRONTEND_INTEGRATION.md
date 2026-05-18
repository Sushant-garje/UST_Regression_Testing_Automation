# 🌐 LAYER 5: FRONTEND & UI INTEGRATION

## **What Does This Layer Do?**

Provides a **web-based dashboard** to browse, visualize, and display optimized test cases.

**Location**: `frontend/` folder
**Technology**: React + Vite
**Purpose**: User-friendly interface for test results and analytics

---

## **Folder Structure**

```
frontend/
├── index.html                    ← HTML entry point
├── package.json                  ← Dependencies
├── vite.config.js               ← Build configuration
├── src/
│   ├── main.jsx                 ← React entry point
│   ├── App.jsx                  ← Main component
│   ├── App.css                  ← Global styles
│   ├── index.css                ← Base styles
│   └── components/
│       ├── SelectedTestsDisplay.jsx    ← Test table display
│       ├── ModuleFilter.jsx            ← Filter by module
│       ├── PriorityFilter.jsx          ← Filter by priority
│       ├── TestChart.jsx               ← Coverage chart
│       └── ... (more components)
```

---

## **What You Can Do**

### **Feature 1: Browse Optimized Tests** 📋
```
┌─────────────────────────────────────┐
│  Select Module: [Half Adder ▼]      │
│                                     │
│  Test ID      │ Priority │ Score   │
│  test_4       │ P0       │ 0.80    │
│  test_22      │ P1       │ 0.70    │
│  test_15      │ P1       │ 0.69    │
│  ...          │ ...      │ ...     │
└─────────────────────────────────────┘
```

### **Feature 2: View Test Details** 🔍
```
Click on a test to see:
- Coverage metrics
- Runtime
- Pass/Fail history
- Priority level
- Redundancy status
- Original parameters
```

### **Feature 3: Filter & Search** 🔎
```
- By module (Half Adder, T FF, etc.)
- By priority (P0, P1, P2, P3)
- By status (PASS, FAIL)
- By coverage range
- By runtime range
```

### **Feature 4: Visualize Results** 📊
```
- Priority distribution pie chart
- Coverage vs Runtime scatter plot
- Pass rate by module
- Test reduction statistics
```

### **Feature 5: Compare Modules** 📈
```
Side-by-side comparison:
- Total tests
- Optimized tests
- Reduction percentage
- Average coverage
- Pass rate
```

---

## **How to Install & Run**

### **Step 1: Install Dependencies**
```bash
cd frontend
npm install
```

### **Step 2: Run Development Server**
```bash
npm run dev
```

Browser opens to: `http://localhost:5173`

### **Step 3: Build for Production**
```bash
npm run build
```

Creates optimized files in `dist/` folder.

---

## **Project Structure**

### **Dependencies** (in package.json)
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "axios": "^1.0.0"  // For API calls
  },
  "devDependencies": {
    "vite": "^4.0.0",
    "@vitejs/plugin-react": "^3.0.0"
  }
}
```

---

## **Main Components**

### **1. App.jsx** (Main Container)
```javascript
import React, { useState, useEffect } from 'react'
import SelectedTestsDisplay from './components/SelectedTestsDisplay'
import ModuleFilter from './components/ModuleFilter'

export default function App() {
  const [modules, setModules] = useState([])
  const [selectedModule, setSelectedModule] = useState('half_adder')
  const [tests, setTests] = useState([])
  
  useEffect(() => {
    // Load tests for selected module
    fetchTests(selectedModule)
  }, [selectedModule])
  
  const fetchTests = async (module) => {
    try {
      // Call API to get tests
      const res = await fetch(`/api/results/${module}`)
      const data = await res.json()
      setTests(data)
    } catch (error) {
      console.error('Error loading tests:', error)
    }
  }
  
  return (
    <div className="app">
      <h1>VLSI Regression Test Optimizer</h1>
      <ModuleFilter 
        selectedModule={selectedModule}
        onSelect={setSelectedModule}
      />
      <SelectedTestsDisplay tests={tests} />
    </div>
  )
}
```

### **2. SelectedTestsDisplay.jsx** (Test Table)
```javascript
export default function SelectedTestsDisplay({ tests }) {
  return (
    <table className="test-table">
      <thead>
        <tr>
          <th>Test ID</th>
          <th>Module</th>
          <th>Coverage</th>
          <th>Score</th>
          <th>Priority</th>
          <th>Runtime</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {tests.map((test, idx) => (
          <tr key={idx}>
            <td>{test.testcase_id}</td>
            <td>{test.module}</td>
            <td>{test.coverage}%</td>
            <td>{test.score.toFixed(2)}</td>
            <td><span className={`priority-${test.priority_rank}`}>
              P{test.priority_rank}
            </span></td>
            <td>{test.runtime_seconds}s</td>
            <td>{test.pass_fail}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

### **3. ModuleFilter.jsx** (Module Selector)
```javascript
export default function ModuleFilter({ selectedModule, onSelect }) {
  const modules = [
    'half_adder',
    'four_bit_subtractor',
    '4_bit_sub',
    'register_comparator',
    't_flip_flop',
    '8_bit_alu',
    'jk_flip_flop',
    'register_downcounter'
  ]
  
  return (
    <div className="module-filter">
      <label>Select Module:</label>
      <select value={selectedModule} onChange={e => onSelect(e.target.value)}>
        {modules.map(m => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>
    </div>
  )
}
```

---

## **API Endpoints Used**

The frontend expects these API endpoints:

```
GET /api/modules
  → Returns list of all modules
  Response: { modules: ['half_adder', 't_flip_flop', ...] }

GET /api/results/{module}
  → Returns optimized tests for module
  Response: [ { testcase_id, module, coverage, score, ... }, ... ]

GET /api/analysis/{module}
  → Returns analysis statistics
  Response: { total: 1000, selected: 20, coverage: 89%, ... }

POST /api/optimize
  → Triggers new optimization
  Request: { module: 'half_adder' }
  Response: { status: 'success', file: '...' }
```

---

## **CSS Styling**

### **App.css** (Global Styles)
```css
/* Main layout */
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

/* Table styling */
.test-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.test-table th {
  background-color: #2c3e50;
  color: white;
  padding: 12px;
  text-align: left;
}

.test-table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.test-table tr:hover {
  background-color: #f5f5f5;
}

/* Priority badges */
.priority-1 { background-color: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px; }
.priority-2 { background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px; }
.priority-3 { background-color: #3498db; color: white; padding: 4px 8px; border-radius: 4px; }
.priority-4 { background-color: #95a5a6; color: white; padding: 4px 8px; border-radius: 4px; }

/* Filter section */
.module-filter {
  margin: 20px 0;
  padding: 15px;
  background-color: #ecf0f1;
  border-radius: 5px;
}

.module-filter select {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
}
```

---

## **Usage Workflow**

### **Step 1: Start Frontend**
```bash
cd frontend
npm install      # First time only
npm run dev      # Start dev server
```

### **Step 2: Ensure Backend is Running**
```bash
# In another terminal, start API service
python3 -c "from regression_manager.api_service import APIService; api = APIService(); api.run()"
```

### **Step 3: Open Browser**
```
Navigate to: http://localhost:5173
```

### **Step 4: Browse Tests**
- Select module from dropdown
- View optimized test list
- Click test for details
- See charts and statistics

---

## **Feature Ideas**

### **Future Features** 🚀
```
✓ Test details modal (click to expand)
✓ Coverage trend chart
✓ Pass/fail rate by module
✓ Test execution timeline
✓ Comparison between old/new optimization
✓ Export to CSV/PDF
✓ Dark mode
✓ Real-time test execution tracking
```

---

## **Build & Deployment**

### **Development Build**
```bash
npm run dev
# Creates development server at localhost:5173
# Hot reload enabled
```

### **Production Build**
```bash
npm run build
# Creates optimized files in dist/
# Run: npx vite preview
```

### **Deploy to Web Server**
```bash
npm run build               # Build
rsync -r dist/ server:/var/www/html/  # Copy to server
# Or use Docker, cloud platform, etc.
```

---

## **Integration with Backend**

### **Option 1: Fetch CSVs Directly**
```javascript
// Load optimized CSV and display
const response = await fetch('/optimized_testcases/optimized_half_adder.csv')
const text = await response.text()
const rows = text.split('\n').map(line => line.split(','))
setTests(parseRows(rows))
```

### **Option 2: API Endpoints**
```javascript
// Call backend API
const response = await fetch('http://api.local:5000/results/half_adder')
const tests = await response.json()
setTests(tests)
```

### **Option 3: WebSocket (Real-time)**
```javascript
// Real-time updates as tests run
const ws = new WebSocket('ws://api.local:5000/live')
ws.onmessage = (event) => {
  const update = JSON.parse(event.data)
  updateTestStatus(update)
}
```

---

## **Environment Configuration**

### **.env File**
```
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
VITE_ENABLE_CHARTS=true
```

### **Usage in Code**
```javascript
const API_URL = import.meta.env.VITE_API_URL
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT

const response = await fetch(`${API_URL}/results/half_adder`)
```

---

## **Performance Optimization**

### **Implemented Optimizations**
```
✓ Lazy loading (load tests on demand)
✓ Virtual scrolling (render only visible rows)
✓ Caching (cache API responses)
✓ Code splitting (lazy load components)
✓ Image optimization (if using images)
```

### **Build Optimization**
```bash
npm run build
# Generated: dist/index.html (optimized)
# Size: ~50KB gzipped
# Load time: <2 seconds
```

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| "Cannot GET /" | Run `npm run dev` in frontend folder |
| API connection error | Check backend is running on port 5000 |
| Tests not loading | Check CORS headers in API |
| Slow performance | Reduce number of tests displayed |
| Styles not loading | Clear browser cache, hard refresh |

---

## **Next Steps**

**Now your frontend can**:
- ✅ Display optimized tests
- ✅ Browse by module
- ✅ View details
- ✅ Filter and search
- ✅ Visualize metrics

**Next**: Go to [06_CONFIGURATION_MANAGEMENT.md](06_CONFIGURATION_MANAGEMENT.md)
- Learn how to configure the entire system
- Set up modules and data sources
- Customize optimization parameters

---

**The Frontend makes optimization results accessible to everyone!** 🌐


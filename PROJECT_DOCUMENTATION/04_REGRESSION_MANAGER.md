# 🛠️ LAYER 4: REGRESSION MANAGER (CORE SERVICES)

## **What is the Regression Manager?**

Core Python module that provides **reusable components** for test optimization, prioritization, and analysis. Think of it as the "engine" that powers the optimization.

**Location**: `regression_manager/` folder
**Purpose**: Provide APIs and services for scoring, prioritization, and analysis
**Use For**: Building custom tools, integrations, CI/CD pipelines

---

## **Folder Structure**

```
regression_manager/
├── __init__.py                      ← Package initialization
├── scoring_engine.py                ← Test scoring logic
├── prioritization_engine.py         ← Priority assignment
├── coverage_parser.py               ← Coverage metric extraction
├── redundancy_detector.py           ← Find duplicate tests
├── feature_engineering.py           ← Generate features
├── gemini_regression_agent.py       ← AI-powered analysis
├── load_optimizer.py                ← Load balancing
├── log_parser.py                    ← Parse test logs
├── llm_copilot.py                   ← LLM integration
├── integrated_copilot.py            ← Copilot wrapper
├── api_service.py                   ← REST API endpoints
├── config.py                        ← Configuration
├── data_loader.py                   ← Load CSV files
└── regression_manager_agent.py      ← Main orchestrator
```

---

## **Core Components**

### **1. Scoring Engine** 📊
**File**: `scoring_engine.py`

**Purpose**: Calculate test importance scores

**Key Functions**:
```python
def calculate_coverage_score(test_coverage, max_coverage):
    """Score based on coverage"""
    return test_coverage / max_coverage

def calculate_efficiency_score(coverage, runtime):
    """Score balancing coverage and speed"""
    normalized_runtime = runtime / max_runtime
    return (coverage * 0.6) + (1 - normalized_runtime * 0.4)

def calculate_final_score(efficiency, pass_rate_impact):
    """Combine factors into final score"""
    return (efficiency * 0.5) + (pass_rate_impact * 0.5)
```

**Usage**:
```python
from regression_manager.scoring_engine import ScoringEngine

scorer = ScoringEngine(df)
scores = scorer.calculate_scores()
```

---

### **2. Prioritization Engine** 🎯
**File**: `prioritization_engine.py`

**Purpose**: Assign priority levels (P0-P3)

**Key Functions**:
```python
def assign_priorities(scores):
    """Map scores to P0-P3 priorities"""
    priorities = []
    for score in scores:
        if score >= 0.80:
            priorities.append('P0')  # Critical
        elif score >= 0.60:
            priorities.append('P1')  # Important
        elif score >= 0.40:
            priorities.append('P2')  # Secondary
        else:
            priorities.append('P3')  # Low
    return priorities

def filter_by_priority(df, priority_level):
    """Get all P0 or P1 tests, etc."""
    return df[df['priority'] == priority_level]
```

**Usage**:
```python
from regression_manager.prioritization_engine import PrioritizationEngine

prioritizer = PrioritizationEngine(df)
df = prioritizer.assign_priorities()

# Get only P0 tests
critical_tests = df[df['priority_rank'] == 'P0']
```

---

### **3. Coverage Parser** 📈
**File**: `coverage_parser.py`

**Purpose**: Extract and validate coverage metrics

**Key Functions**:
```python
def parse_coverage(coverage_value):
    """Convert various formats to percentage"""
    # Handles: 50, 50%, 0.50, etc.

def aggregate_coverage(test_list):
    """Calculate combined coverage"""
    # Union of all test coverages

def coverage_delta(old_coverage, new_coverage):
    """Calculate coverage improvement"""
```

**Usage**:
```python
from regression_manager.coverage_parser import CoverageParser

parser = CoverageParser()
coverage = parser.aggregate_coverage(selected_tests)
print(f"Combined coverage: {coverage}%")
```

---

### **4. Redundancy Detector** 🔍
**File**: `redundancy_detector.py`

**Purpose**: Find and mark duplicate/similar tests

**Key Functions**:
```python
def calculate_similarity(test1, test2):
    """How similar are two tests?"""
    # Returns 0-1 (1 = identical)

def find_redundant_tests(test_list, threshold=0.90):
    """Find tests that are 90%+ similar"""
    redundant = []
    for i, t1 in enumerate(test_list):
        for j, t2 in enumerate(test_list[i+1:]):
            if calculate_similarity(t1, t2) > threshold:
                redundant.append((i, j))
    return redundant

def keep_best_of_duplicates(test_list, redundancies):
    """Remove redundant tests, keep highest-scoring"""
```

**Usage**:
```python
from regression_manager.redundancy_detector import RedundancyDetector

detector = RedundancyDetector(test_dataframe)
redundancies = detector.find_redundant_tests(threshold=0.90)
cleaned_tests = detector.remove_redundancy()
```

---

### **5. Feature Engineering** 🔧
**File**: `feature_engineering.py`

**Purpose**: Generate derived features for better scoring

**Key Functions**:
```python
def generate_features(df):
    """Create derived columns"""
    df['rolling_mean_coverage'] = df['coverage'].rolling(window=5).mean()
    df['coverage_trend'] = df['coverage'].diff()
    df['failure_pattern'] = calculate_failure_frequency(df)
    return df

def normalize_features(df):
    """Scale features to 0-1"""
    for col in ['coverage', 'runtime', 'score']:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df
```

**Usage**:
```python
from regression_manager.feature_engineering import FeatureEngineering

engineer = FeatureEngineering(df)
df_with_features = engineer.generate_features()
```

---

### **6. LLM/Copilot Integration** 🤖
**Files**: `gemini_regression_agent.py`, `llm_copilot.py`

**Purpose**: AI-powered test analysis and recommendations

**Key Functions**:
```python
def analyze_test_failures(failures, context):
    """Use AI to analyze why tests failed"""
    # Sends to Gemini API
    # Returns analysis and recommendations

def suggest_optimizations(test_results):
    """AI suggests test improvements"""
    # Analyzes patterns
    # Recommends which tests to prioritize

def root_cause_analysis(failed_test, logs):
    """AI examines logs to find root cause"""
```

**Usage**:
```python
from regression_manager.gemini_regression_agent import GeminiAgent

agent = GeminiAgent(api_key="...")
analysis = agent.analyze_failures(df_failures)
print(analysis['recommendations'])
```

---

## **Main Orchestrator**

### **Regression Manager Agent** 🎭
**File**: `regression_manager_agent.py`

**Purpose**: Orchestrate entire optimization pipeline

**Key Functions**:
```python
class RegressionManagerAgent:
    
    def __init__(self, config):
        """Initialize with configuration"""
        self.scorer = ScoringEngine()
        self.prioritizer = PrioritizationEngine()
        self.coverage_parser = CoverageParser()
        self.redundancy_detector = RedundancyDetector()
    
    def optimize_tests(self, df):
        """Run complete optimization"""
        # 1. Score tests
        df = self.scorer.calculate_scores(df)
        
        # 2. Detect redundancy
        redundant = self.redundancy_detector.find_redundant_tests(df)
        df = self.redundancy_detector.remove_redundancy(df)
        
        # 3. Generate features
        engineer = FeatureEngineering(df)
        df = engineer.generate_features()
        
        # 4. Assign priorities
        df = self.prioritizer.assign_priorities(df)
        
        # 5. Select best tests
        selected = self.select_tests(df, target_coverage=0.85)
        
        return selected
```

**Usage**:
```python
from regression_manager.regression_manager_agent import RegressionManagerAgent

agent = RegressionManagerAgent(config)
optimized_tests = agent.optimize_tests(raw_dataframe)
```

---

## **Data Services**

### **Data Loader** 📂
**File**: `data_loader.py`

```python
class DataLoader:
    def load_csv(self, filepath):
        """Load and validate CSV"""
    
    def load_all_modules(self, config):
        """Load all module CSVs"""
    
    def save_csv(self, df, filepath):
        """Save optimized CSV"""
```

---

## **API Service** 🔌

### **REST API Endpoints**
**File**: `api_service.py`

**Endpoints**:
```python
# Start API server
python3 -c "from regression_manager.api_service import APIService; api = APIService(); api.run()"

# Or use in code
from regression_manager.api_service import APIService

api = APIService()
api.register_route('/optimize', optimize_tests)
api.run(port=5000)
```

**Available Endpoints**:
```
GET  /modules              - List all modules
GET  /modules/{name}       - Get module details
POST /optimize             - Run optimization
GET  /results/{module}     - Get optimized tests
GET  /analysis/{module}    - Get analysis report
```

---

## **Configuration** ⚙️

**File**: `config.py`

```python
class Config:
    # Scoring weights
    COVERAGE_WEIGHT = 0.6
    RUNTIME_WEIGHT = 0.4
    
    # Priorities
    P0_THRESHOLD = 0.80
    P1_THRESHOLD = 0.60
    P2_THRESHOLD = 0.40
    
    # Optimization
    COVERAGE_TARGET = 0.85
    REDUNDANCY_THRESHOLD = 0.90
    
    # Integration
    API_PORT = 5000
    ENABLE_COPILOT = True
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

---

## **Usage Examples**

### **Example 1: Score Tests**
```python
from regression_manager.scoring_engine import ScoringEngine
import pandas as pd

df = pd.read_csv('normalized_half_adder.csv')
scorer = ScoringEngine()
df['score'] = scorer.calculate_scores(df)
print(df[['testcase_id', 'score']].head())
```

### **Example 2: Prioritize Tests**
```python
from regression_manager.prioritization_engine import PrioritizationEngine

prioritizer = PrioritizationEngine()
df['priority'] = prioritizer.assign_priorities(df['score'])

# Get P0 tests only
p0_tests = df[df['priority'] == 'P0']
```

### **Example 3: Complete Optimization**
```python
from regression_manager.regression_manager_agent import RegressionManagerAgent

agent = RegressionManagerAgent(config={
    'coverage_target': 0.85,
    'max_selection': None
})

optimized = agent.optimize_tests(df)
optimized.to_csv('optimized_tests.csv', index=False)
```

### **Example 4: API Integration**
```python
from regression_manager.api_service import APIService

api = APIService()
api.run(port=5000)

# Then query via HTTP:
# curl http://localhost:5000/modules
# curl http://localhost:5000/results/half_adder
```

---

## **Integration Points**

### **With CI/CD Pipeline** 🔄
```python
# In your CI/CD script (Jenkins, GitLab CI, etc.)
from regression_manager import RegressionManagerAgent

# 1. Load latest test results
results = load_test_results()

# 2. Optimize
agent = RegressionManagerAgent()
optimized = agent.optimize_tests(results)

# 3. Run only optimized tests
for test_id in optimized['testcase_id']:
    run_test(test_id)
```

### **With Test Frameworks** 🧪
```python
# In pytest conftest.py
from regression_manager import PrioritizationEngine

@pytest.fixture(scope="session")
def test_order():
    """Pytest plugin to run tests in priority order"""
    prioritizer = PrioritizationEngine()
    return prioritizer.get_execution_order()
```

### **With Frontend** 🎨
```python
# In React component
import axios from 'axios'

// Call Regression Manager API
axios.get('http://api:5000/results/half_adder')
  .then(res => {
    // Display optimized tests
    setTests(res.data)
  })
```

---

## **Performance Benchmarks**

| Operation | Time | Module Size |
|-----------|------|-------------|
| Load CSV | 50ms | 1000 rows |
| Calculate scores | 200ms | 1000 tests |
| Detect redundancy | 150ms | 1000 tests |
| Assign priorities | 50ms | 1000 tests |
| Select tests | 100ms | 1000 tests |
| **Total** | **550ms** | All operations |

---

## **Key Classes & Methods**

| Module | Class | Key Methods |
|--------|-------|-------------|
| `scoring_engine.py` | `ScoringEngine` | `calculate_scores()` |
| `prioritization_engine.py` | `PrioritizationEngine` | `assign_priorities()` |
| `redundancy_detector.py` | `RedundancyDetector` | `find_redundant_tests()` |
| `coverage_parser.py` | `CoverageParser` | `aggregate_coverage()` |
| `feature_engineering.py` | `FeatureEngineering` | `generate_features()` |
| `regression_manager_agent.py` | `RegressionManagerAgent` | `optimize_tests()` |
| `api_service.py` | `APIService` | `run()`, `register_route()` |

---

## **Next Steps**

**Use Regression Manager for**:
- ✅ Custom optimization logic
- ✅ CI/CD integration
- ✅ API endpoints
- ✅ Advanced analysis
- ✅ Test framework plugins

**Next**: Go to [05_FRONTEND_INTEGRATION.md](05_FRONTEND_INTEGRATION.md)
- Learn how to use the optimized data in web UI
- Build dashboards and reports
- Create test result visualizations

---

**The Regression Manager is the heart of the system - all optimization logic lives here!** ⚙️


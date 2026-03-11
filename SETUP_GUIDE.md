# VLSI Regression Testing Copilot - Complete Setup Guide

## Overview

This is a complete AI-powered copilot for VLSI regression testing that includes:
- ✅ Regression Manager Agent (test selection & prioritization)
- ✅ Load Optimizer Agent (CPU/GPU/Cloud resource allocation)
- ✅ Coverage Parser (VCS, Questa, Xcelium support)
- ✅ Google Gemini Integration (AI insights & chat interface)
- ✅ REST API Service (FastAPI)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Gemini API Key

Get your API key from: https://makersuite.google.com/app/apikey

```bash
# Linux/Mac
export GOOGLE_API_KEY='your-api-key-here'

# Windows PowerShell
$env:GOOGLE_API_KEY='your-api-key-here'

# Or create .env file
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

### 3. Run Basic Example

```bash
python run_example.py
```

### 4. Run with AI Copilot

```bash
python example_copilot_usage.py
```

### 5. Start API Server

```bash
uvicorn regression_manager.api_service:app --reload --port 8000
```

## Features

### 1. Regression Manager Agent

**What it does:**
- Analyzes test history and coverage data
- Identifies redundant tests
- Prioritizes critical tests
- Optimizes regression suite

**Usage:**
```python
from regression_manager import RegressionManagerAgent

agent = RegressionManagerAgent(
    csv_path='rag_training_data.csv',
    log_path='sim.log'
)

result = agent.run()
```

### 2. Load Optimizer Agent

**What it does:**
- Allocates tests to CPU/GPU/Cloud resources
- Estimates execution cost
- Tracks server usage
- Optimizes resource utilization

**Usage:**
```python
from regression_manager.load_optimizer import LoadOptimizer

optimizer = LoadOptimizer()
optimizer.configure_resources(cpu_units=16, gpu_units=4, cloud_units=50)
df_allocated = optimizer.allocate_tests(tests_df)
```

### 3. Coverage Parser

**What it does:**
- Parses VCS, Questa, Xcelium coverage reports
- Extracts line, branch, toggle, FSM coverage
- Provides module-level coverage breakdown

**Usage:**
```python
from regression_manager.coverage_parser import CoverageParser

parser = CoverageParser('coverage.rpt', report_type='vcs')
coverage_data = parser.parse()
```

### 4. AI Copilot (Google Gemini)

**What it does:**
- Analyzes regression results with AI
- Explains test scores in natural language
- Suggests critical modules
- Interactive chat interface for VLSI questions

**Usage:**
```python
from regression_manager.llm_copilot import RegressionCopilot

copilot = RegressionCopilot()  # Uses GOOGLE_API_KEY from env

# Analyze results
insights = copilot.analyze_regression_results(result)

# Chat interface
response = copilot.chat("How can I reduce regression time by 30%?")

# Explain test score
explanation = copilot.explain_test_score(test_data)
```

## API Endpoints

### Core Endpoints

#### 1. Optimize Regression
```bash
curl -X POST "http://localhost:8000/optimize-regression" \
     -H "Content-Type: application/json" \
     -d '{
       "csv_path": "rag_training_data.csv",
       "log_path": "sim.log",
       "enable_load_optimizer": true,
       "enable_llm_copilot": true
     }'
```

#### 2. Chat with Copilot
```bash
curl -X POST "http://localhost:8000/copilot/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What are best practices for regression test selection?"
     }'
```

#### 3. Explain Test Score
```bash
curl -X POST "http://localhost:8000/copilot/explain-test" \
     -H "Content-Type: application/json" \
     -d '{
       "testcase_id": "jk_ff_test_seed1",
       "score": 0.85,
       "coverage": 95.0,
       "runtime_seconds": 145.0,
       "pass_rate": 0.92
     }'
```

#### 4. Configure Resources
```bash
curl -X POST "http://localhost:8000/resources/configure" \
     -H "Content-Type: application/json" \
     -d '{
       "cpu_units": 32,
       "gpu_units": 8,
       "cloud_units": 100
     }'
```

#### 5. Parse Coverage Report
```bash
curl -X POST "http://localhost:8000/coverage/parse" \
     -F "coverage_file=@coverage.rpt" \
     -F "report_type=vcs"
```

#### 6. Get Resource Usage
```bash
curl -X GET "http://localhost:8000/resources/usage"
```

## Configuration

### Scoring Weights

Edit `regression_manager/config.py`:

```python
config.scoring_weights.coverage = 0.4    # Coverage importance
config.scoring_weights.efficiency = 0.3  # Runtime efficiency
config.scoring_weights.stability = 0.3   # Test stability
```

### Redundancy Thresholds

```python
config.redundancy_thresholds.pass_rate_threshold = 0.95
config.redundancy_thresholds.coverage_gain_threshold = 1.0
config.redundancy_thresholds.no_failure_window = 10
```

### Critical Modules

```python
config.critical_modules.modules = [
    "cpu_core",
    "memory_controller",
    "cache_controller"
]
config.critical_modules.critical_weight_multiplier = 1.5
```

## Input Data Format

### CSV Format (Required)

```csv
module,test,seed,rtl_version,git_commit,result,coverage,sim_time,test_runtime
jk_ff,test,1,v1.0,commit_001,PASS,95.0,145,0.5
jk_ff,test,2,v1.0,commit_001,FAIL,85.0,120,0.4
```

**Required Columns:**
- `module`: Module name
- `test`: Test name
- `seed`: Random seed
- `result`: PASS/FAIL/RESET
- `coverage`: Coverage percentage
- `sim_time`: Simulation time in seconds

### Simulation Log (Optional)

Standard VCS/Questa/Xcelium log format with:
- Compilation time
- Simulation time
- Memory usage
- Error/warning counts

### Coverage Report (Optional)

Supported formats:
- VCS URG reports
- Questa coverage reports
- Xcelium coverage reports

## Use Cases

### 1. Daily Regression Optimization

```python
# Run every night
agent = RegressionManagerAgent(
    csv_path='daily_tests.csv',
    log_path='sim.log',
    enable_load_optimizer=True
)

result = agent.run()

# Get top priority tests
top_tests = result['ranked_tests'][:50]

# Run only these tests tomorrow
```

### 2. Resource Planning

```python
optimizer = LoadOptimizer()
optimizer.configure_resources(cpu_units=32, gpu_units=8, cloud_units=100)

df_allocated = optimizer.allocate_tests(tests_df)
cost = optimizer.estimate_cost()

print(f"Estimated cost: ${cost['total_cost']:.2f}")
```

### 3. Coverage Analysis

```python
parser = CoverageParser('coverage.rpt', report_type='vcs')
coverage = parser.parse()

print(f"Line Coverage: {coverage['line_coverage']}%")
print(f"Branch Coverage: {coverage['branch_coverage']}%")
```

### 4. AI-Powered Insights

```python
copilot = RegressionCopilot()

# Get insights
insights = copilot.analyze_regression_results(result)
print(insights)

# Ask questions
response = copilot.chat("Which modules are failing most frequently?")
print(response)

# Get recommendations
modules = copilot.suggest_critical_modules(test_history_df)
print(f"Suggested critical modules: {modules}")
```

## Troubleshooting

### Issue: Gemini API Key Not Found

**Solution:**
```bash
export GOOGLE_API_KEY='your-key-here'
# Or add to .env file
```

### Issue: Import Error for google.generativeai

**Solution:**
```bash
pip install google-generativeai
```

### Issue: No Tests Excluded

**Solution:** Adjust redundancy thresholds in config.py

### Issue: Resource Allocation Not Working

**Solution:** Ensure `enable_load_optimizer=True` when creating agent

## Performance

- **Handles**: 10,000+ testcases
- **Time Complexity**: O(n log n)
- **Execution Time**: ~0.1s for 51 tests
- **Memory**: Efficient pandas operations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   API Service (FastAPI)                  │
│  /optimize-regression  /copilot/chat  /resources/*      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│            Regression Manager Agent                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Data Loader  │  │   Feature    │  │   Scoring    │ │
│  │              │→ │  Engineering │→ │   Engine     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Redundancy  │  │Prioritization│  │     Load     │ │
│  │  Detector    │→ │   Engine     │→ │  Optimizer   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│              Google Gemini Copilot                       │
│  • Analyze Results  • Explain Scores  • Chat Interface  │
└─────────────────────────────────────────────────────────┘
```

## Next Steps

1. ✅ Set up Google Gemini API key
2. ✅ Run example scripts
3. ✅ Configure your resource pools
4. ✅ Add your test data
5. ✅ Start API server
6. ✅ Try copilot chat interface
7. ✅ Integrate with your CI/CD pipeline

## Support

For issues or questions:
- Check logs for detailed error messages
- Review ARCHITECTURE.md for technical details
- Run unit tests: `pytest tests/ -v`
- Check API docs: http://localhost:8000/docs

## License

Proprietary - Internal Use Only

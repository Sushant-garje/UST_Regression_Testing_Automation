# Regression Manager Agent - Quick Reference

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Run Example Script
```bash
python run_example.py
```

### Option 2: Programmatic Usage
```python
from regression_manager import RegressionManagerAgent

agent = RegressionManagerAgent(
    csv_path='rag_training_data.csv',
    log_path='sim.log'
)

result = agent.run()
```

### Option 3: API Service
```bash
# Start server
uvicorn regression_manager.api_service:app --reload --port 8000

# Make request
curl -X POST "http://localhost:8000/optimize-regression" \
     -H "Content-Type: application/json" \
     -d '{"csv_path": "rag_training_data.csv", "log_path": "sim.log"}'
```

## Key Formulas

### Coverage Gain
```
coverage_gain = current_coverage - rolling_mean_coverage
```

### Efficiency Score
```
efficiency = coverage_gain / runtime_seconds
```

### Redundancy Detection
```
is_redundant = (pass_rate > 0.95) AND 
               (coverage_gain < 1.0%) AND 
               (no_recent_failures)
```

### Final Score
```
base_score = 0.4 * coverage_gain_norm + 
             0.3 * efficiency_norm + 
             0.3 * (1 - failure_rate)

final_score = (base_score - redundancy_penalty) * critical_boost
```

## Configuration

### Update Weights
```python
from regression_manager.config import config

config.scoring_weights.coverage = 0.5
config.scoring_weights.efficiency = 0.3
config.scoring_weights.stability = 0.2
```

### Update Thresholds
```python
config.redundancy_thresholds.pass_rate_threshold = 0.95
config.redundancy_thresholds.coverage_gain_threshold = 1.0
```

### Set Critical Modules
```python
config.critical_modules.modules = [
    'cpu_core',
    'memory_controller',
    'cache_controller'
]
config.critical_modules.critical_weight_multiplier = 1.5
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| POST | `/optimize-regression` | Run optimization |
| POST | `/upload-and-optimize` | Upload files and optimize |
| GET | `/config` | Get configuration |
| PUT | `/config` | Update configuration |

## Output Structure

```json
{
  "ranked_tests": [
    {
      "testcase_id": "module_test_seed1",
      "module_name": "module",
      "score": 0.87,
      "priority_rank": 1,
      "action": "run_first",
      "coverage": 95.0,
      "runtime_seconds": 10.5,
      "pass_rate": 0.92
    }
  ],
  "excluded_tests": [
    {
      "testcase_id": "module_test_seed2",
      "module_name": "module",
      "reason": "Consistently passing...",
      "pass_rate": 0.98,
      "coverage_gain": 0.5
    }
  ],
  "summary": {
    "total_tests": 100,
    "selected": 85,
    "excluded": 15,
    "optimization_ratio": 0.85
  }
}
```

## Action Labels

| Action | Description | Score Range |
|--------|-------------|-------------|
| `run_first` | Highest priority | Top 25% (Q4) |
| `run_early` | High priority | 50-75% (Q3) |
| `run_normal` | Normal priority | 25-50% (Q2) |
| `run_late` | Low priority | Bottom 25% (Q1) |

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Generate Synthetic Data
```bash
python utils/synthetic_data_generator.py
```

## Module Overview

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `config.py` | Configuration | Weights, thresholds, critical modules |
| `data_loader.py` | Data ingestion | Load and normalize CSV |
| `log_parser.py` | Log parsing | Extract simulation metrics |
| `feature_engineering.py` | Feature computation | Coverage gain, efficiency, stability |
| `scoring_engine.py` | Score calculation | Compute final scores |
| `redundancy_detector.py` | Redundancy detection | Identify low-value tests |
| `prioritization_engine.py` | Test ranking | Rank and label tests |
| `regression_manager_agent.py` | Orchestration | Main workflow |
| `api_service.py` | REST API | FastAPI endpoints |

## Performance

- **Scalability**: 10,000+ testcases
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Execution Time**: ~0.1s for 51 tests

## Common Tasks

### Change Scoring Weights
```bash
curl -X PUT "http://localhost:8000/config" \
     -H "Content-Type: application/json" \
     -d '{
       "coverage_weight": 0.5,
       "efficiency_weight": 0.3,
       "stability_weight": 0.2
     }'
```

### Add Critical Modules
```bash
curl -X PUT "http://localhost:8000/config" \
     -H "Content-Type: application/json" \
     -d '{
       "critical_modules": ["cpu_core", "memory_controller", "jk_ff"]
     }'
```

### Upload and Optimize
```bash
curl -X POST "http://localhost:8000/upload-and-optimize" \
     -F "csv_file=@rag_training_data.csv" \
     -F "log_file=@sim.log"
```

## Troubleshooting

### Issue: CSV file not found
**Solution**: Ensure file path is correct and file exists

### Issue: Missing columns in CSV
**Solution**: CSV must have: module, test, seed, result, coverage, sim_time

### Issue: Weights don't sum to 1.0
**Solution**: Ensure coverage_weight + efficiency_weight + stability_weight = 1.0

### Issue: No tests excluded
**Solution**: Adjust redundancy thresholds if needed

## Extension Points

### Add ML Predictor
```python
# Create ml_predictor.py
class FailurePredictor:
    def predict(self, df):
        # ML logic here
        pass

# Integrate in regression_manager_agent.py
def _predict_failures(self, df):
    predictor = FailurePredictor()
    df['failure_prob'] = predictor.predict(df)
    return df
```

### Add Custom Scorer
```python
# Extend scoring_engine.py
class CustomScoringEngine(ScoringEngine):
    def compute_custom_score(self):
        # Custom scoring logic
        pass
```

## Best Practices

1. **Always validate input data** before running optimization
2. **Adjust weights** based on your verification priorities
3. **Review excluded tests** to ensure no critical tests are removed
4. **Monitor score distribution** to ensure balanced prioritization
5. **Update critical modules list** as your design evolves
6. **Run unit tests** after configuration changes
7. **Log all optimization runs** for historical analysis

## Support

For issues or questions:
1. Check logs for detailed error messages
2. Review ARCHITECTURE.md for technical details
3. Run unit tests to verify system health
4. Check configuration values

## Version

Current Version: 1.0.0

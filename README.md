# Regression Manager Agent

Production-grade intelligent regression test optimization system for semiconductor verification workflows.

## Overview

The Regression Manager Agent is a modular, extensible backend service that optimizes regression test execution by:

- Selecting optimal testcases for maximum coverage per unit runtime
- Detecting and excluding redundant testcases
- Identifying consistently passing low-value tests
- Prioritizing critical-path modules
- Generating ranked, optimized regression plans

## Architecture

```
regression_manager/
├── config.py                    # Centralized configuration
├── data_loader.py               # CSV data ingestion
├── log_parser.py                # Simulation log parsing
├── feature_engineering.py       # Derived metric computation
├── scoring_engine.py            # Final score calculation
├── redundancy_detector.py       # Redundancy identification
├── prioritization_engine.py     # Test ranking and planning
├── regression_manager_agent.py  # Main orchestration
└── api_service.py               # FastAPI REST service
```

## Intelligence Logic

### 1. Coverage Gain
```
coverage_gain = testcase_coverage - rolling_mean_coverage
```

### 2. Efficiency Score
```
efficiency_score = coverage_gain / runtime_seconds
```

### 3. Stability Metric
```
pass_rate = cumulative_passes / cumulative_runs
```

### 4. Redundancy Detection
Mark as redundant if:
- `pass_rate > 0.95`
- `coverage_gain < 1%`
- No failures in last N runs

### 5. Priority Boost
If module in critical modules list:
```
score *= critical_weight_multiplier
```

### 6. Final Regression Score
```
final_score = (
    weight_coverage * coverage_gain_normalized +
    weight_efficiency * efficiency_normalized +
    weight_stability * (1 - failure_rate)
) - redundancy_penalty
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Programmatic Usage

```python
from regression_manager import RegressionManagerAgent

agent = RegressionManagerAgent(
    csv_path='rag_training_data.csv',
    log_path='sim.log'
)

result = agent.run()

print(result['summary'])
print(result['ranked_tests'][:10])
print(result['excluded_tests'])
```

### API Usage

Start the server:
```bash
uvicorn regression_manager.api_service:app --reload
```

Optimize regression:
```bash
curl -X POST "http://localhost:8000/optimize-regression" \
     -H "Content-Type: application/json" \
     -d '{"csv_path": "rag_training_data.csv", "log_path": "sim.log"}'
```

Update configuration:
```bash
curl -X PUT "http://localhost:8000/config" \
     -H "Content-Type: application/json" \
     -d '{"coverage_weight": 0.5, "efficiency_weight": 0.3, "stability_weight": 0.2}'
```

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /optimize-regression` - Run optimization
- `POST /upload-and-optimize` - Upload files and optimize
- `GET /config` - Get current configuration
- `PUT /config` - Update configuration

## Output Format

```json
{
  "ranked_tests": [
    {
      "testcase_id": "jk_ff_test_seed1",
      "module_name": "jk_ff",
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
      "testcase_id": "jk_ff_test_seed14",
      "module_name": "jk_ff",
      "reason": "Consistently passing (pass_rate > 0.95), low coverage gain (< 1.0%), no failures in last 10 runs",
      "pass_rate": 0.98,
      "coverage_gain": 0.5
    }
  ],
  "summary": {
    "total_tests": 28,
    "selected": 22,
    "excluded": 6,
    "optimization_ratio": 0.79
  }
}
```

## Configuration

Edit `regression_manager/config.py` or use API to update:

```python
from regression_manager.config import config

# Scoring weights (must sum to 1.0)
config.scoring_weights.coverage = 0.4
config.scoring_weights.efficiency = 0.3
config.scoring_weights.stability = 0.3

# Redundancy thresholds
config.redundancy_thresholds.pass_rate_threshold = 0.95
config.redundancy_thresholds.coverage_gain_threshold = 1.0

# Critical modules
config.critical_modules.modules = ['cpu_core', 'memory_controller']
config.critical_modules.critical_weight_multiplier = 1.5
```

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Generate synthetic data:
```bash
python utils/synthetic_data_generator.py
```

## Performance

- Handles 10,000+ testcases efficiently
- Vectorized pandas operations (no O(n²) algorithms)
- Optimized for production workloads
- Comprehensive logging for debugging

## Extensibility

The modular architecture allows easy addition of:

- ML-based failure prediction models
- Reinforcement learning schedulers
- Resource optimization agents
- RAG-based explanation layers

Simply create new modules and integrate via the main agent orchestrator.

## Decision Logic

The agent makes decisions based on:

1. **Historical Performance**: Analyzes pass rates and failure patterns
2. **Coverage Efficiency**: Prioritizes tests with high coverage gain per unit time
3. **Stability**: Balances between stable tests and failure-prone tests
4. **Module Criticality**: Boosts priority for critical system components
5. **Redundancy**: Excludes consistently passing tests with minimal value

## Example

See `example_usage.py` for complete examples.

```bash
python example_usage.py
```

## License

Proprietary - Internal Use Only

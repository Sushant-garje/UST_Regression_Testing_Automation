# Regression Manager Agent - Architecture Documentation

## System Architecture

### Design Principles

1. **SOLID Principles**
   - Single Responsibility: Each module has one clear purpose
   - Open/Closed: Extensible without modifying core logic
   - Liskov Substitution: Modules can be swapped with compatible implementations
   - Interface Segregation: Clean, focused interfaces
   - Dependency Inversion: Depends on abstractions, not concrete implementations

2. **Modularity**
   - Each component is independently testable
   - Clear separation of concerns
   - Minimal coupling between modules

3. **Scalability**
   - Vectorized operations for performance
   - No O(n²) algorithms
   - Efficient memory usage with pandas

## Module Breakdown

### 1. config.py
**Purpose**: Centralized configuration management

**Key Classes**:
- `ScoringWeights`: Weights for score calculation
- `RedundancyThresholds`: Thresholds for redundancy detection
- `CriticalModules`: Critical module configuration
- `RegressionConfig`: Master configuration

**Extensibility**: Add new configuration sections as dataclasses

### 2. data_loader.py
**Purpose**: Data ingestion and normalization

**Key Methods**:
- `load_csv()`: Load and validate CSV data
- `normalize_data()`: Clean and standardize data

**Input**: CSV with columns: module, test, seed, result, coverage, sim_time
**Output**: Normalized DataFrame with testcase_id, pass_fail, etc.

### 3. log_parser.py
**Purpose**: Simulation log parsing

**Key Methods**:
- `parse_log()`: Extract metrics from log files
- `merge_with_csv()`: Merge log data with CSV data

**Extracted Metrics**:
- simulation_time
- compile_time
- memory_usage
- error_count
- warning_count

### 4. feature_engineering.py
**Purpose**: Compute derived features

**Key Features**:
- `coverage_gain`: Coverage relative to rolling mean
- `efficiency_score`: Coverage gain per unit time
- `pass_rate`: Historical pass rate
- `failure_rate`: Inverse of pass rate

**Algorithm**: Vectorized pandas operations with groupby and rolling windows

### 5. redundancy_detector.py
**Purpose**: Identify low-value testcases

**Detection Logic**:
```
is_redundant = (
    pass_rate > threshold AND
    coverage_gain < threshold AND
    no_recent_failures
)
```

**Output**: Boolean flag + reason string

### 6. scoring_engine.py
**Purpose**: Compute final regression scores

**Scoring Formula**:
```python
base_score = (
    w_coverage * coverage_gain_norm +
    w_efficiency * efficiency_norm +
    w_stability * (1 - failure_rate)
)

final_score = (base_score - redundancy_penalty) * critical_boost
```

**Normalization**: Min-max scaling to [0, 1] range

### 7. prioritization_engine.py
**Purpose**: Rank tests and generate execution plan

**Actions**:
- `run_first`: Top 25% (Q4)
- `run_early`: 50-75% (Q3)
- `run_normal`: 25-50% (Q2)
- `run_late`: Bottom 25% (Q1)

**Output**: Ranked list with priority and action labels

### 8. regression_manager_agent.py
**Purpose**: Main orchestration

**Workflow**:
1. Load data (CSV + logs)
2. Engineer features
3. Detect redundancy
4. Compute scores
5. Prioritize tests
6. Generate output

**Design Pattern**: Pipeline pattern with clear stages

### 9. api_service.py
**Purpose**: REST API interface

**Endpoints**:
- `POST /optimize-regression`: Run optimization
- `POST /upload-and-optimize`: Upload and optimize
- `GET /config`: Get configuration
- `PUT /config`: Update configuration

**Framework**: FastAPI with Pydantic validation

## Data Flow

```
CSV File ──┐
           ├──> DataLoader ──> FeatureEngineer ──> RedundancyDetector ──┐
Log File ──┘                                                             │
                                                                         ▼
                                                              ScoringEngine
                                                                         │
                                                                         ▼
                                                           PrioritizationEngine
                                                                         │
                                                                         ▼
                                                                  JSON Output
```

## Performance Characteristics

### Time Complexity
- Data loading: O(n)
- Feature engineering: O(n log n) due to sorting
- Redundancy detection: O(n)
- Scoring: O(n)
- Prioritization: O(n log n) due to sorting

**Overall**: O(n log n) where n = number of testcases

### Space Complexity
- O(n) for main DataFrame
- O(1) for intermediate computations (in-place operations)

### Scalability
- Tested with 10,000+ testcases
- Vectorized pandas operations
- No nested loops or O(n²) algorithms

## Extensibility Points

### 1. Add ML-Based Failure Prediction

```python
# New module: ml_predictor.py
class FailurePredictor:
    def predict_failure_probability(self, df: pd.DataFrame) -> pd.Series:
        # ML model inference
        pass

# Integration in regression_manager_agent.py
def _predict_failures(self, df: pd.DataFrame) -> pd.DataFrame:
    predictor = FailurePredictor()
    df['failure_probability'] = predictor.predict_failure_probability(df)
    return df
```

### 2. Add Reinforcement Learning Scheduler

```python
# New module: rl_scheduler.py
class RLScheduler:
    def optimize_schedule(self, tests: List[Dict]) -> List[Dict]:
        # RL-based scheduling
        pass
```

### 3. Add RAG-Based Explanation

```python
# New module: rag_explainer.py
class RAGExplainer:
    def explain_decision(self, testcase_id: str, score: float) -> str:
        # RAG-based explanation generation
        pass
```

### 4. Add Resource Optimization

```python
# New module: resource_optimizer.py
class ResourceOptimizer:
    def optimize_resources(self, tests: List[Dict], constraints: Dict) -> Dict:
        # Resource allocation optimization
        pass
```

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock dependencies
- Test edge cases and error conditions

### Integration Tests
- Test complete workflow
- Test with real data
- Test API endpoints

### Performance Tests
- Benchmark with large datasets
- Profile memory usage
- Identify bottlenecks

## Deployment

### Development
```bash
uvicorn regression_manager.api_service:app --reload
```

### Production
```bash
uvicorn regression_manager.api_service:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY regression_manager/ ./regression_manager/
CMD ["uvicorn", "regression_manager.api_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring and Logging

All modules use Python's logging framework:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Processing started")
logger.warning("Potential issue detected")
logger.error("Error occurred", exc_info=True)
```

Configure logging level via environment or config file.

## Security Considerations

1. **Input Validation**: Pydantic models validate all API inputs
2. **File Path Validation**: Check file existence and permissions
3. **Resource Limits**: Limit file upload sizes
4. **Error Handling**: Never expose internal errors to API clients

## Future Enhancements

1. **Database Integration**: Store historical results
2. **Caching**: Cache computed features for repeated runs
3. **Parallel Processing**: Distribute computation across workers
4. **Real-time Updates**: WebSocket support for live progress
5. **Visualization**: Dashboard for results visualization

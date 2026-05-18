# ⚙️ CONFIGURATION MANAGEMENT

## **What is Configuration?**

Central place to specify:
- Where your test data is located
- Which modules to optimize
- How to score and prioritize tests
- API settings and integrations

**Main File**: `dataset_config.yaml`
**Backup Files**: `config.py`, `requirements.txt`

---

## **Main Configuration: dataset_config.yaml**

This YAML file controls everything. Edit it to add/remove modules or change data paths.

### **File Structure**

```yaml
# ================================
# 📊 DATASET CONFIGURATION
# ================================

modules:
  half_adder:
    enabled: true
    input_path: "19 aprilt/half_adder_dataset.csv"
    description: "Half Adder - 2-bit addition circuit"
    expected_tests: 20

  t_flip_flop:
    enabled: true
    input_path: "19 aprilt/t_ff_dataset.csv"
    description: "T Flip-Flop - 1-bit memory element"
    expected_tests: 918

  # ... more modules

output:
  lightweight_format: "optimized_testcases/"
  full_data_format: "optimized_testcases_full/"
```

---

## **Adding a New Module**

### **Step 1: Get Your Test Data**
```bash
# Copy new test data to project
cp ~/Downloads/my_new_module.csv ./new_data/

# Or use existing location
ls 19\ aprilt/
# See all available files
```

### **Step 2: Edit dataset_config.yaml**
```yaml
modules:
  # ... existing modules ...
  
  my_new_module:
    enabled: true
    input_path: "new_data/my_new_module.csv"
    description: "My new VLSI circuit"
    expected_tests: 100  # Optional
```

### **Step 3: Run Pipeline**
```bash
python3 normalize_datasets.py && \
python3 export_optimized_tests.py && \
python3 export_with_full_data.py
```

### **Step 4: Use Results**
```bash
ls optimized_testcases/optimized_my_new_module.csv
# ✅ Your optimized tests are ready!
```

---

## **Disabling a Module**

If a module has issues, temporarily disable it:

```yaml
register_counter:
  enabled: false  # Skip this module
  input_path: "..."
  description: "..."
```

Then run pipeline - this module will be skipped.

---

## **Path Configuration**

### **Relative Paths** (recommended)
```yaml
half_adder:
  input_path: "19 aprilt/half_adder_dataset.csv"
  # Relative to project root
```

### **Absolute Paths**
```yaml
half_adder:
  input_path: "/Users/sushant/Downloads/half_adder.csv"
  # Full system path
```

### **Home Directory Path**
```yaml
half_adder:
  input_path: "~/Downloads/half_adder.csv"
  # Expands ~ to home directory
```

### **Network Path** (if mounted)
```yaml
half_adder:
  input_path: "/mnt/network/shared/half_adder.csv"
```

---

## **Python Configuration: config.py**

Optimization parameters that control behavior.

### **Key Settings**

```python
# regression_manager/config.py

class Config:
    
    # ========== SCORING CONFIGURATION ==========
    COVERAGE_WEIGHT = 0.6          # 60% weight to coverage
    RUNTIME_WEIGHT = 0.4           # 40% weight to runtime
    
    # ========== PRIORITY THRESHOLDS ==========
    P0_THRESHOLD = 0.80            # Score >= 0.80 → P0
    P1_THRESHOLD = 0.60            # Score >= 0.60 → P1
    P2_THRESHOLD = 0.40            # Score >= 0.40 → P2
    # Else → P3
    
    # ========== OPTIMIZATION SETTINGS ==========
    COVERAGE_TARGET = 0.85         # Target 85% coverage
    MAX_SELECTION = None           # None = select as needed
    REDUNDANCY_THRESHOLD = 0.90    # 90% similar = redundant
    
    # ========== API CONFIGURATION ==========
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    API_DEBUG = True
    CORS_ENABLED = True
    
    # ========== LLM/COPILOT ==========
    ENABLE_COPILOT = True
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    LLM_MODEL = 'gemini-pro'
    
    # ========== LOGGING ==========
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'regression_manager.log'
```

---

## **How to Customize Scoring**

### **Adjust Weights** (favor coverage over speed or vice versa)

```python
# Default: 60% coverage, 40% speed
COVERAGE_WEIGHT = 0.6
RUNTIME_WEIGHT = 0.4

# Option 1: Favor speed (important for CI/CD)
COVERAGE_WEIGHT = 0.4
RUNTIME_WEIGHT = 0.6

# Option 2: Favor coverage (important for quality)
COVERAGE_WEIGHT = 0.8
RUNTIME_WEIGHT = 0.2
```

### **Adjust Priority Thresholds**

```python
# Default thresholds (generous)
P0_THRESHOLD = 0.80
P1_THRESHOLD = 0.60
P2_THRESHOLD = 0.40

# Option 1: Stricter (fewer P0 tests)
P0_THRESHOLD = 0.95
P1_THRESHOLD = 0.75
P2_THRESHOLD = 0.50

# Option 2: Looser (more P0 tests)
P0_THRESHOLD = 0.60
P1_THRESHOLD = 0.40
P2_THRESHOLD = 0.20
```

### **Adjust Coverage Target**

```python
# Default: Try to keep 85% coverage
COVERAGE_TARGET = 0.85

# Option 1: More aggressive (lower coverage OK)
COVERAGE_TARGET = 0.70  # Accept 70% coverage → fewer tests

# Option 2: More conservative (maintain coverage)
COVERAGE_TARGET = 0.95  # Keep 95% coverage → more tests
```

---

## **Environment Variables**

### **Create .env file**
```bash
# .env (in project root)
GEMINI_API_KEY=your_api_key_here
LOG_LEVEL=DEBUG
API_PORT=8000
DATABASE_URL=postgresql://...
```

### **Load in Python**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

api_key = os.getenv('GEMINI_API_KEY')
log_level = os.getenv('LOG_LEVEL', 'INFO')
api_port = int(os.getenv('API_PORT', 5000))
```

---

## **Requirements File**

### **requirements.txt** (Python dependencies)

```
pandas==1.5.3
numpy==1.24.3
scikit-learn==1.2.2
google-generativeai==0.2.0
flask==2.3.2
flask-cors==4.0.0
python-dotenv==1.0.0
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Configuration by Use Case**

### **Use Case 1: CI/CD Pipeline** (fast, limited tests)
```yaml
# dataset_config.yaml
modules:
  half_adder:
    enabled: true
    input_path: "test_data/half_adder.csv"

# config.py
COVERAGE_TARGET = 0.70      # Accept 70% coverage
REDUNDANCY_THRESHOLD = 0.95 # Aggressive deduplication
RUNTIME_WEIGHT = 0.6        # Favor speed

# Result: ~10 tests, ~1 minute runtime
```

### **Use Case 2: Full Testing** (comprehensive, all tests)
```yaml
# dataset_config.yaml
modules:
  half_adder:
    enabled: true
    
# config.py
COVERAGE_TARGET = 0.99      # Keep 99% coverage
REDUNDANCY_THRESHOLD = 0.99 # Keep all unique tests
MAX_SELECTION = 1000        # Allow many tests

# Result: ~1000 tests, ~100 minutes runtime
```

### **Use Case 3: Quality Focus** (high coverage)
```yaml
# dataset_config.yaml
modules:
  half_adder:
    enabled: true

# config.py
COVERAGE_TARGET = 0.95      # Keep 95% coverage
COVERAGE_WEIGHT = 0.8       # 80% weight to coverage
RUNTIME_WEIGHT = 0.2        # 20% weight to speed

# Result: ~50 tests, ~10 minutes runtime, 95%  coverage
```

---

## **Module Configuration Options**

### **Full Module Config Example**

```yaml
half_adder:
  enabled: true                           # Process this module?
  input_path: "19 aprilt/half_adder_dataset.csv"  # Data location
  description: "Half Adder - 2-bit addition"      # Display name
  expected_tests: 20                      # Expected result (optional)
  
  # Optional: Module-specific settings
  coverage_target: 0.85                   # Override global target
  max_tests: 50                           # Max tests to select
  min_tests: 10                           # Min tests to select
  priority_override: "P0"                 # Force priority if needed
```

---

## **Monitoring Configuration**

### **Enable Detailed Logging**

```python
# config.py
LOG_LEVEL = 'DEBUG'  # Show detailed logs
LOG_FILE = 'regression.log'

# Usage
import logging

logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Loading module: half_adder")
logger.info("Optimization complete")
logger.warning("Coverage below target")
logger.error("Failed to load file")
```

### **Example Log Output**
```
2026-04-19 14:23:45 INFO     Starting optimization...
2026-04-19 14:23:45 DEBUG    Loading config from dataset_config.yaml
2026-04-19 14:23:45 DEBUG    Processing module: half_adder
2026-04-19 14:23:46 DEBUG    Loaded 1000 tests, calculated scores
2026-04-19 14:23:46 DEBUG    Selected 20 tests (98% reduction)
2026-04-19 14:23:47 INFO     Optimization complete
2026-04-19 14:23:47 INFO     Results saved to optimized_testcases/
```

---

## **Validation**

### **Check Configuration**
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('dataset_config.yaml'))"

# If no error → Config is valid ✅
# If error → Fix syntax issues ⚠️
```

### **Verify Paths**
```bash
# Check if all files in config exist
python3 << 'EOF'
import yaml
from pathlib import Path

with open('dataset_config.yaml') as f:
    config = yaml.safe_load(f)

for name, settings in config['modules'].items():
    if not settings['enabled']:
        print(f"⏭️  {name} (disabled)")
        continue
    
    path = Path(settings['input_path'])
    if path.exists():
        print(f"✅ {name}: {path}")
    else:
        print(f"❌ {name}: NOT FOUND - {path}")
EOF
```

---

## **Common Configuration Issues**

### **Issue 1: File Not Found** ❌
```yaml
# Wrong
input_path: "half_adder_dataset.csv"  # File not in project root

# Correct
input_path: "19 aprilt/half_adder_dataset.csv"
```

### **Issue 2: YAML Syntax Error** ❌
```yaml
# Wrong (indentation)
half_adder:
input_path: "file.csv"  # Should be indented!

# Correct
half_adder:
  input_path: "file.csv"
```

### **Issue 3: Disabled Module** ❌
```yaml
# This module won't be processed
register_counter:
  enabled: false  # Skipped by pipeline

# To enable it
register_counter:
  enabled: true
```

### **Issue 4: Wrong Data Format** ❌
```yaml
# Path points to Excel file (not CSV)
input_path: "data.xlsx"  # Won't work!

# Convert to CSV first or point to correct file
input_path: "data.csv"
```

---

## **Configuration Checklist**

Before running the pipeline:

```
✅ dataset_config.yaml exists
✅ All modules have enabled: true/false
✅ All enabled modules have valid input_path
✅ All input_path files exist
✅ No YAML syntax errors (brackets, colons, indentation)
✅ config.py has desired settings
✅ requirements.txt dependencies installed
✅ .env file has API keys (if needed)
✅ Output folders can be created
✅ Sufficient disk space for outputs
```

---

## **Quick Config Templates**

### **Template 1: Minimal (1 module)**
```yaml
modules:
  half_adder:
    enabled: true
    input_path: "19 aprilt/half_adder_dataset.csv"
```

### **Template 2: Full (all modules)**
```yaml
modules:
  half_adder:
    enabled: true
    input_path: "19 aprilt/half_adder_dataset.csv"
  t_flip_flop:
    enabled: true
    input_path: "19 aprilt/t_ff_dataset.csv"
  # ... all 8 modules
```

### **Template 3: Mixed (enabled + disabled)**
```yaml
modules:
  half_adder:
    enabled: true
    input_path: "..."
  register_counter:
    enabled: false  # Skip this one
    input_path: "..."
```

---

## **Next Steps**

**Configure Your System**:
1. ✅ Edit `dataset_config.yaml` with your module paths
2. ✅ Customize `config.py` for your optimization preferences
3. ✅ Verify all paths exist
4. ✅ Run pipeline: `python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py`
5. ✅ Use outputs!

**Next**: Go to [07_DATA_FLOW_GUIDE.md](07_DATA_FLOW_GUIDE.md)
- See complete end-to-end flow
- Understand data transformations
- Troubleshoot issues

---

**Configuration is the first step to customizing the system for your needs!** ⚙️


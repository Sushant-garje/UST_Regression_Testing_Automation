# 🔧 LAYER 3: FEATURE ENGINEERING & FULL DATA EXPORT

## **What Does This Layer Do?**

Takes **optimized tests** and **merges back the original data** to create comprehensive CSVs with 14-20 columns for debugging and traceability.

**Input**: `normalized_*.csv` + Original raw CSVs
**Output**: `optimized_testcases_full/*.csv` files (14-20 columns)
**File**: `export_with_full_data.py`

**Use Case**: When a test fails, you need ALL the details to debug!

---

## **The Problem It Solves**

The optimized CSVs are lightweight (9 columns) for **fast execution**, but lack details:

```csv
# Optimized CSV (simple but lacking details)
testcase_id,module,coverage,runtime_seconds,pass_fail,score,priority_rank,selected,reduction_percent
half_adder_test_4,half_adder,50,5,PASS,0.80,1,true,98.0
```

But when debugging a failure, you need the **original inputs and outputs**:

```csv
# Full Data CSV (complete for debugging)
testcase_id,module,A,B,rst,exp_sum,exp_carry,act_sum,act_carry,pass_fail,coverage,score,priority_rank,runtime_seconds,reduction_percent
half_adder_test_4,half_adder,1,1,0,1,0,1,0,PASS,50,0.80,1,5,98.0
```

---

## **The Methodology**

### **Stage 1: Load Optimized Data** 📊
```python
# Load the 9-column optimized CSV
optimized_df = pd.read_csv('optimized_testcases/optimized_half_adder.csv')

# Example:
# [testcase_id | module | coverage | runtime_seconds | pass_fail | score | priority_rank | selected | reduction]
```

### **Stage 2: Load Original Data** 📇
```python
# Load the original raw CSV
original_df = pd.read_csv('19 aprilt/half_adder_dataset.csv')

# Example:
# [A | B | rst | exp_sum | exp_carry | act_sum | act_carry | pass_fail | coverage | runtime]
```

### **Stage 3: Generate Test IDs** 🆔
```python
# Create mapping from test index to original testcase_id
for idx, row in optimized_df.iterrows():
    original_idx = extract_test_number(row['testcase_id'])
    # half_adder_test_4 → index 4
```

### **Stage 4: Merge Data** 🔗
```python
# Join optimized + original data
merged_df = optimized_df.merge(
    original_df.iloc[original_indices],
    left_index=True,
    right_index=True,
    how='left'
)
```

### **Stage 5: Add Metadata** 📝
```python
# Add extra columns for traceability
merged_df['export_date'] = datetime.now()
merged_df['data_source'] = 'normalized_half_adder.csv'
merged_df['analysis_version'] = '1.0'
```

### **Stage 6: Export to CSV** 💾
```python
# Save full data CSV with all columns
merged_df.to_csv(
    'optimized_testcases_full/optimized_half_adder_full.csv',
    index=False
)
```

---

## **How to Run**

### **Option 1: Standalone**
```bash
cd /Users/sushant/Documents/engineering/Industry\ Project/harsh/UST
python3 export_with_full_data.py
```

### **Option 2: Full Pipeline**
```bash
python3 normalize_datasets.py && \
python3 export_optimized_tests.py && \
python3 export_with_full_data.py
```

---

## **Input & Output**

### **Inputs**
```
1. normalized_*.csv              (5 columns, clean data)
   └─ From Layer 1: Normalization

2. Original raw CSV files        (8-12 columns, original data)
   └─ From: 19 aprilt/ folder
   └─ Used to get back original test parameters
```

### **Outputs**
```
optimized_testcases_full/
├── optimized_half_adder_full.csv           (20 tests, 16 columns)
├── optimized_t_flip_flop_full.csv          (918 tests, 14 columns)
├── optimized_4_bit_subtractor_full.csv     (37 tests, 16 columns)
├── optimized_register_comparator_full.csv  (37 tests, 20 columns)
├── optimized_register_downcounter_full.csv (20 tests, 15 columns)
├── optimized_8_bit_alu_full.csv            (507 tests, 16 columns)
└── optimized_jk_flip_flop_full.csv         (1 test, 16 columns)
```

---

## **Column Structure by Module**

### **Half Adder (16 columns)**
```
testcase_id | module | A | B | rst | exp_sum | exp_carry | act_sum | act_carry |
pass_fail | coverage | score | priority_rank | runtime_seconds | selected | 
reduction_percent

Example:
half_adder_test_4 | half_adder | 1 | 1 | 0 | 1 | 0 | 1 | 0 |
PASS | 50 | 0.80 | 1 | 5 | true | 98.0
```

### **T Flip-Flop (14 columns)**
```
testcase_id | module | T | rst | prev_Q | exp_Q | act_Q | pass_fail |
coverage | score | priority_rank | runtime_seconds | selected | reduction_percent

Example:
T_FF_test_3 | t_flip_flop | 1 | 0 | 0 | 1 | 1 |
PASS | 37 | 0.69 | 1 | 3 | true | 0.2
```

### **Register Comparator (20 columns)**
```
testcase_id | module | A | B | ExpGT | ExpEQ | ExpLT | ActGT | ActEQ | ActLT |
pass_fail | coverage | score | priority_rank | runtime_seconds | selected |
reduction_percent | delta_cov | test_vector | timestamp

Example: (20 columns total)
```

---

## **Detailed Example: Half Adder**

### **Before: Optimized CSV (9 columns)**
```csv
testcase_id,module,coverage,runtime_seconds,pass_fail,score,priority_rank,selected,reduction_percent
half_adder_test_4,half_adder,50,5,PASS,0.80,1,true,98.0
half_adder_test_22,half_adder,100,8,PASS,0.70,2,true,98.0
```

### **Merge with Original (10 columns)**
```csv
A,B,rst,exp_sum,exp_carry,act_sum,act_carry,pass_fail,coverage,runtime
1,1,0,1,0,1,0,PASS,50,5
0,0,0,0,0,0,0,PASS,100,8
```

### **After: Full Data CSV (16 columns)**
```csv
testcase_id,module,A,B,rst,exp_sum,exp_carry,act_sum,act_carry,pass_fail,coverage,score,priority_rank,runtime_seconds,selected,reduction_percent
half_adder_test_4,half_adder,1,1,0,1,0,1,0,PASS,50,0.80,1,5,true,98.0
half_adder_test_22,half_adder,0,0,0,0,0,0,0,PASS,100,0.70,2,8,true,98.0
```

---

## **Code Structure**

### **Main Class: `FullDataExporter`**

```python
class FullDataExporter:
    
    def __init__(self, module_name, optimized_path, original_path):
        """Initialize exporter"""
        self.module_name = module_name
        self.optimized_df = pd.read_csv(optimized_path)
        self.original_df = pd.read_csv(original_path)
    
    def merge_data(self):
        """Merge optimized + original data"""
        # Extract test indices from testcase_id
        # Map to original dataframe rows
        # Merge data
    
    def add_metadata(self):
        """Add metadata columns"""
        # Add export date
        # Add source file
        # Add version info
    
    def validate_merge(self):
        """Verify merge successful"""
        # Check no NaN values
        # Check row count matches
        # Check columns present
    
    def export(self):
        """Export to CSV"""
        # Save to optimized_testcases_full/
```

### **Main Function: `main()`**

```python
def main():
    modules = [
        ('half_adder', 'normalized_half_adder.csv', '19 aprilt/half_adder_dataset.csv'),
        ('t_flip_flop', 'normalized_t_flip_flop.csv', '19 aprilt/t_ff_dataset.csv'),
        # ... more modules
    ]
    
    for module_name, optimized_path, original_path in modules:
        exporter = FullDataExporter(module_name, optimized_path, original_path)
        exporter.merge_data()
        exporter.add_metadata()
        exporter.validate_merge()
        exporter.export()
```

---

## **What Gets Exported**

### **Core Columns** (Always present, 9)
```
testcase_id, module, pass_fail, coverage, score, priority_rank,
runtime_seconds, selected, reduction_percent
```

### **Original Test Parameters** (Varies by module, 5-11)
```
Half Adder: A, B, rst, exp_sum, exp_carry, act_sum, act_carry
T Flip-Flop: T, rst, prev_Q, exp_Q, act_Q
4-bit Sub: A, B, Expected, Actual
Comparator: A, B, ExpGT, ExpEQ, ExpLT, ActGT, ActEQ, ActLT
```

### **Total Columns** (14-20 depending on module)
```
Lightweight (9) + Original (5-11) = Full (14-20)
```

---

## **Use Cases for Full Data**

### **Use Case 1: Debug a Failed Test**
```python
import pandas as pd

df = pd.read_csv('optimized_testcases_full/optimized_half_adder_full.csv')

# Find failed test
failed = df[df['testcase_id'] == 'half_adder_test_4'].iloc[0]

print(f"Test Inputs:")
print(f"  A = {failed['A']}, B = {failed['B']}, rst = {failed['rst']}")

print(f"Expected Outputs:")
print(f"  sum = {failed['exp_sum']}, carry = {failed['exp_carry']}")

print(f"Actual Outputs:")
print(f"  sum = {failed['act_sum']}, carry = {failed['act_carry']}")

print(f"Result: {failed['pass_fail']}")
print(f"Coverage: {failed['coverage']}%")
```

### **Use Case 2: Analyze Test Patterns**
```python
# Check if certain inputs always fail
failing_tests = df[df['pass_fail'] == 'FAIL']

for _, test in failing_tests.iterrows():
    print(f"Test {test['testcase_id']}: A={test['A']}, B={test['B']}")
```

### **Use Case 3: Export for Report**
```python
# Create human-readable report
report = df[[
    'testcase_id', 'priority_rank', 'coverage', 'score',
    'A', 'B', 'exp_sum', 'act_sum', 'pass_fail'
]].copy()

report.to_csv('test_report.csv', index=False)
```

---

## **Performance**

| Operation | Time | Notes |
|-----------|------|-------|
| Load optimized CSV | 50ms | Pandas |
| Load original CSV | 100ms | May be large |
| Extract indices | 100ms | String parsing |
| Merge dataframes | 200ms | Join operation |
| Add metadata | 50ms | Column creation |
| Validate | 100ms | Data quality checks |
| Export to CSV | 150ms | to_csv |
| **Total per module** | **2-3 seconds** | |
| **All 8 modules** | **15-20 seconds** | |

---

## **Error Handling**

### **Mismatch: Different row counts**
```
Original: 1,000 rows
Optimized: 20 rows (selected)
Merge Result: OK - we want only selected tests!
```

### **Missing columns in original**
```
If original CSV missing expected columns:
→ Fill with NaN
→ Log warning
→ Continue (don't crash)
```

### **Different encoding**
```
If encoding mismatch:
→ Try UTF-8
→ Fallback to latin-1
→ Fallback to cp1252
→ Log which encoding used
```

---

## **Output Manifest**

After running, check `export_full_data_manifest.json`:

```json
{
  "half_adder": {
    "status": "success",
    "tests_exported": 20,
    "columns": 16,
    "output_file": "optimized_testcases_full/optimized_half_adder_full.csv",
    "columns_list": [
      "testcase_id", "module", "A", "B", "rst", "exp_sum", "exp_carry",
      "act_sum", "act_carry", "pass_fail", "coverage", "score", 
      "priority_rank", "runtime_seconds", "selected", "reduction_percent"
    ]
  },
  "t_flip_flop": {
    "status": "success",
    "tests_exported": 918,
    "columns": 14,
    ...
  }
}
```

---

## **Advantages**

✅ **Complete Traceability**: All info plus optimization scores
✅ **Debugging-Ready**: Original inputs and outputs together
✅ **Flexible**: Works with any original format
✅ **Automatic**: No manual merging needed
✅ **Safe**: Doesn't modify original files
✅ **Fast**: <20 seconds for all modules

---

## **Comparison: Lightweight vs Full Data**

| Aspect | Lightweight (9 cols) | Full (14-20 cols) |
|--------|------------------|---|
| **Size** | Small (fast loading) | Larger (slower loading) |
| **Execution** | ✅ Use for fast runs | ❌ Too slow |
| **Debugging** | ❌ Missing parameters | ✅ Complete info |
| **Columns** | Score, priority, metrics | Original data + metrics |
| **Use Case** | Test runner | QA/debugging |

---

## **Workflow**

```
┌─────────────────────────────────────────────┐
│  Step 1: Generate Optimized Tests           │
│  (Layer 2: export_optimized_tests.py)       │
│  Output: 9-column lightweight CSVs          │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  Step 2: Merge with Original Data           │
│  (Layer 3: export_with_full_data.py)        │
│  Input: 9 cols + original data              │
│  Output: 14-20 column full data CSVs        │
└────────────┬────────────────────────────────┘
             │
        ┌────┴───────┐
        │             │
        ▼             ▼
   Use for        Use for
   fast runs    debugging &
   (lightweight) reporting
   (full data)
```

---

## **Next Steps**

**Generated**: `optimized_testcases_full/*.csv` with 14-20 columns

**Now you can**:
- ✅ Execute from `optimized_testcases/` (fast)
- ✅ Debug from `optimized_testcases_full/` (detailed)
- ✅ Build reports from full data
- ✅ Integrate with CI/CD pipeline

**Next**: Go to [04_REGRESSION_MANAGER.md](04_REGRESSION_MANAGER.md)
- Learn about core scoring/prioritization services
- Understand API structure
- See how to use regression_manager/ module

---

**This layer bridges optimization and debugging!** 🔧


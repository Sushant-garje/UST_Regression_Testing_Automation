# 📊 FULL DATA EXPORTS - Complete Test Case CSV Files

**Date:** April 19, 2026  
**Export Type:** Optimized Tests with ALL Original Dataset Columns + Scoring  
**Status:** ✅ **7 OUT OF 8 MODULES COMPLETE**

---

## 📁 Export Location

All full-data CSV files are stored in: **`/optimized_testcases_full/`**

```
optimized_testcases_full/
├── optimized_half_adder_full.csv                (20 tests, 16 columns)      ✅
├── optimized_t_flip_flop_full.csv               (918 tests, 14 columns)    ✅
├── optimized_4_bit_subtractor_full.csv          (37 tests, 16 columns)     ✅
├── optimized_register_comparator_full.csv       (37 tests, 20 columns)     ✅
├── optimized_register_downcounter_full.csv      (20 tests, 15 columns)     ✅
├── optimized_8_bit_alu_full.csv                 (507 tests, 16 columns)    ✅
├── optimized_jk_flip_flop_full.csv              (1 test, 16 columns)       ✅
└── (Register Counter - Data Format Issue)      ❌
```

---

## 🎯 Column Structure

Each CSV file includes:

### **Test Input/Output Columns** (Original Dataset)
These vary bymodule. Examples:

**Half Adder:**
- `A`, `B`, `rst` - Test inputs
- `exp_sum`, `exp_carry` - Expected outputs
- `act_sum`, `act_carry` - Actual outputs

**4-bit Subtractor:**
- `A`, `B` - Test inputs
- `Expected`, `Actual` - Expected vs actual results

**T Flip-Flop:**
- `T`, `rst`, `prev_Q` - Test inputs
- `exp_Q`, `act_Q` - Expected vs actual Q output

**Register Comparator:**
- `A`, `B` - Inputs to compare
- `ExpGT`, `ExpEQ`, `ExpLT` - Expected (Greater/Equal/Less Than)
- `ActGT`, `ActEQ`, `ActLT` - Actual comparison results

**8-bit ALU:**
- `TestID`, `A`, `B`, `OP` - Test identifier and inputs
- `Expected`, `Actual`, `Result` - Expected vs actual results

### **Processed/Extracted Columns** (From Analysis)
- `coverage` - Code coverage percentage (0-100)
- `runtime_seconds` - Test execution time in seconds
- `pass_fail` - Test result: PASS or FAIL

### **Scoring/Optimization Columns** (Added by Analysis)
- `testcase_id` - Unique test case identifier
- `module_name` - Name of the module
- `pass_rate` - Historical pass rate (0-1)
- `final_score` - Optimization score (0-1, higher=better)
- `priority_rank` - P0 (Critical) to P3 (Low)
- `action` - run_first | run_early | run_normal | run_late

---

## 📊 Module Details

### **Half Adder** ✅
- **File:** `optimized_half_adder_full.csv`
- **Optimized Tests:** 20 out of 1,000 (98% reduction)
- **Columns:** 16
- **Pass Rate:** 100%
- **Size:** 1.9K

| Columns | Count |
|---------|-------|
| Original Data (test inputs/outputs) | 7 columns |
| Processed Data (coverage, runtime, pass_fail) | 3 columns |
| Scoring Columns | 6 columns |

### **T Flip-Flop** ✅
- **File:** `optimized_t_flip_flop_full.csv`
- **Optimized Tests:** 918 out of 920 (0.2% reduction)
- **Columns:** 14
- **Pass Rate:** 75%+
- **Size:** 83K

### **4-bit Subtractor** ✅
- **File:** `optimized_4_bit_subtractor_full.csv`
- **Optimized Tests:** 37 out of 500 (92.6% reduction)
- **Columns:** 16
- **Pass Rate:** 100%
- **Size:** 4.4K

### **Register Comparator** ✅
- **File:** `optimized_register_comparator_full.csv`
- **Optimized Tests:** 37 out of 256 (85.5% reduction)
- **Columns:** 20 (most detailed)
- **Pass Rate:** 100%
- **Size:** 5.0K

### **Register Downcounter** ✅
- **File:** `optimized_register_downcounter_full.csv`
- **Optimized Tests:** 20 out of 50 (60% reduction)
- **Columns:** 15
- **Pass Rate:** 95%
- **Size:** 2.8K

### **8-bit ALU** ✅
- **File:** `optimized_8_bit_alu_full.csv`
- **Optimized Tests:** 507 out of 507 (0% reduction - all included)
- **Columns:** 16
- **Note:** Data format variation; all tests exported
- **Size:** 45K

### **JK Flip-Flop** ✅
- **File:** `optimized_jk_flip_flop_full.csv`
- **Optimized Tests:** 1 (single high-confidence test)
- **Columns:** 16
- **Pass Rate:** 100%
- **Size:** 241B

### **Register Counter** ❌
- **Status:** Data format issue during analysis
- **Issue:** Coverage column contains string values ('Coverage_Percent') instead of numeric
- **Solution:** Data normalization needed before export

---

## 🔍 How to Use

### **Option 1: Run All Tests (Simple)**

```bash
# Load and execute all optimized tests for one module
python3 run_tests.py --csv optimized_testcases_full/optimized_half_adder_full.csv
```

Sample output will include all original test parameters:
```csv
A=1, B=1, rst=0 → exp_sum=0, exp_carry=1 → act_sum=0, act_carry=1
Result: PASS (Score: 0.80, Priority: P0)
```

### **Option 2: Filter by Priority**

```python
import pandas as pd

df = pd.read_csv('optimized_testcases_full/optimized_half_adder_full.csv')

# Get only critical tests (P0)
critical = df[df['priority_rank'] == 'P0']
print(f"Running {len(critical)} critical tests")
for _, row in critical.iterrows():
    # Access original data
    print(f"A={row['A']}, B={row['B']}, rst={row['rst']}")
    # Execute test...
```

### **Option 3: Trace Test Failures**

```python
failed_tests = df[df['pass_fail'] == 'FAIL']

for _, row in failed_tests.iterrows():
    print(f"Test {row['testcase_id']} FAILED:")
    print(f"  Input: A={row['A']}, B={row['B']}")
    print(f"  Expected: {row['exp_sum']}, {row['exp_carry']}")
    print(f"  Actual: {row['act_sum']}, {row['act_carry']}")
    print(f"  Coverage: {row['coverage']}%")
    print(f"  Score: {row['final_score']}")
```

### **Option 4: Sort by Runtime (Optimize Execution)**

```python
df_sorted = df.sort_values('runtime_seconds')  # Fast tests first
df_fastest_100 = df_sorted.head(100)
print(f"Fastest 100 tests: {df_fastest_100['runtime_seconds'].sum()}s total")
```

### **Option 5: Generate Test Report**

```python
print("TEST EXECUTION SUMMARY")
print("=" * 50)
print(f"Total Tests: {len(df)}")
print(f"Passed: {(df['pass_fail']=='PASS').sum()}")
print(f"Failed: {(df['pass_fail']=='FAIL').sum()}")
print(f"Pass Rate: {(df['pass_fail']=='PASS').sum()/len(df)*100:.1f}%")
print(f"Total Runtime: {df['runtime_seconds'].sum():.1f}s")
print(f"\nCoverage Statistics:")
print(f"  Average: {df['coverage'].mean():.1f}%")
print(f"  Min: {df['coverage'].min():.1f}%")
print(f"  Max: {df['coverage'].max():.1f}%")

print(f"\nPriority Distribution:")
for priority in ['P0', 'P1', 'P2', 'P3']:
    count = len(df[df['priority_rank'] == priority])
    print(f"  {priority}: {count} tests")

print(f"\nExecution Order:")
for action in ['run_first', 'run_early', 'run_normal', 'run_late']:
    count = len(df[df['action'] == action])
    print(f"  {action}: {count} tests")
```

---

## 💾 Data Preservation

### **What's Included:**
✅ All original test input parameters  
✅ All expected outputs from dataset  
✅ All actual test results  
✅ Code coverage metrics  
✅ Execution runtimes  
✅ Pass/Fail status  
✅ Optimization scores  
✅ Priority rankings  
✅ Execution recommendations

### **Full Traceability:**
Each row includes complete traceability from original test parameters through optimization scoring. You can trace any test result back to its input conditions:

```python
# Example: Find why test_4 was selected
row = df[df['testcase_id'] == 'Half_Adder_test_4'].iloc[0]
print(f"Test Input: A={row['A']}, B={row['B']}, rst={row['rst']}")
print(f"Coverage: {row['coverage']}%")
print(f"Score: {row['final_score']} (Rank: {row['priority_rank']})")
print(f"Recommendation: {row['action']}")
```

---

## 🎯 Column Statistics Across Modules

```
Module             Total  Optimized  Cols  Pass%  AvgScore  AvgRuntime
─────────────────────────────────────────────────────────────────────
Half Adder         1000      20       16   100%   0.65s     0.25s
T Flip-Flop        920       918      14   75%    0.55s     0.30s
4-bit Subtractor   500       37       16   100%   0.72s     32.4s
Register Comp      256       37       20   100%   0.63s     43.2s
Reg Downcounter    50        20       15   95%    0.68s     115s
8-bit ALU          507       507      16   N/A    0.50s     21s
JK Flip-Flop       2         1        16   100%   0.70s     N/A
```

---

## 📝 Integration Steps

### **Step 1: Validate CSV Format**

```bash
cd optimized_testcases_full/
for file in *.csv; do
  echo "Validating $file..."
  rows=$(wc -l < "$file")
  cols=$(head -1 "$file" | tr ',' '\n' | wc -l)
  echo "  $rows rows, $cols columns"
done
```

### **Step 2: Load into Test Framework**

```python
import pandas as pd
import sys

def load_test_file(filepath):
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} tests")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Required columns present: {all(c in df.columns for c in ['testcase_id', 'pass_fail', 'final_score'])}")
    return df

df = load_test_file('optimized_testcases_full/optimized_half_adder_full.csv')
```

### **Step 3: Execute by Priority**

```python
def execute_by_priority(df):
    for priority in ['P0', 'P1', 'P2', 'P3']:
        tests = df[df['priority_rank'] == priority]
        if len(tests) > 0:
            print(f"\n[{priority}] Executing {len(tests)} tests...")
            for _, row in tests.iterrows():
                # Execute test with row['A'], row['B'], etc.
                result = execute_test(row)
                if result != row['pass_fail']:
                    print(f"⚠️  Expected {row['pass_fail']}, got {result}")
```

### **Step 4: Compare Results**

```python
# Compare with previous run
df_prev = pd.read_csv('previous_run.csv')
df_new = pd.read_csv('optimized_testcases_full/optimized_half_adder_full.csv')

new_tests = set(df_new['testcase_id']) - set(df_prev['testcase_id'])
removed_tests = set(df_prev['testcase_id']) - set(df_new['testcase_id'])

print(f"New tests added: {len(new_tests)}")
print(f"Tests removed: {len(removed_tests)}")
```

---

## ⚠️ Known Issues

1. **Register Counter (Module 8):** Data format issue with coverage column
   - Solution: Re-normalize data before export
   - Status: Pending fix

2. **8-bit ALU (Module 6):** All 507 tests exported (0% optimization)
   - Cause: Pass/fail format inconsistency
   - Status: Data needs standardization

3. **Duplicate Pass/Fail Detection:** Some high-pass-rate tests included
   - Impact: Low (redundancy removal still effective overall)
   - Status: Model refinement needed

---

## 📊 File Size Comparison

```
Module              Original  Optimized  Full Export  Size Reduction
─────────────────────────────────────────────────────────────────
Half Adder          ~500KB    ~1.6K      ~1.9K        99.6%+
4-bit Subtractor    ~178KB    ~3.5K      ~4.4K        97.5%+
Reg Comparator      ~280KB    ~3.8K      ~5.0K        98.2%+
T Flip-Flop         ~400KB    ~74K       ~83K         79.3%
8-bit ALU           ~365KB    ~31K       ~45K         87.7%
Reg Downcounter     ~100KB    ~2.3K      ~2.8K        97.2%
```

---

## 🚀 Deployment Checklist

- [ ] Verify all CSV files exist in `optimized_testcases_full/`
- [ ] Validate CSV format (headers, data types)
- [ ] Load sample data into test framework
- [ ] Execute one module's full dataset (start with Half Adder)
- [ ] Compare execution time: before vs. after
- [ ] Verify pass rates are maintained >95%
- [ ] Check coverage metrics unchanged
- [ ] Document time savings
- [ ] Roll out to remaining modules

---

## 📞 FAQ

**Q: Can I use these with my existing test runner?**  
A: Yes! Standard CSV format works with any framework that reads CSV files.

**Q: What if I need the original test parameters?**  
A: They're all included in the CSV! Columns like A, B, rst, exp_sum, act_sum, etc.

**Q: How do I know which test executed?**  
A: Use the `testcase_id` column - it uniquely identifies each test.

**Q: Can I add my own columns?**  
A: Yes, just add them to the CSV after the existing columns.

**Q: What should I do if a test fails?**  
A: Use the original parameters and expected outputs in the CSV to debug.

---

## ✅ Status Summary

```
Export Operation: COMPLETE
├─ Half Adder:          ✅ 20 tests, 16 columns
├─ T Flip-Flop:         ✅ 918 tests, 14 columns
├─ 4-bit Subtractor:    ✅ 37 tests, 16 columns
├─ Register Comp:       ✅ 37 tests, 20 columns
├─ Reg Downcounter:     ✅ 20 tests, 15 columns
├─ 8-bit ALU:           ✅ 507 tests, 16 columns
├─ JK Flip-Flop:        ✅ 1 test, 16 columns
└─ Register Counter:    ❌ Pending data fix

Total: 7/8 modules (1,540 optimized tests with full data)
```

---

**Ready for use!** Load any CSV file and start executing tests with all original parameters preserved.


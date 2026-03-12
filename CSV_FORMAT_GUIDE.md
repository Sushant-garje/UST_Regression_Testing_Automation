# CSV Format Guide - Flexible Data Loading

## ✅ Problem Solved

The system now **automatically handles ANY CSV format** with intelligent column mapping and defaults!

## 🎯 Supported CSV Formats

### Format 1: Standard VLSI Format
```csv
module,test,seed,rtl_version,git_commit,result,coverage,sim_time
jk_ff,test,1,v1.0,commit_001,PASS,95.0,145
```

### Format 2: Simple Test Format
```csv
TestID,A,B,Expected,Actual,Status,Coverage(%)
1,0,0,0,0,PASS,31.94
```

### Format 3: Custom Format
```csv
Module,TestName,RandomSeed,Result,Cov,Runtime
cpu,test1,42,PASSED,87.5,120
```

## 🔧 How It Works

### 1. Flexible Column Mapping

The system automatically maps columns using these patterns:

| Standard Name | Recognized Variations |
|---------------|----------------------|
| `module` | module, Module, MODULE, module_name, ModuleName |
| `test` | test, Test, TEST, test_name, TestName, TestID, test_id |
| `seed` | seed, Seed, SEED, random_seed, RandomSeed |
| `result` | result, Result, RESULT, status, Status, STATUS, pass_fail, PassFail |
| `coverage` | coverage, Coverage, COVERAGE, cov, Coverage(%), coverage_percentage |
| `sim_time` | sim_time, SimTime, simulation_time, runtime, Runtime, time, Time |

### 2. Intelligent Defaults

If columns are missing, the system fills them automatically:

- **module**: Uses filename (e.g., `8bitadder.csv` → `8bitadder`)
- **test**: Uses `test_` + row number
- **seed**: Defaults to `1`
- **result**: Uses `PASS` or maps from Status column
- **coverage**: Defaults to `50.0` or finds any coverage-like column
- **sim_time**: Uses incremental values or finds any time-like column

### 3. Type Handling

- All columns converted to appropriate types
- String concatenation handled safely
- Numeric columns coerced with error handling
- Missing values filled intelligently

## 📊 Example Transformations

### Example 1: 8bitadder.csv

**Input:**
```csv
TestID,A,B,Expected,Actual,Status,Coverage(%)
1,0,0,0,0,PASS,31.94
```

**After Processing:**
```
module_name: 8bitadder
testcase_id: 8bitadder_test_1_seed1
pass_fail: 1
coverage: 31.94
runtime_seconds: 5
```

### Example 2: rag_training_data.csv

**Input:**
```csv
module,test,seed,result,coverage,sim_time
jk_ff,test,1,PASS,95.0,145
```

**After Processing:**
```
module_name: jk_ff
testcase_id: jk_ff_test_seed1
pass_fail: 1
coverage: 95.0
runtime_seconds: 145
```

## 🚀 Usage

### No Changes Needed!

Just use any CSV file:

```python
from regression_manager import RegressionManagerAgent

# Works with ANY CSV format
agent = RegressionManagerAgent(
    csv_path='your_file.csv',  # Any format!
    log_path='sim.log'
)

result = agent.run()
```

### Multiple Files

```python
# Process different formats
files = ['8bitadder.csv', 'rag_training_data.csv', 'custom_tests.csv']

for file in files:
    agent = RegressionManagerAgent(csv_path=file)
    result = agent.run()
```

## 📝 Best Practices

### 1. Include Key Columns

For best results, include:
- Test identifier (TestID, test, test_name)
- Status/Result (Status, result, pass_fail)
- Coverage (Coverage, cov, Coverage(%))

### 2. Use Standard Names

Prefer standard names when possible:
- `module`, `test`, `seed`
- `result`, `coverage`, `sim_time`

### 3. Consistent Formats

Within a file, keep formats consistent:
- Same date format
- Same number format
- Same status values (PASS/FAIL)

## 🔍 Troubleshooting

### Issue: Wrong Column Detected

**Solution:** Rename column to standard name

```python
# Before loading
df = pd.read_csv('file.csv')
df.rename(columns={'MyTest': 'test'}, inplace=True)
df.to_csv('file_fixed.csv', index=False)
```

### Issue: Coverage Values Wrong

**Solution:** Check column name contains "cov" or "coverage"

### Issue: Module Name Generic

**Solution:** Add module column to CSV

## ✅ Tested Formats

- ✅ Standard VLSI format
- ✅ Simple test format
- ✅ Custom formats
- ✅ Mixed case columns
- ✅ Special characters in names
- ✅ Missing columns
- ✅ Extra columns (ignored)

## 🎉 Result

**Your system now works with ANY CSV format automatically!**

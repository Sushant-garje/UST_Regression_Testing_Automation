# 🎯 HOW TO UPDATE DATASETS - STEP BY STEP

## **The 3-Minute Workflow**

### **When You Get New Data:**

**Step 1: Edit the config file**
```bash
# Open this file in your editor:
open dataset_config.yaml
```

**Step 2: Update one or more paths**

Example - updating Half Adder with new data:
```yaml
# BEFORE:
half_adder:
  enabled: true
  input_path: "half_adder_dataset.csv"

# AFTER (new data from Downloads):
half_adder:
  enabled: true
  input_path: "/Users/sushant/Downloads/new_half_adder_test_suite.csv"
```

Example - updating multiple modules:
```yaml
half_adder:
  input_path: "/Users/sushant/Downloads/April2026/half_adder.csv"

4bit_sub:
  input_path: "/Users/sushant/Downloads/April2026/4bit_sub.csv"

t_flip_flop:
  input_path: "/Users/sushant/Downloads/April2026/t_flip_flop.csv"
```

**Step 3: Run pipeline (auto-detects from config)**
```bash
python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py
```

**Step 4: Use updated CSVs**
```bash
# Check what was generated
ls -lh optimized_testcases/
```

Done! ✅

---

## **Common Config Patterns**

### **Pattern 1: New Downloads Folder**
```yaml
# All new data in ~/Downloads/
half_adder:
  input_path: "/Users/sushant/Downloads/half_adder.csv"

t_flip_flop:
  input_path: "/Users/sushant/Downloads/t_flip_flop.csv"

4bit_sub:
  input_path: "/Users/sushant/Downloads/4bit_sub.csv"
```

### **Pattern 2: Cloud Synced Folder**
```yaml
# Data in Dropbox/OneDrive/GoogleDrive
half_adder:
  input_path: "~/Dropbox/VLSI_Testing/April2026/half_adder.csv"

t_flip_flop:
  input_path: "~/Dropbox/VLSI_Testing/April2026/t_flip_flop.csv"
```

### **Pattern 3: CI/CD Pipeline Output**
```yaml
# Results from your test pipeline in project subfolder
half_adder:
  input_path: "test_results/2026-04-19/half_adder_results.csv"

t_flip_flop:
  input_path: "test_results/2026-04-19/t_flip_flop_results.csv"
```

### **Pattern 4: Temporary Disable Module**
```yaml
# Disable Register Counter while debugging
register_counter:
  enabled: false
  # input_path doesn't matter when disabled
  input_path: "WILL_BE_IGNORED.csv"

# Everything else still processes
half_adder:
  enabled: true
  input_path: "half_adder.csv"
```

---

## **Key Features**

✅ **Supports Relative Paths**
```yaml
# Files in project folder or subfolders
input_path: "file.csv"
input_path: "subfolder/file.csv"
input_path: "19 april/results/data.csv"
```

✅ **Supports Absolute Paths**
```yaml
# Files anywhere on system
input_path: "/Users/sushant/Downloads/data.csv"
input_path: "/Volumes/ExternalDrive/tests.csv"
```

✅ **Supports Home Directory (~)**
```yaml
# User home shortcuts
input_path: "~/Downloads/data.csv"
input_path: "~/Dropbox/data.csv"
```

✅ **Auto-Detects CSV Format**
```yaml
# These can be:
# - Semicolon separated (Europe format)
# - Comma separated (US format)
# - Tab separated
# - Any combination
# Script handles it all automatically!

input_path: "/Users/sushant/Downloads/data.csv"
```

✅ **Skip Disabled Modules**
```yaml
# Set enabled: false to skip module entirely
# Useful when fixing data or testing subsets

register_counter:
  enabled: false  # Won't be processed
```

---

## **Step-by-Step Example**

**Scenario: You got new test data as email attachments**

### Before:
```bash
ls ~/Downloads/
# Sees: new_half_adder.xlsx  new_4bit_sub.csv  new_t_flip_flop.csv
```

### Step 1: Convert Excel to CSV (if needed)
```bash
# Using your spreadsheet app or online tool
# Create files in CSV format
```

### Step 2: Open config
```bash
cd /Users/sushant/Documents/engineering/Industry\ Project/harsh/UST
open dataset_config.yaml
```

### Step 3: Update paths
```yaml
half_adder:
  enabled: true
  input_path: "/Users/sushant/Downloads/new_half_adder.csv"

4bit_sub:
  enabled: true
  input_path: "/Users/sushant/Downloads/new_4bit_sub.csv"

t_flip_flop:
  enabled: true
  input_path: "/Users/sushant/Downloads/new_t_flip_flop.csv"

# Leave others unchanged:
register_comparator:
  enabled: true
  input_path: "reg_comparator_logs_makefile_result/results/comparator_combined.csv"

# (rest stays the same...)
```

### Step 4: Run full pipeline
```bash
python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py
```

### Step 5: Verify
```bash
python3 << 'EOF'
import pandas as pd
import glob

print("🎉 CHECK UPDATED RESULTS:\n")
for csv in sorted(glob.glob('optimized_testcases/optimized_*.csv')):
    df = pd.read_csv(csv)
    module = csv.split('/')[-1].replace('optimized_', '').replace('.csv', '')
    print(f"✅ {module:20} → {len(df):4} tests ready")
EOF
```

Output:
```
🎉 CHECK UPDATED RESULTS:

✅ half_adder           →  20 tests ready
✅ 4bit_sub             →  37 tests ready
✅ t_flip_flop          → 918 tests ready
✅ register_comparator  →  37 tests ready
✅ reg_downcounter      →  20 tests ready
✅ 8bit_alu             → 507 tests ready
✅ jk_flip_flop         →   1 test ready
```

---

## **Troubleshooting**

### **Q: "File not found" error**
**A:** Check the path in dataset_config.yaml:
```bash
# Verify file exists:
ls -la "/Users/sushant/Downloads/new_half_adder.csv"

# If it doesn't exist, find it:
find ~ -name "*half_adder*.csv" -type f
```

### **Q: "No numeric types to aggregate" error**
**A:** Your CSV format isn't being detected correctly. Check:
```bash
# View first 5 rows:
head -5 "/Users/sushant/Downloads/new_half_adder.csv"

# If headers look weird, try opening in Excel:
open "/Users/sushant/Downloads/new_half_adder.csv"
```

### **Q: Only some modules updated**
**A:** Some modules might still use old paths. Check enabled status:
```yaml
# Make sure enabled: true for modules you want:
half_adder:
  enabled: true  # ← This must be true

# If false, override it:
half_adder:
  enabled: true
  input_path: "..."
```

### **Q: Want to keep old data for one module, update others?**
**A:** Just leave it unchanged in config:
```yaml
# UPDATE ONLY THESE:
half_adder:
  input_path: "/Users/sushant/Downloads/new_half_adder.csv"

t_flip_flop:
  input_path: "/Users/sushant/Downloads/new_t_flip_flop.csv"

# LEAVE UNCHANGED - keeps using old paths:
4bit_sub:
  input_path: "4bit_sub_logs_makefile_results/results/results_combined.csv"

register_comparator:
  input_path: "reg_comparator_logs_makefile_result/results/comparator_combined.csv"
```

Then run pipeline - only specified modules get updated!

---

## **Pro Tips** 🚀

**Tip 1: Organize by date**
```yaml
# Comment where data came from:
half_adder:
  input_path: "/Users/sushant/Downloads/April19_2026_half_adder.csv"
  # Source: Email from test team, 2:30 PM

t_flip_flop:
  input_path: "/Users/sushant/Downloads/April19_2026_t_flip_flop.csv"
  # Source: CI/CD pipeline run #1847
```

**Tip 2: Keep backup config**
```bash
# Before making changes
cp dataset_config.yaml dataset_config.backup.yaml

# Now you can always restore:
cp dataset_config.backup.yaml dataset_config.yaml
```

**Tip 3: Test single module first**
```yaml
# Temporarily disable all but one:
half_adder:
  enabled: true    # Test this one

4bit_sub:
  enabled: false   # Disable others

t_flip_flop:
  enabled: false

# Then run: python3 normalize_datasets.py
# If it works, enable others
```

**Tip 4: Use absolute paths for cloud storage**
```yaml
# Dropbox on Mac is at:
"~/Dropbox/path/to/file.csv"

# Use full expansion to be safe:
"/Users/sushant/Dropbox/path/to/file.csv"
```

---

## **Summary**

1. **Edit** `dataset_config.yaml` with new paths
2. **Run** `python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py`
3. **Use** updated CSVs in `optimized_testcases/`

That's it! The config approach is:
- ✅ **Single source of truth** for all dataset paths
- ✅ **No code editing needed** - just config file
- ✅ **Easy to share** - send config to team
- ✅ **Easy to backup** - save old configs
- ✅ **Works offline** - no external dependencies

Now you're ready to update data quickly whenever you get new datasets! 🚀


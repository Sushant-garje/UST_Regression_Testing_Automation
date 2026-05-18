# 📌 DATASET CONFIG - QUICK REFERENCE CARD

## Copy & Paste Cheat Sheet

### **Quick One-Module Update**
```yaml
# Edit dataset_config.yaml
# Change ONLY this module path:

half_adder:
  enabled: true
  input_path: "/Users/sushant/Downloads/NEW_HALF_ADDER.csv"
```

Then run:
```bash
python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py
```

---

### **Quick Multi-Module Update**
```yaml
# Edit dataset_config.yaml
# Update multiple paths:

half_adder:
  input_path: "/Users/sushant/Downloads/new_half_adder.csv"

4bit_sub:
  input_path: "/Users/sushant/Downloads/new_4bit_sub.csv"

t_flip_flop:
  input_path: "/Users/sushant/Downloads/new_t_flip_flop.csv"

register_comparator:
  input_path: "/Users/sushant/Downloads/new_register_comp.csv"

reg_downcounter:
  input_path: "/Users/sushant/Downloads/new_reg_downcounter.csv"

8bit_alu:
  input_path: "/Users/sushant/Downloads/new_8bit_alu.csv"
```

Then run the same command.

---

### **Quick Disable Module**
```yaml
# Temporarily skip a module:

register_counter:
  enabled: false
  input_path: "IGNORED.csv"
```

---

### **Path Formats**

| Format | Example |
|--------|---------|
| **Downloads** | `/Users/sushant/Downloads/file.csv` |
| **Home** | `~/Downloads/file.csv` |
| **Relative** | `file.csv` or `subfolder/file.csv` |
| **Dropbox** | `~/Dropbox/Project/file.csv` |

---

### **After Editing Config - Command to Run**

```bash
cd /Users/sushant/Documents/engineering/Industry\ Project/harsh/UST

python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py
```

Takes 5-10 seconds. Done!

---

## **Current Module Mapping**

| Module | Current Path | Status |
|--------|--------------|--------|
| half_adder | `half_adder_dataset.csv` | ✅ Active |
| 4bit_sub | `4bit_sub_logs_makefile_results/...` | ✅ Active |
| register_comparator | `reg_comparator_logs_makefile_result/...` | ✅ Active |
| reg_downcounter | `reg_downcounter_logs_makefile_results/...` | ✅ Active |
| t_flip_flop | `t_ff_dataset.csv` | ✅ Active |
| 8bit_alu | `8bitalu_logs_makefile_res/...` | ✅ Active |
| jk_flip_flop | `jk_flip_flop_dataset.csv` | ✅ Active |
| register_counter | `reg_COUNTER_LOG_makefile_result/...` | ⏳ Disabled |

---

## **Full Config File Locations**

- **Config File:** `dataset_config.yaml`
- **View Details:** Open in any text editor
- **Edit:** Update `input_path` values only
- **No Restart:** Changes take effect immediately

---

## **Workflow in 3 Steps**

```
1️⃣  Edit dataset_config.yaml
    └─ Change input_path for one or more modules

2️⃣  Run pipeline
    └─ python3 normalize_datasets.py && \
       python3 export_optimized_tests.py && \
       python3 export_with_full_data.py

3️⃣  Use updated CSVs
    └─ optimized_testcases/optimized_*.csv
```

---

## **Verify It Worked**

```bash
# Quick check:
python3 -c "
import pandas as pd
import glob

for f in sorted(glob.glob('optimized_testcases/optimized_*.csv')):
    df = pd.read_csv(f)
    module = f.split('/')[-1].replace('optimized_', '').replace('.csv', '')
    print(f'✅ {module:20} → {len(df)} tests')
"
```

---

## **Troubleshooting**

| Issue | Fix |
|-------|-----|
| "File not found" | Check path in config exists: `ls -la /path/to/file.csv` |
| Config ignored | Make sure filename is exactly: `dataset_config.yaml` |
| Old data still there | Delete `normalized_*.csv` files, then rerun |

---

**Full guide:** [HOW_TO_UPDATE_DATASETS.md](HOW_TO_UPDATE_DATASETS.md)


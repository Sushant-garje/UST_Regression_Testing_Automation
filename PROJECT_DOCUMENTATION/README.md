# 📚 PROJECT DOCUMENTATION INDEX

Welcome to the comprehensive documentation for the **VLSI Regression Test Optimization System**!

This folder contains detailed guides for every section of the project. Start here to understand what you need.

---

## **Quick Navigation**

### **I'm New - Where Do I Start?** 🎯
Start with **[00_SYSTEM_OVERVIEW.md](00_SYSTEM_OVERVIEW.md)**
- Understand what the system does
- See the architecture
- Learn about the 4 layers
- 10 minutes read

### **I Want to Understand One Specific Layer**
Pick your layer:

| Layer | Description | File |
|-------|-------------|------|
| Layer 1 | **Data Normalization** (standardize any CSV) | [01_NORMALIZATION_LAYER.md](01_NORMALIZATION_LAYER.md) |
| Layer 2 | **Test Optimization** (score & prioritize) | [02_OPTIMIZATION_LAYER.md](02_OPTIMIZATION_LAYER.md) |
| Layer 3 | **Feature Engineering** (add debugging data) | [03_FEATURE_ENGINEERING_LAYER.md](03_FEATURE_ENGINEERING_LAYER.md) |
| Layer 4 | **Regression Manager** (core APIs) | [04_REGRESSION_MANAGER.md](04_REGRESSION_MANAGER.md) |

### **I Want to Use a Specific Component**
Pick your use case:

| Use Case | Description | File |
|----------|-------------|------|
| User Interface | Browse tests in web dashboard | [05_FRONTEND_INTEGRATION.md](05_FRONTEND_INTEGRATION.md) |
| Configuration | Set up modules & parameters | [06_CONFIGURATION_MANAGEMENT.md](06_CONFIGURATION_MANAGEMENT.md) |
| End-to-End | See how data flows through system | [07_DATA_FLOW_GUIDE.md](07_DATA_FLOW_GUIDE.md) |

---

## **Documentation Files Overview**

### **00_SYSTEM_OVERVIEW.md** 📋
**What**: The big picture
**Length**: 10 minutes
**Learn**: 
- System architecture
- 4-layer design
- Key metrics
- Current status

**Read this to**: Understand how parts fit together

---

### **01_NORMALIZATION_LAYER.md** 📥
**What**: Converting any CSV format to standard
**Length**: 15 minutes
**Learn**:
- Auto-detection mechanism
- Standardization process
- Supported formats
- Error handling

**Read this to**: Understand how different data formats are handled

---

### **02_OPTIMIZATION_LAYER.md** 🎯
**What**: Scoring and selecting best tests
**Length**: 20 minutes
**Learn**:
- Scoring methodology
- Priority assignment
- Greedy selection algorithm
- Results achieved

**Read this to**: Understand test prioritization and why 52% reduction works

---

### **03_FEATURE_ENGINEERING_LAYER.md** 🔧
**What**: Adding debugging data to optimized tests
**Length**: 15 minutes
**Learn**:
- Merging optimized + original data
- 14-20 column output format
- Debugging workflow
- Full traceability

**Read this to**: Debug failed tests with complete information

---

### **04_REGRESSION_MANAGER.md** 🛠️
**What**: Core Python module with APIs
**Length**: 20 minutes
**Learn**:
- 6 core components (Scorer, Prioritizer, etc.)
- Usage examples
- Integration patterns
- Performance benchmarks

**Read this to**: Build custom tools or CI/CD integration

---

### **05_FRONTEND_INTEGRATION.md** 🌐
**What**: Web-based dashboard for test browsing
**Length**: 15 minutes
**Learn**:
- React + Vite setup
- Component structure
- API integration
- Installation & running

**Read this to**: Understand the web interface and how to use it

---

### **06_CONFIGURATION_MANAGEMENT.md** ⚙️
**What**: Setting up modules and parameters
**Length**: 20 minutes
**Learn**:
- dataset_config.yaml structure
- Adding new modules
- Customizing scores/priorities
- Validation & troubleshooting

**Read this to**: Configure the system for your needs

---

### **07_DATA_FLOW_GUIDE.md** 📊
**What**: Complete end-to-end data flow
**Length**: 25 minutes
**Learn**:
- 5-stage pipeline with example
- Column evolution
- Data quality checkpoints
- Error handling throughout

**Read this to**: Troubleshoot issues or understand entire flow

---

## **Learning Paths**

### **Path 1: "I Just Want to Use It"** 🚀
```
1. 00_SYSTEM_OVERVIEW.md       (understand what it does)
2. 06_CONFIGURATION_MANAGEMENT.md (set up your modules)
3. 05_FRONTEND_INTEGRATION.md   (use the web UI)
4. Run: python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py
5. Done! Use optimized_testcases/
```
**Time**: 30 minutes

---

### **Path 2: "I Want to Understand How It Works"** 🔬
```
1. 00_SYSTEM_OVERVIEW.md           (big picture)
2. 01_NORMALIZATION_LAYER.md        (data standardization)
3. 02_OPTIMIZATION_LAYER.md         (test selection)
4. 03_FEATURE_ENGINEERING_LAYER.md  (data enrichment)
5. 07_DATA_FLOW_GUIDE.md            (complete flow)
```
**Time**: 60 minutes

---

### **Path 3: "I Want to Integrate into My System"** 🔌
```
1. 04_REGRESSION_MANAGER.md         (APIs and services)
2. 06_CONFIGURATION_MANAGEMENT.md   (setup)
3. 05_FRONTEND_INTEGRATION.md       (optional UI)
4. 07_DATA_FLOW_GUIDE.md            (understand flow)
5. Build your integration!
```
**Time**: 90 minutes

---

### **Path 4: "I Need to Debug Something"** 🐛
```
1. 07_DATA_FLOW_GUIDE.md            (understand full flow)
2. Pick the failing layer:
   - Data format issue? → 01_NORMALIZATION_LAYER.md
   - Score seems wrong? → 02_OPTIMIZATION_LAYER.md
   - Missing merge data? → 03_FEATURE_ENGINEERING_LAYER.md
   - API issue? → 04_REGRESSION_MANAGER.md
3. Check "Troubleshooting" section in that file
```
**Time**: Variable

---

## **Common Questions & Where to Find Answers**

### **"What does this system do?"**
→ [00_SYSTEM_OVERVIEW.md](00_SYSTEM_OVERVIEW.md) (section: "What is This Project?")

### **"How does it reduce tests by 98%?"**
→ [02_OPTIMIZATION_LAYER.md](02_OPTIMIZATION_LAYER.md) (section: "The Methodology")

### **"Where do I put my test data?"**
→ [06_CONFIGURATION_MANAGEMENT.md](06_CONFIGURATION_MANAGEMENT.md) (section: "Adding a New Module")

### **"How do I run the system?"**
→ [06_CONFIGURATION_MANAGEMENT.md](06_CONFIGURATION_MANAGEMENT.md) (section: "Quick Config Templates") + Each layer file "How to Run"

### **"I'm getting an error, how do I fix it?"**
→ [07_DATA_FLOW_GUIDE.md](07_DATA_FLOW_GUIDE.md) (section: "Troubleshooting Guide") or appropriate layer file "Error Handling"

### **"Can I customize scoring?"**
→ [06_CONFIGURATION_MANAGEMENT.md](06_CONFIGURATION_MANAGEMENT.md) (section: "How to Customize Scoring")

### **"How do I debug a failed test?"**
→ [03_FEATURE_ENGINEERING_LAYER.md](03_FEATURE_ENGINEERING_LAYER.md) (section: "Use Case 1: Debug a Failed Test")

### **"How do I integrate with CI/CD?"**
→ [04_REGRESSION_MANAGER.md](04_REGRESSION_MANAGER.md) (section: "Integration Points")

### **"What are the output CSVs?"**
→ [02_OPTIMIZATION_LAYER.md](02_OPTIMIZATION_LAYER.md) (section: "The 9-Column Output Format") and [03_FEATURE_ENGINEERING_LAYER.md](03_FEATURE_ENGINEERING_LAYER.md)

### **"How long does each stage take?"**
→ [07_DATA_FLOW_GUIDE.md](07_DATA_FLOW_GUIDE.md) (section: "Time & Performance Through Flow")

---

## **File Organization Reminder**

```
PROJECT ROOT
├── dataset_config.yaml              ← EDIT THIS to configure modules
├── normalize_datasets.py            ← RUN: Layer 1
├── export_optimized_tests.py        ← RUN: Layer 2
├── export_with_full_data.py         ← RUN: Layer 3
├── regression_manager/              ← Layer 4 (APIs)
├── frontend/                        ← Layer 5 (UI)
└── PROJECT_DOCUMENTATION/           ← YOU ARE HERE
    ├── 00_SYSTEM_OVERVIEW.md
    ├── 01_NORMALIZATION_LAYER.md
    ├── 02_OPTIMIZATION_LAYER.md
    ├── 03_FEATURE_ENGINEERING_LAYER.md
    ├── 04_REGRESSION_MANAGER.md
    ├── 05_FRONTEND_INTEGRATION.md
    ├── 06_CONFIGURATION_MANAGEMENT.md
    ├── 07_DATA_FLOW_GUIDE.md
    └── README.md (this file)
```

---

## **Key Concepts to Know**

### **Test Optimization**
The system scores each test and selects the best ones that maintain coverage while reducing execution time.

### **Prioritization**
Tests are assigned P0 (critical) to P3 (low) based on their score, so you know which to run first.

### **Coverage**
The percentage of code exercised by tests. System maintains coverage while reducing test count.

### **Redundancy**
Tests that cover the same code paths. System removes redundant ones automatically.

### **Greedy Algorithm**
Selection method: pick highest-scoring tests first until coverage target is met.

---

## **Recommended Reading Order**

### **First Time Users**
1. **00_SYSTEM_OVERVIEW.md** (10 min)
   - Understand the system
   
2. **06_CONFIGURATION_MANAGEMENT.md** (10 min)
   - Learn how to configure
   
3. **Run the pipeline** (1 min)
   - Execute the scripts
   
4. **05_FRONTEND_INTEGRATION.md** (optional, 5 min)
   - View results in web UI

**Total: ~25 minutes to get started!**

---

### **Power Users (Deep Understanding)**
1. **00_SYSTEM_OVERVIEW.md** (10 min)
2. **01_NORMALIZATION_LAYER.md** (15 min)
3. **02_OPTIMIZATION_LAYER.md** (20 min)
4. **03_FEATURE_ENGINEERING_LAYER.md** (15 min)
5. **04_REGRESSION_MANAGER.md** (20 min)
6. **07_DATA_FLOW_GUIDE.md** (25 min)

**Total: ~105 minutes for complete understanding**

---

## **Quick Reference**

### **Commands**
```bash
# Run full pipeline
python3 normalize_datasets.py && python3 export_optimized_tests.py && python3 export_with_full_data.py

# View results
ls optimized_testcases/
ls optimized_testcases_full/

# Start web UI
cd frontend && npm run dev

# Start API
python3 -c "from regression_manager.api_service import APIService; api = APIService(); api.run()"
```

### **Key Files to Edit**
- **Dataset paths**: `dataset_config.yaml`
- **Optimization parameters**: `regression_manager/config.py`
- **API endpoints**: `regression_manager/api_service.py`
- **Web UI**: `frontend/src/App.jsx`

### **Output Locations**
- **Normalized data**: `normalized_*.csv` (5 columns)
- **Optimized tests**: `optimized_testcases/*.csv` (9 columns)
- **Full data**: `optimized_testcases_full/*.csv` (14-20 columns)
- **Analytics**: `module_analysis_final.json`, `export_manifest.json`

---

## **Getting Help**

### **If Something Doesn't Work**

1. **Check error message** → Search in relevant layer doc
2. **Look in troubleshooting** → Each doc has "Troubleshooting" section
3. **Read 07_DATA_FLOW_GUIDE.md** → Often reveals what went wrong
4. **Check configuration** → Usually dataset_config.yaml issue

### **Common Issues Quick Links**

- **"File not found"** → [06_CONFIGURATION_MANAGEMENT.md](06_CONFIGURATION_MANAGEMENT.md#configuration-issues)
- **"Wrong values in output"** → [02_OPTIMIZATION_LAYER.md](02_OPTIMIZATION_LAYER.md#troubleshooting)
- **"Tests not selected"** → [02_OPTIMIZATION_LAYER.md](02_OPTIMIZATION_LAYER.md#troubleshooting)
- **"Debugging info missing"** → [03_FEATURE_ENGINEERING_LAYER.md](03_FEATURE_ENGINEERING_LAYER.md#error-handling)

---

## **Summary**

This documentation provides:
- ✅ **System overview** - Understand the architecture
- ✅ **Detailed guides** - Learn each layer in depth
- ✅ **Practical examples** - See real usage patterns
- ✅ **Troubleshooting** - Fix common issues
- ✅ **Integration guide** - Connect to your systems
- ✅ **Configuration** - Customize for your needs

**Everything you need to understand and use the system!**

---

## **Feedback & Updates**

Documentation is kept current with system changes.

Last Updated: **April 19, 2026**

---

**Ready to dive in? Start with [00_SYSTEM_OVERVIEW.md](00_SYSTEM_OVERVIEW.md)!** 🚀


#!/usr/bin/env python3
"""
Flexible Data Normalizer for VLSI Test Datasets
Converts different CSV formats to regression manager format

Configuration: Uses dataset_config.yaml for module paths
              Falls back to hardcoded paths if config not found
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import yaml

def normalize_data(csv_path, module_name):
    """
    Normalize any CSV format to regression manager format.
    Returns DataFrame with: testcase_id, module, coverage, runtime_seconds, pass_fail
    """
    print(f"\nNormalizing {module_name}...")
    df = pd.read_csv(csv_path)
    
    print(f"  Original shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    
    # Detect column types
    result_col = None
    coverage_col = None
    runtime_col = None
    
    # Find result column
    for col in df.columns:
        if 'pass' in col.lower() or 'result' in col.lower() or 'fail' in col.lower():
            result_col = col
            break
    
    # Find coverage column
    for col in df.columns:
        if 'coverage' in col.lower() or 'cov' in col.lower():
            coverage_col = col
            break
    
    # Find runtime column
    for col in df.columns:
        if 'runtime' in col.lower() or 'time' in col.lower():
            runtime_col = col
            break
    
    print(f"  Detected: result={result_col}, coverage={coverage_col}, runtime={runtime_col}")
    
    # Create normalized dataframe
    normalized = pd.DataFrame()
    
    # Add testcase_id
    if 'testcase_id' in df.columns:
        normalized['testcase_id'] = df['testcase_id']
    else:
        normalized['testcase_id'] = [f"{module_name}_test_{i}" for i in range(len(df))]
    
    # Add module
    normalized['module_name'] = module_name
    
    # Add coverage (default to 50 if not found)
    if coverage_col and coverage_col in df.columns:
        normalized['coverage'] = df[coverage_col].fillna(50)
    else:
        normalized['coverage'] = 50
    
    # Add runtime (default to 10 if not found)
    if runtime_col and runtime_col in df.columns:
        normalized['runtime_seconds'] = df[runtime_col].fillna(10)
    else:
        normalized['runtime_seconds'] = 10
    
    # Add pass_fail
    if result_col and result_col in df.columns:
        normalized['pass_fail'] = df[result_col]
    else:
        normalized['pass_fail'] = 'PASS'
    
    print(f"  Normalized shape: {normalized.shape}")
    print(f"  Sample:\n{normalized.head()}")
    
    return normalized

def load_config():
    """Load module paths from dataset_config.yaml"""
    config_path = Path('dataset_config.yaml')
    
    if not config_path.exists():
        print("⚠️  dataset_config.yaml not found. Using default paths.")
        return None
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"✅ Loaded config from dataset_config.yaml")
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        print("⚠️  Using default paths instead.")
        return None

def get_modules_from_config(base_dir, config):
    """Convert config.yaml to modules dict"""
    modules = {}
    
    if not config or 'modules' not in config:
        return None
    
    for module_name, module_config in config['modules'].items():
        
        # Skip disabled modules
        if not module_config.get('enabled', True):
            print(f"⏭️  Skipping {module_name} (disabled in config)")
            continue
        
        input_path = module_config.get('input_path')
        if not input_path:
            print(f"❌ {module_name}: No input_path in config")
            continue
        
        # Handle relative and absolute paths
        if input_path.startswith('/') or input_path.startswith('~'):
            # Absolute path
            full_path = Path(input_path).expanduser()
        else:
            # Relative path
            full_path = base_dir / input_path
        
        description = module_config.get('description', module_name)
        modules[module_name] = (full_path, description)
    
    return modules if modules else None

def main():
    """Process all modules with data normalization."""
    base = Path.cwd()
    
    # Try loading from config first
    config = load_config()
    modules = None
    
    if config:
        modules = get_modules_from_config(base, config)
    
    # Fallback to default paths if config not found or failed
    if not modules:
        print("⚠️  Using default hardcoded paths...")
        april_dir = base / "19 aprilt"
        
        modules = {
            "JK_FF": (base / "selected_testcases.csv", "Normalize from pre-optimized results"),
            "T_FF": (april_dir / "t_ff_dataset.csv", "T Flip-Flop test execution data"),
            "Half_Adder": (april_dir / "half_adder_dataset.csv", "Half Adder test execution data"),
            "4bit_Subtractor": (april_dir / "4bit_sub_logs,makefile,results/results/results_1.csv", "4-bit Subtractor"),
            "Register_Comparator": (april_dir / "reg_comparator_logs_makefile_result/results/results_1.csv", "Register Comparator"),
            "8bit_ALU": (april_dir / "8bitalu_logs_makefile_res/results/alu_results_seed_1.csv", "8-bit ALU"),
            "Register_Counter": (april_dir / "reg_COUNTER_LOG_makefile_result/results/regression_report.csv", "Register Counter"),
            "Register_Downcounter": (april_dir / "reg_downcounter_logs_makefile_results/results/results_1.csv", "Register Downcounter"),
        }
    
    print("="*80)
    print("VLSI MODULE DATA NORMALIZATION")
    print("="*80)
    
    normalized_files = {}
    
    for module_name, (csv_path, desc) in modules.items():
        if not csv_path.exists():
            print(f"\n❌ {module_name}: File not found - {csv_path}")
            continue
        
        try:
            print(f"\n[{module_name}] {desc}")
            normalized_df = normalize_data(str(csv_path), module_name)
            
            # Save normalized data
            output_file = base / f"normalized_{module_name.lower()}.csv"
            normalized_df.to_csv(output_file, index=False)
            
            normalized_files[module_name] = {
                'source': str(csv_path),
                'output': str(output_file),
                'rows': len(normalized_df),
                'status': 'success'
            }
            
            print(f"  ✅ Saved to: {output_file}")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            normalized_files[module_name] = {
                'source': str(csv_path),
                'status': 'error',
                'error': str(e)
            }
    
    # Save manifest
    with open('normalization_manifest.json', 'w') as f:
        json.dump(normalized_files, f, indent=2)
    
    print("\n" + "="*80)
    print("NORMALIZATION COMPLETE")
    print("="*80)
    print(f"\n✅ Manifest saved to: normalization_manifest.json")
    
    # Print summary
    successful = len([d for d in normalized_files.values() if d.get('status') == 'success'])
    print(f"Successfully normalized {successful}/{len(normalized_files)} modules")

if __name__ == '__main__':
    main()

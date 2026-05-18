#!/usr/bin/env python3
"""Analyze multiple VLSI modules with Regression Manager separately."""

import os
import json
import pandas as pd
from pathlib import Path
from regression_manager.regression_manager_agent import RegressionManagerAgent

def get_file_info(csv_path):
    """Get info about CSV file."""
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return {
                'exists': True,
                'rows': len(df),
                'columns': list(df.columns)
            }
    except:
        pass
    return {'exists': False}

def main():
    base = Path.cwd()
    april_dir = base / "19 aprilt"
    
    modules = {
        "JK_FF": "selected_testcases.csv",
        "T_FF": "19 aprilt/t_ff_dataset.csv",
        "Half_Adder": "19 aprilt/half_adder_dataset.csv",
        "4bit_Subtractor": "19 aprilt/4bit_sub_logs,makefile,results/results/results_1.csv",
        "Register_Comparator": "19 aprilt/reg_comparator_logs_makefile_result/results/results_1.csv",
        "8bit_ALU": "19 aprilt/8bitalu_logs_makefile_res/results/alu_results_seed_1.csv",
        "Register_Counter": "19 aprilt/reg_COUNTER_LOG_makefile_result/results/regression_report.csv",
        "Register_Downcounter": "19 aprilt/reg_downcounter_logs_makefile_results/results/results_1.csv",
    }
    
    print("\n" + "="*80)
    print("VLSI MODULE REGRESSION ANALYSIS")
    print("="*80)
    
    results = {}
    
    for module_name, csv_file in modules.items():
        csv_path = base / csv_file
        print(f"\n[{module_name}]")
        print(f"CSV: {csv_file}")
        
        file_info = get_file_info(str(csv_path))
        
        if not file_info.get('exists'):
            print(f"❌ File not found")
            results[module_name] = {'status': 'not_found'}
            continue
        
        print(f"✅ Found: {file_info['rows']} rows, {len(file_info['columns'])} columns")
        
        try:
            print("  Running Regression Manager...")
            agent = RegressionManagerAgent(csv_path=str(csv_path))
            result = agent.run()
            
            all_tests = result.get('all_tests', [])
            optimized = result.get('optimized_tests', [])
            excluded = len(all_tests) - len(optimized)
            
            print(f"  ✅ Analysis complete:")
            print(f"     Total: {len(all_tests)}")
            print(f"     Selected: {len(optimized)}")
            print(f"     Excluded: {excluded}")
            if all_tests:
                print(f"     Reduction: {(excluded/len(all_tests)*100):.1f}%")
            
            redundant = len([t for t in all_tests if t.get('is_redundant')])
            print(f"     Redundant: {redundant}")
            
            results[module_name] = {
                'status': 'success',
                'total': len(all_tests),
                'selected': len(optimized),
                'excluded': excluded,
                'reduction_percent': (excluded/len(all_tests)*100) if all_tests else 0,
                'redundant': redundant
            }
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[module_name] = {'status': 'error', 'error': str(e)}
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n{'Module':<25} {'Total':<10} {'Selected':<10} {'Reduction':<12} {'Redundant':<10}")
    print("-"*80)
    
    for module, data in results.items():
        if data.get('status') == 'success':
            print(f"{module:<25} {data['total']:<10} {data['selected']:<10} "
                  f"{data['reduction_percent']:>10.1f}% {data['redundant']:<10}")
        else:
            print(f"{module:<25} {data.get('status', 'N/A'):<30}")
    
    # Save results
    with open('module_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to module_analysis_results.json")
    
    # Print statistics
    successful = len([d for d in results.values() if d.get('status') == 'success'])
    total_modules = len(results)
    print(f"\nAnalyzed {successful}/{total_modules} modules successfully")

if __name__ == '__main__':
    main()

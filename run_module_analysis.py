#!/usr/bin/env python3
"""
Run Regression Manager analysis on all normalized VLSI modules.
"""

import os
from pathlib import Path
from regression_manager.regression_manager_agent import RegressionManagerAgent
import json
import pandas as pd

def analyze_module(normalized_csv, module_name):
    """Analyze a single normalized module."""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {module_name}")
    print(f"{'='*80}")
    
    if not os.path.exists(normalized_csv):
        print(f"❌ File not found: {normalized_csv}")
        return None
    
    try:
        # Load data info
        df = pd.read_csv(normalized_csv)
        print(f"Data: {len(df)} test cases")
        
        # Initialize and run agent
        print(f"Starting Regression Manager Agent...")
        agent = RegressionManagerAgent(csv_path=normalized_csv)
        result = agent.run()
        
        # Extract results
        all_tests = result.get('all_tests', [])
        optimized_tests = result.get('optimized_tests', [])
        summary = result.get('summary', {})
        
        # Calculate metrics
        excluded = len(all_tests) - len(optimized_tests)
        reduction_pct = (excluded / len(all_tests) * 100) if all_tests else 0
        redundant = len([t for t in all_tests if t.get('is_redundant', False)])
        
        # Coverage analysis
        avg_coverage = None
        if optimized_tests:
            coverages = [t.get('coverage', 0) for t in optimized_tests]
            avg_coverage = sum(coverages) / len(coverages) if coverages else None
        
        # Runtime analysis
        total_runtime = None
        if optimized_tests:
            runtimes = [t.get('runtime_seconds', 0) for t in optimized_tests]
            total_runtime = sum(runtimes) if runtimes else None
        
        # Priority distribution
        priorities = {}
        for test in optimized_tests:
            p = test.get('priority_rank', 'unranked')
            priorities[p] = priorities.get(p, 0) + 1
        
        print(f"\n[RESULTS]")
        print(f"-" * 80)
        print(f"Total Tests:        {len(all_tests)}")
        print(f"Selected Tests:     {len(optimized_tests)}")
        print(f"Excluded Tests:     {excluded}")
        print(f"Reduction:          {reduction_pct:.1f}%")
        print(f"Redundant Tests:    {redundant}")
        
        if avg_coverage:
            print(f"Avg Coverage:       {avg_coverage:.2f}%")
        if total_runtime:
            print(f"Total Runtime:      {total_runtime:.2f}s ({total_runtime/60:.2f}m)")
        
        print(f"\n[PRIORITY DISTRIBUTION]")
        for p in sorted(priorities.keys()):
            print(f"  {p}: {priorities[p]} tests")
        
        # Top 10 tests
        if optimized_tests:
            print(f"\n[TOP 10 SELECTED TESTS]")
            print(f"{'Rank':<6} {'Test ID':<30} {'Coverage':<10} {'Score':<10}")
            for i, test in enumerate(optimized_tests[:10], 1):
                print(f"{i:<6} {test.get('testcase_id', 'N/A'):<30} "
                      f"{test.get('coverage', 0):<10.2f} {test.get('final_score', 0):<10.2f}")
        
        result_dict = {
            'module': module_name,
            'total_tests': len(all_tests),
            'selected_tests': len(optimized_tests),
            'excluded_tests': excluded,
            'reduction_percent': reduction_pct,
            'redundant_tests': redundant,
            'avg_coverage': avg_coverage,
            'total_runtime': total_runtime,
            'priorities': priorities
        }
        
        return result_dict
        
    except Exception as e:
        print(f"❌ Error analyzing {module_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run analysis on all normalized modules."""
    base = Path.cwd()
    
    modules = {
        "JK Flip-Flop": base / "normalized_jk_ff.csv",
        "T Flip-Flop": base / "normalized_t_ff.csv",
        "Half Adder": base / "normalized_half_adder.csv",
        "4-bit Subtractor": base / "normalized_4bit_subtractor.csv",
        "Register Comparator": base / "normalized_register_comparator.csv",
        "8-bit ALU": base / "normalized_8bit_alu.csv",
        "Register Counter": base / "normalized_register_counter.csv",
        "Register Downcounter": base / "normalized_register_downcounter.csv",
    }
    
    print("="*80)
    print("VLSI MODULE REGRESSION ANALYSIS")
    print("Analyzing all modules with Regression Manager")
    print("="*80)
    
    all_results = {}
    
    for module_name, csv_path in modules.items():
        result = analyze_module(str(csv_path), module_name)
        if result:
            all_results[module_name] = result
    
    # Print summary
    print(f"\n\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"\n{'Module':<25} {'Total':<10} {'Selected':<10} {'Reduction':<12} {'Redundant':<10}")
    print("-"*80)
    
    for module_name, data in all_results.items():
        print(f"{module_name:<25} {data['total_tests']:<10} {data['selected_tests']:<10} "
              f"{data['reduction_percent']:>10.1f}% {data['redundant_tests']:<10}")
    
    # Save detailed results
    with open('all_modules_analysis.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Detailed results saved to: all_modules_analysis.json")
    
    # Calculate totals
    total_tests = sum(r['total_tests'] for r in all_results.values())
    total_selected = sum(r['selected_tests'] for r in all_results.values())
    total_excluded = sum(r['excluded_tests'] for r in all_results.values())
    avg_reduction = sum(r['reduction_percent'] for r in all_results.values()) / len(all_results) if all_results else 0
    
    print(f"\n[AGGREGATE STATISTICS]")
    print(f"-"*80)
    print(f"Total all modules:  {total_tests} tests")
    print(f"Selected:           {total_selected} tests ({total_selected/max(1,total_tests)*100:.1f}%)")
    print(f"Excluded:           {total_excluded} tests ({total_excluded/max(1,total_tests)*100:.1f}%)")
    print(f"Average reduction:  {avg_reduction:.1f}%")

if __name__ == '__main__':
    main()

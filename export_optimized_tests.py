#!/usr/bin/env python3
"""
Direct VLSI Module Analysis with CSV Export
Analyzes each module and exports optimized test cases to individual CSV files.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, List

class DirectModuleAnalyzer:
    """Implements regression optimization and exports optimized tests to CSV."""
    
    def __init__(self, csv_path: str, module_name: str):
        self.csv_path = csv_path
        self.module_name = module_name
        self.df = None
        self.results = {}
        self.optimized_df = None
    
    def load_data(self):
        """Load and prepare data."""
        self.df = pd.read_csv(self.csv_path)
        print(f"  Loaded {len(self.df)} test cases")
        return self.df
    
    def compute_features(self):
        """Compute efficiency and redundancy features."""
        df = self.df.copy()
        
        # Ensure required columns
        if 'coverage' not in df.columns:
            df['coverage'] = 50
        if 'runtime_seconds' not in df.columns:
            df['runtime_seconds'] = 10
        if 'pass_fail' not in df.columns:
            df['pass_fail'] = 'PASS'
        
        # Compute rolling mean
        df['rolling_mean_coverage'] = df['coverage'].rolling(window=5, min_periods=1).mean()
        
        # Coverage gain
        df['coverage_gain'] = df['coverage'] - df['rolling_mean_coverage']
        
        # Efficiency
        df['efficiency_score'] = df['coverage_gain'] / (df['runtime_seconds'] + 1)
        
        # Normalization
        min_eff = df['efficiency_score'].min()
        max_eff = df['efficiency_score'].max()
        if max_eff > min_eff:
            df['efficiency_normalized'] = (df['efficiency_score'] - min_eff) / (max_eff - min_eff)
        else:
            df['efficiency_normalized'] = 0.5
        
        # Pass rate
        df['pass_count'] = (df['pass_fail'] == 'PASS').astype(int)
        df['cumulative_passes'] = df['pass_count'].cumsum()
        df['cumulative_runs'] = range(1, len(df) + 1)
        df['pass_rate'] = df['cumulative_passes'] / df['cumulative_runs']
        
        # Redundancy detection
        df['is_redundant'] = (
            (df['pass_rate'] > 0.95) &
            (df['coverage_gain'] < 1.0) &
            (df['pass_fail'] == 'PASS')
        )
        
        # Scoring
        w_coverage = 0.4
        w_efficiency = 0.35
        w_stability = 0.25
        
        df['base_score'] = (
            w_coverage * (df['coverage'] / 100) +
            w_efficiency * df['efficiency_normalized'] +
            w_stability * df['pass_rate']
        )
        
        # Redundancy penalty
        redundancy_penalty = df['is_redundant'].astype(int) * 0.8
        
        # Final score
        df['final_score'] = df['base_score'] - redundancy_penalty
        df['final_score'] = df['final_score'].clip(lower=0)
        
        self.df = df
        return df
    
    def prioritize(self):
        """Rank tests by priority."""
        df = self.df.copy()
        
        # Sort by final_score descending
        df = df.sort_values('final_score', ascending=False).reset_index(drop=True)
        
        # Assign priority rank
        df['priority_rank'] = pd.cut(df['final_score'], 
                                      bins=[0, 0.2, 0.5, 0.7, 1.0],
                                      labels=['P3', 'P2', 'P1', 'P0'],
                                      include_lowest=True)
        
        # Action based on score
        def get_action(score):
            if score >= 0.7:
                return 'run_first'
            elif score >= 0.5:
                return 'run_early'
            elif score >= 0.2:
                return 'run_normal'
            else:
                return 'run_late'
        
        df['action'] = df['final_score'].apply(get_action)
        
        self.df = df
        return df
    
    def select_tests(self, keep_redundant=False):
        """Select non-redundant tests."""
        df = self.df.copy()
        
        if keep_redundant:
            selected = df
        else:
            selected = df[~df['is_redundant']].copy()
        
        return selected
    
    def export_optimized_tests(self, base_path: Path):
        """Export optimized tests to CSV file."""
        selected_tests = self.select_tests(keep_redundant=False)
        
        if len(selected_tests) == 0:
            print(f"  ⚠️  No tests to export")
            return None
        
        # Select relevant columns for export
        export_columns = [
            'testcase_id', 'module_name', 'coverage', 'runtime_seconds', 
            'pass_fail', 'pass_rate', 'final_score', 'priority_rank', 'action'
        ]
        
        # Keep only existing columns
        export_columns = [col for col in export_columns if col in selected_tests.columns]
        
        export_df = selected_tests[export_columns].copy()
        
        # Create output filename
        safe_name = self.module_name.lower().replace(' ', '_').replace('-', '_')
        output_file = base_path / f"optimized_{safe_name}.csv"
        
        # Save to CSV
        export_df.to_csv(output_file, index=False)
        
        print(f"  ✅ Exported {len(export_df)} optimized tests to: {output_file}")
        
        self.optimized_df = export_df
        return output_file
    
    def generate_report(self):
        """Generate analysis report."""
        
        print(f"\n[ANALYSIS: {self.module_name}]")
        print(f"-" * 80)
        
        all_tests = self.df
        selected_tests = self.select_tests(keep_redundant=False)
        excluded_tests = all_tests[all_tests['is_redundant']]
        
        # Basic stats
        total = len(all_tests)
        selected_count = len(selected_tests)
        excluded_count = len(excluded_tests)
        reduction = (excluded_count / total * 100) if total > 0 else 0
        
        print(f"Total Tests:        {total}")
        print(f"Selected Tests:     {selected_count}")
        print(f"Excluded Tests:     {excluded_count}")
        print(f"Reduction:          {reduction:.1f}%")
        
        # Coverage stats
        if selected_count > 0:
            avg_coverage = selected_tests['coverage'].mean()
            print(f"Avg Coverage:       {avg_coverage:.2f}%")
            
            total_runtime = selected_tests['runtime_seconds'].sum()
            print(f"Total Runtime:      {total_runtime:.2f}s ({total_runtime/60:.2f}m)")
        
        # Priority distribution
        if 'priority_rank' in selected_tests.columns:
            priority_dist = selected_tests['priority_rank'].value_counts().sort_index(ascending=False)
            print(f"\n[PRIORITY DISTRIBUTION]")
            for priority, count in priority_dist.items():
                print(f"  {priority}: {count}")
        
        # Pass rate
        pass_count = (selected_tests['pass_fail'] == 'PASS').sum()
        print(f"\nPass Rate:          {pass_count}/{selected_count} ({pass_count/max(1,selected_count)*100:.1f}%)")
        
        # Top 10 tests
        top_10 = selected_tests.head(10)
        print(f"\n[TOP 10 TESTS BY SCORE]")
        print(f"{'#':<4} {'TestID':<30} {'Coverage':<10} {'Score':<10} {'Priority':<8}")
        for i, (_, row) in enumerate(top_10.iterrows(), 1):
            test_id = str(row['testcase_id'])[:28]
            priority = row.get('priority_rank', 'N/A')
            print(f"{i:<4} {test_id:<30} {row['coverage']:<10.2f} {row['final_score']:<10.2f} {priority:<8}")
        
        self.results = {
            'module': self.module_name,
            'total_tests': total,
            'selected_tests': selected_count,
            'excluded_tests': excluded_count,
            'reduction_percent': reduction,
            'avg_coverage': avg_coverage if selected_count > 0 else None,
            'total_runtime': total_runtime if selected_count > 0 else None,
            'pass_rate': pass_count / max(1, selected_count),
            'priority_distribution': priority_dist.to_dict() if 'priority_rank' in selected_tests.columns else {}
        }
        
        return self.results
    
    def analyze(self):
        """Run complete analysis."""
        self.load_data()
        self.compute_features()
        self.prioritize()
        self.generate_report()
        return self.results


def main():
    """Run analysis on all normalized modules and export optimized tests."""
    base = Path.cwd()
    output_dir = base / "optimized_testcases"
    output_dir.mkdir(exist_ok=True)
    
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
    print("VLSI MODULE ANALYSIS WITH CSV EXPORT")
    print("Exporting optimized tests to individual CSV files")
    print("="*80)
    
    all_results = {}
    export_files = {}
    
    for module_name, csv_path in modules.items():
        try:
            if not csv_path.exists():
                print(f"\n❌ {module_name}: File not found")
                continue
            
            analyzer = DirectModuleAnalyzer(str(csv_path), module_name)
            result = analyzer.analyze()
            all_results[module_name] = result
            
            # Export optimized tests to CSV
            export_file = analyzer.export_optimized_tests(output_dir)
            if export_file:
                export_files[module_name] = str(export_file)
            
        except Exception as e:
            print(f"\n❌ {module_name}: {str(e)}")
    
    # Print aggregate summary
    print(f"\n\n{'='*80}")
    print("AGGREGATE SUMMARY")
    print(f"{'='*80}")
    print(f"\n{'Module':<25} {'Total':<10} {'Selected':<10} {'Reduction':<12} {'Pass Rate':<10}")
    print("-"*80)
    
    total_all = 0
    selected_all = 0
    excluded_all = 0
    
    for module_name, data in all_results.items():
        total_all += data['total_tests']
        selected_all += data['selected_tests']
        excluded_all += data['excluded_tests']
        
        print(f"{module_name:<25} {data['total_tests']:<10} {data['selected_tests']:<10} "
              f"{data['reduction_percent']:>10.1f}% {data['pass_rate']:>10.1%}")
    
    print("-"*80)
    overall_reduction = (excluded_all / total_all * 100) if total_all > 0 else 0
    print(f"{'TOTAL':<25} {total_all:<10} {selected_all:<10} {overall_reduction:>10.1f}%")
    
    # Summary of exports
    print(f"\n\n{'='*80}")
    print("CSV EXPORT SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"Output Directory: {output_dir}\n")
    print(f"{'Module':<25} {'CSV File':<40} {'Tests':<10}")
    print("-"*80)
    
    for module_name, file_path in export_files.items():
        if module_name in all_results:
            selected_count = all_results[module_name]['selected_tests']
            file_name = Path(file_path).name
            print(f"{module_name:<25} {file_name:<40} {selected_count:<10}")
    
    # Save results summary
    with open(base / 'module_analysis_final.json', 'w') as f:
        # Convert numpy types to native Python types for JSON serialization
        json_data = {}
        for module_name, data in all_results.items():
            json_data[module_name] = {
                'total_tests': int(data['total_tests']),
                'selected_tests': int(data['selected_tests']),
                'excluded_tests': int(data['excluded_tests']),
                'reduction_percent': float(data['reduction_percent']),
                'avg_coverage': float(data['avg_coverage']) if data['avg_coverage'] else None,
                'total_runtime': float(data['total_runtime']) if data['total_runtime'] else None,
                'pass_rate': float(data['pass_rate'])
            }
        json.dump(json_data, f, indent=2)
    
    with open(base / 'export_manifest.json', 'w') as f:
        json.dump({
            'output_directory': str(output_dir),
            'total_modules': len(export_files),
            'exported_files': export_files,
            'timestamp': pd.Timestamp.now().isoformat()
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: module_analysis_final.json")
    print(f"✅ Export manifest saved to: export_manifest.json")
    print(f"✅ Optimized tests exported to: {output_dir}/")
    print(f"\n📊 Analyzed {len(all_results)} modules successfully")
    print(f"💾 Created {len(export_files)} CSV files with optimized test cases")

if __name__ == '__main__':
    main()

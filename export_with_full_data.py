#!/usr/bin/env python3
"""
Export Optimized Tests with FULL Original Dataset Columns
Exports optimized test cases with ALL original data columns plus scoring/ranking.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, List

class FullDataExporter:
    """Exports optimized tests with complete dataset information."""
    
    def __init__(self, normalized_csv: str, original_csv: str, module_name: str):
        self.normalized_csv = normalized_csv
        self.original_csv = original_csv
        self.module_name = module_name
        self.df_normalized = None
        self.df_original = None
        self.df_merged = None
        
    def load_normalized_data(self):
        """Load normalized data with scoring."""
        try:
            self.df_normalized = pd.read_csv(self.normalized_csv)
            print(f"  ✅ Loaded normalized data: {len(self.df_normalized)} rows")
            return self.df_normalized
        except Exception as e:
            print(f"  ❌ Error loading normalized data: {e}")
            return None
    
    def load_original_data(self):
        """Load original full dataset."""
        try:
            self.df_original = pd.read_csv(self.original_csv)
            print(f"  ✅ Loaded original data: {len(self.df_original)} rows, {len(self.df_original.columns)} columns")
            print(f"     Columns: {', '.join(self.df_original.columns.tolist())}")
            return self.df_original
        except Exception as e:
            print(f"  ⚠️  Could not load original data: {e}")
            return None
    
    def merge_data(self):
        """Merge original data with scoring columns by row index."""
        if self.df_normalized is None:
            print("  Normalized data not loaded")
            return None
        
        if self.df_original is None:
            print("  ⚠️  Original data not available, using normalized data only")
            self.df_merged = self.df_normalized.copy()
            return self.df_merged
        
        # Merge by row index (since normalized was derived from original)
        try:
            # Handle different row counts (take minimum)
            min_rows = min(len(self.df_original), len(self.df_normalized))
            
            df_orig_trimmed = self.df_original.iloc[:min_rows].reset_index(drop=True)
            df_norm_trimmed = self.df_normalized.iloc[:min_rows].reset_index(drop=True)
            
            # Merge by index
            merged = pd.concat(
                [df_orig_trimmed, df_norm_trimmed],
                axis=1,
                join='inner'
            )
            
            # Remove duplicate and redundant columns
            seen = set()
            cols_to_keep = []
            
            for col in merged.columns:
                # Clean column name (remove _x, _y suffixes)
                clean_col = col.replace('_x', '').replace('_y', '')
                
                # Skip if we've already seen this conceptual column
                if clean_col not in seen:
                    seen.add(clean_col)
                    cols_to_keep.append(col)
                    
            merged = merged[cols_to_keep]
            
            # Rename columns to remove _x, _y if they exist
            merged.columns = [col.replace('_x', '').replace('_y', '') for col in merged.columns]
            
            # Drop truly redundant columns (keep only scoring versions)
            cols_to_drop = []
            
            # Keep normalized versions, drop original if duplicated
            if 'PassFail' in merged.columns and 'pass_fail' in merged.columns:
                cols_to_drop.append('PassFail')
            
            # Keep normalized coverage/runtime
            if 'Coverage' in merged.columns and 'coverage' in merged.columns:
                cols_to_drop.append('Coverage')
            if 'Time' in merged.columns and 'runtime_seconds' in merged.columns:
                cols_to_drop.append('Time')
            if 'runtime' in merged.columns and 'runtime_seconds' in merged.columns:
                cols_to_drop.append('runtime')
            
            # Remove delta columns (we have coverage percentage)
            if 'DeltaCov' in merged.columns:
                cols_to_drop.append('DeltaCov')
            
            merged = merged.drop(columns=cols_to_drop, errors='ignore')
            
            print(f"  ✅ Merged data: {len(merged)} rows, {len(merged.columns)} columns")
            self.df_merged = merged
            return merged
            
        except Exception as e:
            print(f"  ❌ Error merging data: {e}")
            return self.df_normalized.copy()
    
    def export_with_full_data(self, base_path: Path, selected_testcases: pd.DataFrame):
        """Export selected tests with all original columns."""
        if self.df_merged is None:
            print("  ❌ No merged data available")
            return None
        
        if selected_testcases is None or len(selected_testcases) == 0:
            print("  ❌ No test cases provided for export")
            return None
        
        # Since we merged by index, get the indices of selected tests
        try:
            # Get indicesof selected tests
            selected_indices = selected_testcases.index.tolist()
            
            # Filter merged data by index
            selected_merged = self.df_merged.loc[selected_indices].copy()
            
            # Reorder columns: original (test parameters) first, then scoring columns
            scoring_columns = [
                'testcase_id', 'module_name', 'pass_rate', 'final_score', 'priority_rank', 'action'
            ]
            
            # Get original/test input columns (exclude scoring columns)
            original_cols = [col for col in self.df_merged.columns 
                           if col not in scoring_columns]
            
            # Build final column order: test inputs first, then scoring
            final_columns = original_cols + [col for col in scoring_columns if col in selected_merged.columns]
            
            # Keep only columns that exist
            final_columns = [col for col in final_columns if col in selected_merged.columns]
            
            export_df = selected_merged[final_columns].copy()
            
            # Create output filename
            safe_name = self.module_name.lower().replace(' ', '_').replace('-', '_')
            output_file = base_path / f"optimized_{safe_name}_full.csv"
            
            # Save to CSV
            export_df.to_csv(output_file, index=False)
            
            print(f"  ✅ Exported {len(export_df)} tests with {len(export_df.columns)} columns")
            print(f"     Columns: {', '.join(export_df.columns.tolist()[:5])} ... (+ {len(export_df.columns)-5} more)")
            print(f"     Output: {output_file}")
            
            return output_file
            
        except Exception as e:
            print(f"  ❌ Error exporting data: {e}")
            import traceback
            traceback.print_exc()
            return None


class DirectModuleAnalyzer:
    """Implements regression optimization."""
    
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
    
    def analyze(self):
        """Run complete analysis."""
        self.load_data()
        self.compute_features()
        self.prioritize()
        return self.select_tests(keep_redundant=False)


# Module mappings: (normalized_csv, original_csv, display_name)
MODULE_MAPPINGS = {
    "JK Flip-Flop": (
        "normalized_jk_ff.csv",
        "19 aprilt/half_adder_dataset.csv",
        "JK Flip-Flop"
    ),
    "T Flip-Flop": (
        "normalized_t_ff.csv",
        "19 aprilt/t_ff_dataset.csv",
        "T Flip-Flop"
    ),
    "Half Adder": (
        "normalized_half_adder.csv",
        "19 aprilt/half_adder_dataset.csv",
        "Half Adder"
    ),
    "4-bit Subtractor": (
        "normalized_4bit_subtractor.csv",
        "19 aprilt/4bit_sub_logs,makefile,results/results/results_1.csv",
        "4-bit Subtractor"
    ),
    "Register Comparator": (
        "normalized_register_comparator.csv",
        "19 aprilt/reg_comparator_logs_makefile_result/results/results_1.csv",
        "Register Comparator"
    ),
    "8-bit ALU": (
        "normalized_8bit_alu.csv",
        "19 aprilt/8bitalu_logs_makefile_res/results/alu_results_seed_1.csv",
        "8-bit ALU"
    ),
    "Register Counter": (
        "normalized_register_counter.csv",
        "19 aprilt/reg_COUNTER_LOG_makefile_result/results/regression_report.csv",
        "Register Counter"
    ),
    "Register Downcounter": (
        "normalized_register_downcounter.csv",
        "19 aprilt/reg_downcounter_logs_makefile_results/results/results_1.csv",
        "Register Downcounter"
    ),
}


def main():
    """Export optimized tests with full original data."""
    base = Path.cwd()
    output_dir = base / "optimized_testcases_full"
    output_dir.mkdir(exist_ok=True)
    
    all_results = {}
    
    for module_name, (norm_file, orig_file, display_name) in MODULE_MAPPINGS.items():
        print(f"\n{'='*80}")
        print(f"[PROCESSING: {display_name}]")
        print(f"{'='*80}")
        
        norm_path = base / norm_file
        orig_path = base / orig_file
        
        # Check if normalized file exists
        if not norm_path.exists():
            print(f"⚠️  Normalized file not found: {norm_path}")
            continue
        
        try:
            print(f"\n1. Analyzing {display_name}...")
            
            # Run analysis on normalized data to get scoring columns
            analyzer = DirectModuleAnalyzer(str(norm_path), display_name)
            analyzed_df = analyzer.analyze()  # This has scoring columns
            
            print(f"\n2. Preparing full data export...")
            
            # Load original data
            if orig_path.exists():
                df_original = pd.read_csv(orig_path)
                print(f"  ✅ Loaded original data: {len(df_original)} rows, {len(df_original.columns)} columns")
            else:
                print(f"  ⚠️  Original file not found: {orig_path}")
                df_original = None
            
            # Merge original data with analyzed/scored data by index
            if df_original is not None:
                min_rows = min(len(df_original), len(analyzed_df))
                df_orig_trimmed = df_original.iloc[:min_rows].copy()
                df_analyzed_trimmed = analyzed_df.iloc[:min_rows].copy()
                
                # Get column names from analyzed (includes scoring)
                scoring_and_processed = ['testcase_id', 'module_name', 'coverage', 'runtime_seconds', 
                                       'pass_fail', 'pass_rate', 'final_score', 'priority_rank', 'action']
                
                # From original: all except pass_fail, coverage, runtime_seconds (use analyzed versions)
                original_cols = [c for c in df_orig_trimmed.columns 
                               if c not in ['pass_fail', 'coverage', 'runtime_seconds', 'runtime', 'Time']]
                
                # From analyzed: only scoring and processed columns
                analyzed_cols = [c for c in scoring_and_processed if c in df_analyzed_trimmed.columns]
                
                # Build export dataframe
                export_df = pd.DataFrame()
                
                # Add original columns
                for col in original_cols:
                    export_df[col] = df_orig_trimmed[col]
                
                # Add processed/scoring columns from analyzed
                for col in analyzed_cols:
                    export_df[col] = df_analyzed_trimmed[col]
                
                print(f"  ✅ Merged data with {len(export_df.columns)} final columns")
            else:
                export_df = analyzed_df.copy()
            
            # Export to CSV
            safe_name = display_name.lower().replace(' ', '_').replace('-', '_')
            output_file = output_dir / f"optimized_{safe_name}_full.csv"
            export_df.to_csv(output_file, index=False)
            
            print(f"  ✅ Exported {len(export_df)} tests with {len(export_df.columns)} columns")
            print(f"     First 5 columns: {', '.join(export_df.columns[:5])}")
            print(f"     ... + {len(export_df.columns)-5} more")
            print(f"     Output: {output_file}")
            
            all_results[display_name] = {
                'status': 'success',
                'output_file': str(output_file),
                'tests_exported': len(export_df),
                'total_columns': len(export_df.columns)
            }
            
        except Exception as e:
            print(f"  ❌ Error processing {display_name}: {e}")
            import traceback
            traceback.print_exc()
            all_results[display_name] = {
                'status': 'failed',
                'error': str(e)
            }
    
    # Save results manifest
    print(f"\n{'='*80}")
    print("[EXPORT COMPLETE]")
    print(f"{'='*80}")
    
    manifest = {
        'export_type': 'Full Data with All Original Columns + Scoring',
        'output_directory': str(output_dir),
        'modules_processed': all_results,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    manifest_file = base / "export_full_data_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Manifest saved: {manifest_file}")
    
    # Print summary
    print(f"\n[SUMMARY]")
    success_count = 0
    for module, result in all_results.items():
        if result['status'] == 'success':
            print(f"✅ {module}: {result['tests_exported']} tests, {result['total_columns']} columns")
            success_count += 1
        else:
            print(f"❌ {module}: {result.get('error', 'Unknown error')}")
    
    print(f"\nSuccessfully exported: {success_count}/{len(all_results)} modules")


if __name__ == '__main__':
    main()

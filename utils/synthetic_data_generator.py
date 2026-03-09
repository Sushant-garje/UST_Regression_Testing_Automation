"""
Synthetic testcase data generator for testing and development.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class SyntheticDataGenerator:
    """Generates synthetic testcase data for testing."""
    
    def __init__(self, num_tests: int = 1000, num_modules: int = 20, seed: int = 42):
        """
        Initialize generator.
        
        Args:
            num_tests: Number of testcases to generate
            num_modules: Number of unique modules
            seed: Random seed for reproducibility
        """
        self.num_tests = num_tests
        self.num_modules = num_modules
        self.seed = seed
        np.random.seed(seed)
        
    def generate(self) -> pd.DataFrame:
        """
        Generate synthetic testcase data.
        
        Returns:
            DataFrame with synthetic testcase data
        """
        data = []
        
        modules = [f'module_{i:03d}' for i in range(self.num_modules)]
        
        for i in range(self.num_tests):
            module = np.random.choice(modules)
            test_name = f'test_{i:04d}'
            seed_val = np.random.randint(1, 100)
            
            # Generate coverage (biased towards higher values)
            coverage = np.random.beta(5, 2) * 100
            
            # Generate runtime (log-normal distribution)
            runtime = np.random.lognormal(2, 1)
            
            # Generate pass/fail (80% pass rate)
            result = 'PASS' if np.random.random() > 0.2 else 'FAIL'
            
            # Simulate multiple runs per testcase
            num_runs = np.random.randint(5, 20)
            
            for run in range(num_runs):
                sim_time = runtime * (run + 1)
                
                # Coverage increases with runs (diminishing returns)
                run_coverage = min(100, coverage + run * np.random.uniform(0, 2))
                
                # Occasional failures
                if np.random.random() < 0.15:
                    run_result = 'FAIL'
                else:
                    run_result = result
                
                data.append({
                    'module': module,
                    'test': test_name,
                    'seed': seed_val,
                    'rtl_version': 'v1.0',
                    'git_commit': f'commit_{np.random.randint(1, 100):03d}',
                    'result': run_result,
                    'coverage': round(run_coverage, 2),
                    'sim_time': round(sim_time, 2),
                    'test_runtime': round(runtime, 2)
                })
        
        df = pd.DataFrame(data)
        return df
    
    def save(self, output_path: str):
        """
        Generate and save synthetic data to CSV.
        
        Args:
            output_path: Path to save CSV file
        """
        df = self.generate()
        df.to_csv(output_path, index=False)
        print(f"Generated {len(df)} records and saved to {output_path}")


if __name__ == '__main__':
    generator = SyntheticDataGenerator(num_tests=1000, num_modules=20)
    generator.save('synthetic_testcases.csv')

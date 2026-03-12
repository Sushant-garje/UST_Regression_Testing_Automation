"""
Data loader module for CSV and log data ingestion.
Handles reading and initial validation of input data sources.
Flexible loader that adapts to different CSV formats.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and validates CSV testcase data with flexible column mapping."""
    
    # Column mapping for different CSV formats
    COLUMN_MAPPINGS = {
        # Standard format
        'module': ['module', 'Module', 'MODULE', 'module_name', 'ModuleName'],
        'test': ['test', 'Test', 'TEST', 'test_name', 'TestName', 'TestID', 'test_id'],
        'seed': ['seed', 'Seed', 'SEED', 'random_seed', 'RandomSeed'],
        'result': ['result', 'Result', 'RESULT', 'status', 'Status', 'STATUS', 'pass_fail', 'PassFail'],
        'coverage': ['coverage', 'Coverage', 'COVERAGE', 'cov', 'Coverage(%)', 'coverage_percentage'],
        'sim_time': ['sim_time', 'SimTime', 'simulation_time', 'runtime', 'Runtime', 'time', 'Time']
    }
    
    def __init__(self, csv_path: str):
        """
        Initialize data loader.
        
        Args:
            csv_path: Path to CSV file containing testcase data
        """
        self.csv_path = Path(csv_path)
        
    def load_csv(self) -> pd.DataFrame:
        """
        Load CSV data with flexible column detection.
        
        Returns:
            DataFrame with testcase data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        logger.info(f"Loading CSV from {self.csv_path}")
        df = pd.read_csv(self.csv_path)
        
        logger.info(f"Loaded {len(df)} records with columns: {list(df.columns)}")
        
        # Try to map columns flexibly
        df = self._map_columns(df)
        
        return df
    
    def _map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map CSV columns to standard names flexibly.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        column_map = {}
        available_cols = set(df.columns)
        
        # Try to find each required column
        for standard_name, possible_names in self.COLUMN_MAPPINGS.items():
            for possible_name in possible_names:
                if possible_name in available_cols:
                    column_map[possible_name] = standard_name
                    break
        
        # Rename found columns
        if column_map:
            df = df.rename(columns=column_map)
            logger.info(f"Mapped columns: {column_map}")
        
        # Fill in missing columns with defaults
        df = self._fill_missing_columns(df)
        
        return df
    
    def _fill_missing_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fill in missing required columns with intelligent defaults.
        
        Args:
            df: DataFrame with some columns
            
        Returns:
            DataFrame with all required columns
        """
        # Module: use filename or 'unknown'
        if 'module' not in df.columns:
            module_name = self.csv_path.stem
            df['module'] = module_name
            logger.info(f"Added 'module' column with value: {module_name}")
        
        # Test: use TestID or row number
        if 'test' not in df.columns:
            if 'TestID' in df.columns:
                df['test'] = 'test_' + df['TestID'].astype(str)
            else:
                df['test'] = 'test_' + (df.index + 1).astype(str)
            logger.info("Added 'test' column from row numbers")
        
        # Seed: use 1 as default
        if 'seed' not in df.columns:
            df['seed'] = 1
            logger.info("Added 'seed' column with default value: 1")
        
        # Result: map from Status or use PASS
        if 'result' not in df.columns:
            if 'Status' in df.columns:
                df['result'] = df['Status']
            else:
                df['result'] = 'PASS'
            logger.info("Added 'result' column")
        
        # Coverage: look for any coverage-like column
        if 'coverage' not in df.columns:
            cov_cols = [col for col in df.columns if 'cov' in col.lower() or 'coverage' in col.lower()]
            if cov_cols:
                df['coverage'] = df[cov_cols[0]]
                logger.info(f"Mapped coverage from column: {cov_cols[0]}")
            else:
                df['coverage'] = 50.0  # Default coverage
                logger.info("Added 'coverage' column with default value: 50.0")
        
        # Sim_time: use any time-related column or default
        if 'sim_time' not in df.columns:
            time_cols = [col for col in df.columns if 'time' in col.lower() or 'runtime' in col.lower()]
            if time_cols:
                df['sim_time'] = df[time_cols[0]]
                logger.info(f"Mapped sim_time from column: {time_cols[0]}")
            else:
                df['sim_time'] = df.index * 10 + 5  # Incremental time
                logger.info("Added 'sim_time' column with incremental values")
        
        return df
    
    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize and clean loaded data.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Normalized DataFrame
        """
        df = df.copy()
        
        # Ensure all columns are strings for concatenation
        df['module'] = df['module'].astype(str)
        df['test'] = df['test'].astype(str)
        df['seed'] = df['seed'].astype(str)
        
        # Create unique testcase ID
        df['testcase_id'] = df['module'] + '_' + df['test'] + '_seed' + df['seed']
        
        # Normalize result to binary pass/fail
        df['pass_fail'] = df['result'].apply(
            lambda x: 1 if str(x).upper() in ['PASS', 'PASSED', '1', 'TRUE'] else 0
        )
        
        # Ensure numeric types
        df['coverage'] = pd.to_numeric(df['coverage'], errors='coerce')
        df['sim_time'] = pd.to_numeric(df['sim_time'], errors='coerce')
        
        # Handle missing values
        df['coverage'] = df['coverage'].fillna(0)
        df['sim_time'] = df['sim_time'].fillna(0.1)  # Avoid division by zero
        
        # Rename for consistency
        df.rename(columns={
            'module': 'module_name',
            'sim_time': 'runtime_seconds'
        }, inplace=True)
        
        logger.info(f"Normalized {len(df)} records")
        return df

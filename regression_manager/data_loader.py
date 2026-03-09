"""
Data loader module for CSV and log data ingestion.
Handles reading and initial validation of input data sources.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and validates CSV testcase data."""
    
    def __init__(self, csv_path: str):
        """
        Initialize data loader.
        
        Args:
            csv_path: Path to CSV file containing testcase data
        """
        self.csv_path = Path(csv_path)
        
    def load_csv(self) -> pd.DataFrame:
        """
        Load CSV data with validation.
        
        Returns:
            DataFrame with testcase data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If required columns are missing
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        logger.info(f"Loading CSV from {self.csv_path}")
        df = pd.read_csv(self.csv_path)
        
        # Validate required columns
        required_cols = ['module', 'test', 'seed', 'result', 'coverage', 'sim_time']
        missing_cols = set(required_cols) - set(df.columns)
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        logger.info(f"Loaded {len(df)} records from CSV")
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
        
        # Create unique testcase ID
        df['testcase_id'] = df['module'] + '_' + df['test'] + '_seed' + df['seed'].astype(str)
        
        # Normalize result to binary pass/fail
        df['pass_fail'] = df['result'].apply(
            lambda x: 1 if x == 'PASS' else 0
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

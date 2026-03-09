"""
Log parser module for simulation log data extraction.
Parses simulation logs to extract performance metrics.
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

logger = logging.getLogger(__name__)


class LogParser:
    """Parses simulation log files to extract metrics."""
    
    def __init__(self, log_path: str):
        """
        Initialize log parser.
        
        Args:
            log_path: Path to simulation log file
        """
        self.log_path = Path(log_path)
        
    def parse_log(self) -> pd.DataFrame:
        """
        Parse simulation log file.
        
        Returns:
            DataFrame with parsed log metrics
        """
        if not self.log_path.exists():
            logger.warning(f"Log file not found: {self.log_path}")
            return pd.DataFrame()
        
        logger.info(f"Parsing log file: {self.log_path}")
        
        with open(self.log_path, 'r') as f:
            content = f.read()
        
        metrics = self._extract_metrics(content)
        
        if not metrics:
            logger.warning("No metrics extracted from log")
            return pd.DataFrame()
        
        df = pd.DataFrame([metrics])
        logger.info(f"Extracted metrics: {list(metrics.keys())}")
        return df
    
    def _extract_metrics(self, content: str) -> Dict:
        """
        Extract metrics from log content.
        
        Args:
            content: Log file content
            
        Returns:
            Dictionary of extracted metrics
        """
        metrics = {}
        
        # Extract simulation time
        time_match = re.search(r'Time:\s+(\d+)', content)
        if time_match:
            metrics['simulation_time'] = int(time_match.group(1))
        
        # Extract CPU time
        cpu_match = re.search(r'CPU Time:\s+([\d.]+)\s+seconds', content)
        if cpu_match:
            metrics['compile_time'] = float(cpu_match.group(1))
        
        # Extract memory usage
        mem_match = re.search(r'Data structure size:\s+([\d.]+)Mb', content)
        if mem_match:
            metrics['memory_usage'] = float(mem_match.group(1))
        
        # Count errors and warnings
        metrics['error_count'] = len(re.findall(r'UVM_ERROR', content))
        metrics['warning_count'] = len(re.findall(r'UVM_WARNING', content))
        
        # Count PASS/FAIL
        pass_count = len(re.findall(r'\bPASS\b', content))
        fail_count = len(re.findall(r'\bFAIL\b', content))
        
        metrics['pass_count'] = pass_count
        metrics['fail_count'] = fail_count
        
        return metrics
    
    def merge_with_csv(self, csv_df: pd.DataFrame, log_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge log metrics with CSV data.
        
        Args:
            csv_df: DataFrame from CSV
            log_df: DataFrame from log parsing
            
        Returns:
            Merged DataFrame
        """
        if log_df.empty:
            logger.warning("Log DataFrame is empty, skipping merge")
            # Add default columns
            csv_df['compile_time'] = 0.0
            csv_df['memory_usage'] = 0.0
            csv_df['error_count'] = 0
            csv_df['warning_count'] = 0
            return csv_df
        
        # Broadcast log metrics to all rows (assuming single test run)
        for col in log_df.columns:
            csv_df[col] = log_df[col].iloc[0]
        
        logger.info("Merged log metrics with CSV data")
        return csv_df

"""
Redundancy detection module.
Identifies low-value testcases that can be excluded from regression.
"""

import pandas as pd
import logging
from typing import List, Dict

from .config import config

logger = logging.getLogger(__name__)


class RedundancyDetector:
    """Detects redundant testcases based on historical performance."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize redundancy detector.
        
        Args:
            df: DataFrame with feature-engineered testcase data
        """
        self.df = df.copy()
        
    def detect_redundant(self) -> pd.DataFrame:
        """
        Mark redundant testcases.
        
        Returns:
            DataFrame with redundancy flags and reasons
        """
        logger.info("Detecting redundant testcases")
        
        self.df['is_redundant'] = False
        self.df['redundancy_reason'] = ''
        
        # Condition 1: High pass rate
        high_pass_rate = self.df['pass_rate'] > config.redundancy_thresholds.pass_rate_threshold
        
        # Condition 2: Low coverage gain
        low_coverage_gain = self.df['coverage_gain'] < config.redundancy_thresholds.coverage_gain_threshold
        
        # Condition 3: No recent failures
        no_recent_failures = self._check_no_recent_failures()
        
        # Mark as redundant if all conditions met
        redundant_mask = high_pass_rate & low_coverage_gain & no_recent_failures
        
        self.df.loc[redundant_mask, 'is_redundant'] = True
        self.df.loc[redundant_mask, 'redundancy_reason'] = (
            f"Consistently passing (pass_rate > {config.redundancy_thresholds.pass_rate_threshold}), "
            f"low coverage gain (< {config.redundancy_thresholds.coverage_gain_threshold}%), "
            f"no failures in last {config.redundancy_thresholds.no_failure_window} runs"
        )
        
        redundant_count = self.df['is_redundant'].sum()
        logger.info(f"Detected {redundant_count} redundant testcases")
        
        return self.df
    
    def _check_no_recent_failures(self) -> pd.Series:
        """
        Check if testcases have no failures in recent window.
        
        Returns:
            Boolean Series indicating no recent failures
        """
        # For simplified implementation, use pass_rate as proxy
        # In production, would track last N runs explicitly
        window_threshold = 1.0 - (1.0 / config.redundancy_thresholds.no_failure_window)
        
        return self.df['pass_rate'] >= window_threshold
    
    def get_excluded_tests(self) -> List[Dict]:
        """
        Get list of tests to exclude from regression.
        
        Returns:
            List of dictionaries with excluded test info
        """
        excluded = self.df[self.df['is_redundant']].copy()
        
        excluded_list = []
        for _, row in excluded.iterrows():
            excluded_list.append({
                'testcase_id': row['testcase_id'],
                'module_name': row['module_name'],
                'reason': row['redundancy_reason'],
                'pass_rate': float(row['pass_rate']),
                'coverage_gain': float(row['coverage_gain'])
            })
        
        return excluded_list

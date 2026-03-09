"""
Feature engineering module for computing derived metrics.
Transforms raw data into features for scoring.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional

from .config import config

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Computes derived features for regression scoring."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize feature engineer.
        
        Args:
            df: DataFrame with normalized testcase data
        """
        self.df = df.copy()
        
    def compute_features(self) -> pd.DataFrame:
        """
        Compute all derived features.
        
        Returns:
            DataFrame with computed features
        """
        logger.info("Computing features")
        
        self.df = self._compute_coverage_gain()
        self.df = self._compute_efficiency_score()
        self.df = self._compute_stability_metrics()
        self.df = self._compute_failure_rate()
        
        logger.info(f"Feature computation complete. Shape: {self.df.shape}")
        return self.df
    
    def _compute_coverage_gain(self) -> pd.DataFrame:
        """
        Compute coverage gain relative to rolling mean.
        
        Returns:
            DataFrame with coverage_gain column
        """
        # Group by testcase_id to compute rolling statistics
        self.df = self.df.sort_values(['testcase_id', 'runtime_seconds'])
        
        # Compute rolling mean coverage per testcase
        self.df['rolling_mean_coverage'] = self.df.groupby('testcase_id')['coverage'].transform(
            lambda x: x.rolling(window=config.rolling_window_size, min_periods=1).mean()
        )
        
        # Coverage gain = current coverage - rolling mean
        self.df['coverage_gain'] = self.df['coverage'] - self.df['rolling_mean_coverage']
        
        # For first occurrence, use absolute coverage
        self.df['coverage_gain'] = self.df['coverage_gain'].fillna(self.df['coverage'])
        
        logger.debug(f"Coverage gain range: [{self.df['coverage_gain'].min():.2f}, {self.df['coverage_gain'].max():.2f}]")
        return self.df
    
    def _compute_efficiency_score(self) -> pd.DataFrame:
        """
        Compute efficiency score (coverage gain per unit time).
        
        Returns:
            DataFrame with efficiency_score column
        """
        # Avoid division by zero
        runtime_safe = self.df['runtime_seconds'].replace(0, config.min_runtime_seconds)
        
        self.df['efficiency_score'] = self.df['coverage_gain'] / runtime_safe
        
        # Normalize to 0-1 range using min-max scaling
        min_eff = self.df['efficiency_score'].min()
        max_eff = self.df['efficiency_score'].max()
        
        if max_eff > min_eff:
            self.df['efficiency_score_normalized'] = (
                (self.df['efficiency_score'] - min_eff) / (max_eff - min_eff)
            )
        else:
            self.df['efficiency_score_normalized'] = 0.5
        
        logger.debug(f"Efficiency score range: [{min_eff:.4f}, {max_eff:.4f}]")
        return self.df
    
    def _compute_stability_metrics(self) -> pd.DataFrame:
        """
        Compute stability metrics (pass rate).
        
        Returns:
            DataFrame with pass_rate column
        """
        # Compute cumulative pass rate per testcase
        self.df['cumulative_runs'] = self.df.groupby('testcase_id').cumcount() + 1
        self.df['cumulative_passes'] = self.df.groupby('testcase_id')['pass_fail'].cumsum()
        
        self.df['pass_rate'] = self.df['cumulative_passes'] / self.df['cumulative_runs']
        
        logger.debug(f"Pass rate range: [{self.df['pass_rate'].min():.2f}, {self.df['pass_rate'].max():.2f}]")
        return self.df
    
    def _compute_failure_rate(self) -> pd.DataFrame:
        """
        Compute failure rate (inverse of pass rate).
        
        Returns:
            DataFrame with failure_rate column
        """
        self.df['failure_rate'] = 1.0 - self.df['pass_rate']
        
        return self.df
    
    def get_latest_per_testcase(self) -> pd.DataFrame:
        """
        Get latest record for each unique testcase.
        
        Returns:
            DataFrame with one row per testcase
        """
        # Sort by runtime to get latest
        df_sorted = self.df.sort_values(['testcase_id', 'runtime_seconds'])
        
        # Keep last occurrence of each testcase
        df_latest = df_sorted.groupby('testcase_id').tail(1).reset_index(drop=True)
        
        logger.info(f"Extracted {len(df_latest)} unique testcases")
        return df_latest

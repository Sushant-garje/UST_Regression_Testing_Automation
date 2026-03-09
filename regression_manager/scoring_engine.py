"""
Scoring engine module.
Computes final regression scores for testcases.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional

from .config import config

logger = logging.getLogger(__name__)


class ScoringEngine:
    """Computes final regression scores for testcase prioritization."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize scoring engine.
        
        Args:
            df: DataFrame with features and redundancy flags
        """
        self.df = df.copy()
        
    def compute_scores(self) -> pd.DataFrame:
        """
        Compute final regression scores.
        
        Returns:
            DataFrame with final_score column
        """
        logger.info("Computing regression scores")
        
        # Normalize coverage gain to 0-1 range
        coverage_gain_norm = self._normalize_column('coverage_gain')
        
        # Use pre-computed normalized efficiency score
        efficiency_norm = self.df['efficiency_score_normalized']
        
        # Stability component (inverse of failure rate)
        stability_norm = 1.0 - self.df['failure_rate']
        
        # Compute weighted score
        weights = config.scoring_weights
        
        self.df['base_score'] = (
            weights.coverage * coverage_gain_norm +
            weights.efficiency * efficiency_norm +
            weights.stability * stability_norm
        )
        
        # Apply redundancy penalty
        redundancy_penalty = self.df['is_redundant'].astype(float) * config.redundancy_penalty
        
        # Apply critical module boost
        critical_boost = self._compute_critical_boost()
        
        # Final score
        self.df['final_score'] = (self.df['base_score'] - redundancy_penalty) * critical_boost
        
        # Clip to 0-1 range
        self.df['final_score'] = self.df['final_score'].clip(0, 1)
        
        logger.info(f"Score range: [{self.df['final_score'].min():.4f}, {self.df['final_score'].max():.4f}]")
        
        return self.df
    
    def _normalize_column(self, col: str) -> pd.Series:
        """
        Normalize column to 0-1 range using min-max scaling.
        
        Args:
            col: Column name to normalize
            
        Returns:
            Normalized Series
        """
        min_val = self.df[col].min()
        max_val = self.df[col].max()
        
        if max_val > min_val:
            return (self.df[col] - min_val) / (max_val - min_val)
        else:
            return pd.Series(0.5, index=self.df.index)
    
    def _compute_critical_boost(self) -> pd.Series:
        """
        Compute critical module boost multiplier.
        
        Returns:
            Series with boost multipliers
        """
        critical_modules = config.critical_modules.modules
        multiplier = config.critical_modules.critical_weight_multiplier
        
        is_critical = self.df['module_name'].isin(critical_modules)
        
        boost = pd.Series(1.0, index=self.df.index)
        boost[is_critical] = multiplier
        
        critical_count = is_critical.sum()
        logger.info(f"Applied critical boost to {critical_count} testcases")
        
        return boost
    
    def get_score_distribution(self) -> dict:
        """
        Get score distribution statistics.
        
        Returns:
            Dictionary with score statistics
        """
        return {
            'mean': float(self.df['final_score'].mean()),
            'median': float(self.df['final_score'].median()),
            'std': float(self.df['final_score'].std()),
            'min': float(self.df['final_score'].min()),
            'max': float(self.df['final_score'].max()),
            'q25': float(self.df['final_score'].quantile(0.25)),
            'q75': float(self.df['final_score'].quantile(0.75))
        }

"""
Prioritization engine module.
Ranks testcases and generates execution plan.
"""

import pandas as pd
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class PrioritizationEngine:
    """Prioritizes testcases for regression execution."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize prioritization engine.
        
        Args:
            df: DataFrame with final scores
        """
        self.df = df.copy()
        
    def prioritize(self) -> pd.DataFrame:
        """
        Rank testcases by priority.
        
        Returns:
            DataFrame sorted by priority with action labels
        """
        logger.info("Prioritizing testcases")
        
        # Filter out redundant tests
        active_tests = self.df[~self.df['is_redundant']].copy()
        
        # Sort by final score descending
        active_tests = active_tests.sort_values('final_score', ascending=False)
        
        # Assign priority rank
        active_tests['priority_rank'] = range(1, len(active_tests) + 1)
        
        # Assign action labels based on score quartiles
        active_tests['action'] = self._assign_actions(active_tests)
        
        logger.info(f"Prioritized {len(active_tests)} active testcases")
        
        return active_tests
    
    def _assign_actions(self, df: pd.DataFrame) -> pd.Series:
        """
        Assign action labels based on score distribution.
        
        Args:
            df: DataFrame with scores
            
        Returns:
            Series with action labels
        """
        q75 = df['final_score'].quantile(0.75)
        q50 = df['final_score'].quantile(0.50)
        q25 = df['final_score'].quantile(0.25)
        
        actions = pd.Series('run_normal', index=df.index)
        
        actions[df['final_score'] >= q75] = 'run_first'
        actions[(df['final_score'] >= q50) & (df['final_score'] < q75)] = 'run_early'
        actions[(df['final_score'] >= q25) & (df['final_score'] < q50)] = 'run_normal'
        actions[df['final_score'] < q25] = 'run_late'
        
        return actions
    
    def get_ranked_tests(self, df_prioritized: pd.DataFrame) -> List[Dict]:
        """
        Get ranked test list for output.
        
        Args:
            df_prioritized: Prioritized DataFrame with rankings
        
        Returns:
            List of dictionaries with ranked test info
        """
        ranked = []
        
        for _, row in df_prioritized.iterrows():
            ranked.append({
                'testcase_id': row['testcase_id'],
                'module_name': row['module_name'],
                'score': float(row['final_score']),
                'priority_rank': int(row['priority_rank']),
                'action': row['action'],
                'coverage': float(row['coverage']),
                'runtime_seconds': float(row['runtime_seconds']),
                'pass_rate': float(row['pass_rate'])
            })
        
        return ranked
    
    def get_execution_plan(self) -> Dict:
        """
        Generate execution plan summary.
        
        Returns:
            Dictionary with execution plan details
        """
        action_counts = self.df['action'].value_counts().to_dict()
        
        total_runtime = self.df['runtime_seconds'].sum()
        avg_coverage = self.df['coverage'].mean()
        
        return {
            'total_tests': len(self.df),
            'action_distribution': action_counts,
            'estimated_total_runtime': float(total_runtime),
            'average_coverage': float(avg_coverage),
            'high_priority_tests': len(self.df[self.df['action'] == 'run_first'])
        }

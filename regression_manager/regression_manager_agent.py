"""
Main Regression Manager Agent.
Orchestrates the complete regression optimization workflow.
"""

import pandas as pd
import logging
from typing import Dict, Optional
from pathlib import Path

from .data_loader import DataLoader
from .log_parser import LogParser
from .feature_engineering import FeatureEngineer
from .redundancy_detector import RedundancyDetector
from .scoring_engine import ScoringEngine
from .prioritization_engine import PrioritizationEngine

logger = logging.getLogger(__name__)


class RegressionManagerAgent:
    """
    Main agent for regression test optimization.
    
    Orchestrates data loading, feature engineering, scoring,
    redundancy detection, and prioritization.
    """
    
    def __init__(self, csv_path: str, log_path: Optional[str] = None):
        """
        Initialize regression manager agent.
        
        Args:
            csv_path: Path to CSV testcase data
            log_path: Optional path to simulation log file
        """
        self.csv_path = csv_path
        self.log_path = log_path
        self.df = None
        self.ranked_tests = None
        self.excluded_tests = None
        
    def run(self) -> Dict:
        """
        Execute complete regression optimization workflow.
        
        Returns:
            Dictionary with optimization results
        """
        logger.info("Starting Regression Manager Agent")
        
        # Step 1: Load and normalize data
        df = self._load_data()
        
        # Step 2: Feature engineering
        df = self._engineer_features(df)
        
        # Step 3: Detect redundancy
        df = self._detect_redundancy(df)
        
        # Step 4: Compute scores
        df = self._compute_scores(df)
        
        # Step 5: Prioritize tests
        df_prioritized = self._prioritize_tests(df)
        
        # Step 6: Generate output
        result = self._generate_output(df_prioritized, df)
        
        logger.info("Regression Manager Agent completed successfully")
        
        return result
    
    def _load_data(self) -> pd.DataFrame:
        """Load and merge CSV and log data."""
        logger.info("Loading data")
        
        # Load CSV
        loader = DataLoader(self.csv_path)
        df = loader.load_csv()
        df = loader.normalize_data(df)
        
        # Parse and merge log if provided
        if self.log_path:
            parser = LogParser(self.log_path)
            log_df = parser.parse_log()
            df = parser.merge_with_csv(df, log_df)
        
        return df
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute derived features."""
        logger.info("Engineering features")
        
        engineer = FeatureEngineer(df)
        df = engineer.compute_features()
        
        # Get latest per testcase for scoring
        df = engineer.get_latest_per_testcase()
        
        return df
    
    def _detect_redundancy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect redundant testcases."""
        logger.info("Detecting redundancy")
        
        detector = RedundancyDetector(df)
        df = detector.detect_redundant()
        
        self.excluded_tests = detector.get_excluded_tests()
        
        return df
    
    def _compute_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute final regression scores."""
        logger.info("Computing scores")
        
        scorer = ScoringEngine(df)
        df = scorer.compute_scores()
        
        return df
    
    def _prioritize_tests(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prioritize testcases for execution."""
        logger.info("Prioritizing tests")
        
        prioritizer = PrioritizationEngine(df)
        df_prioritized = prioritizer.prioritize()
        
        self.ranked_tests = prioritizer.get_ranked_tests(df_prioritized)
        
        return df_prioritized
    
    def _generate_output(self, df_prioritized: pd.DataFrame, df_all: pd.DataFrame) -> Dict:
        """Generate final output structure."""
        logger.info("Generating output")
        
        total_tests = len(df_all)
        selected_tests = len(df_prioritized)
        excluded_tests = len(self.excluded_tests)
        
        result = {
            'ranked_tests': self.ranked_tests,
            'excluded_tests': self.excluded_tests,
            'summary': {
                'total_tests': total_tests,
                'selected': selected_tests,
                'excluded': excluded_tests,
                'optimization_ratio': round(selected_tests / total_tests, 2) if total_tests > 0 else 0
            }
        }
        
        return result

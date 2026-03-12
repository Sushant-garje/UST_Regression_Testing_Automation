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
from .load_optimizer import LoadOptimizer
from .coverage_parser import CoverageParser
from .llm_copilot import RegressionCopilot

logger = logging.getLogger(__name__)


class RegressionManagerAgent:
    """
    Main agent for regression test optimization.
    
    Orchestrates data loading, feature engineering, scoring,
    redundancy detection, and prioritization.
    """
    
    def __init__(self, csv_path: str, log_path: Optional[str] = None, 
                 coverage_report_path: Optional[str] = None,
                 enable_load_optimizer: bool = True,
                 enable_llm_copilot: bool = False,
                 llm_api_key: Optional[str] = None):
        """
        Initialize regression manager agent.
        
        Args:
            csv_path: Path to CSV testcase data
            log_path: Optional path to simulation log file
            coverage_report_path: Optional path to coverage report
            enable_load_optimizer: Enable resource load optimization
            enable_llm_copilot: Enable LLM-powered copilot
            llm_api_key: API key for LLM provider
        """
        self.csv_path = csv_path
        self.log_path = log_path
        self.coverage_report_path = coverage_report_path
        self.enable_load_optimizer = enable_load_optimizer
        self.enable_llm_copilot = enable_llm_copilot
        
        self.df = None
        self.ranked_tests = None
        self.excluded_tests = None
        self.resource_allocation = None
        self.coverage_data = None
        
        # Initialize optional components
        if enable_load_optimizer:
            self.load_optimizer = LoadOptimizer()
        else:
            self.load_optimizer = None
            
        if enable_llm_copilot:
            self.copilot = RegressionCopilot(api_key=llm_api_key)
        else:
            self.copilot = None
        
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
        
        # --- Select top tests by high coverage and min runtime to achieve >50% optimization ratio ---
        if 'coverage' in df_prioritized.columns and 'runtime_seconds' in df_prioritized.columns:
            total_tests = len(df_prioritized)
            min_selected = max(1, int(0.5 * total_tests))
            # Sort by coverage (desc), then runtime (asc)
            df_sorted = df_prioritized.sort_values(['coverage', 'runtime_seconds'], ascending=[False, True])
            df_selected = df_sorted.head(min_selected)
            # Save selected tests to CSV
            df_selected.to_csv('selected_testcases.csv', index=False)
        else:
            df_selected = df_prioritized
        
        # Step 6: Parse coverage reports (if available)
        if self.coverage_report_path:
            self.coverage_data = self._parse_coverage()
        
        # Step 7: Optimize resource allocation (if enabled)
        if self.enable_load_optimizer and self.load_optimizer:
            df_selected = self._optimize_resources(df_selected)
        
        # Step 8: Generate output
        result = self._generate_output(df_selected, df)
        
        # Step 9: LLM analysis (if enabled)
        if self.enable_llm_copilot and self.copilot:
            result['llm_insights'] = self.copilot.analyze_regression_results(result)
        
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
    
    def _parse_coverage(self) -> Dict:
        """Parse coverage reports."""
        logger.info("Parsing coverage reports")
        
        parser = CoverageParser(self.coverage_report_path)
        coverage_data = parser.parse()
        
        return coverage_data
    
    def _optimize_resources(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize resource allocation."""
        logger.info("Optimizing resource allocation")
        
        df_with_resources = self.load_optimizer.allocate_tests(df)
        self.resource_allocation = {
            'server_usage': self.load_optimizer.get_server_usage_report().to_dict('records'),
            'cost_estimate': self.load_optimizer.estimate_cost()
        }
        
        return df_with_resources
    
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
        
        # Add resource allocation if available
        if self.resource_allocation:
            result['resource_allocation'] = self.resource_allocation
        
        # Add coverage data if available
        if self.coverage_data:
            result['coverage_analysis'] = self.coverage_data
        
        return result

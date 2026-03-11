"""
Gemini-powered Regression Manager Agent.
Uses Google Gemini AI for intelligent test selection, redundancy detection, and prioritization.
"""

import logging
import json
from typing import Dict, List, Optional
import pandas as pd
from dotenv import load_dotenv

from .llm_copilot import RegressionCopilot
from .data_loader import DataLoader
from .log_parser import LogParser
from .feature_engineering import FeatureEngineer

load_dotenv()
logger = logging.getLogger(__name__)


class GeminiRegressionAgent:
    """
    AI-powered Regression Manager using Google Gemini.
    
    Gemini makes decisions on:
    1. Which tests give most coverage
    2. Which tests to exclude (consistently passing)
    3. How to prioritize critical path tests
    """
    
    def __init__(self, csv_path: str, log_path: Optional[str] = None):
        """
        Initialize Gemini-powered regression agent.
        
        Args:
            csv_path: Path to CSV testcase data
            log_path: Optional path to simulation log
        """
        self.csv_path = csv_path
        self.log_path = log_path
        
        # Initialize Gemini copilot
        self.copilot = RegressionCopilot()
        
        if not self.copilot.model:
            logger.warning("Gemini not available. Using fallback mode.")
        else:
            logger.info(f"Gemini-powered agent initialized with {self.copilot.model_name}")
    
    def analyze_and_optimize(self) -> Dict:
        """
        Use Gemini to analyze tests and make optimization decisions.
        
        Returns:
            Dictionary with Gemini's recommendations
        """
        logger.info("Starting Gemini-powered regression analysis")
        
        # Step 1: Load and prepare data
        df = self._load_and_prepare_data()
        
        # Step 2: Ask Gemini to analyze the test suite
        analysis = self._gemini_analyze_test_suite(df)
        
        # Step 3: Ask Gemini to identify high-coverage tests
        high_coverage_tests = self._gemini_find_high_coverage_tests(df, analysis)
        
        # Step 4: Ask Gemini to identify redundant tests
        redundant_tests = self._gemini_find_redundant_tests(df, analysis)
        
        # Step 5: Ask Gemini to prioritize critical path tests
        prioritized_tests = self._gemini_prioritize_critical_tests(df, analysis)
        
        # Step 6: Generate final recommendations
        result = self._generate_recommendations(
            df, high_coverage_tests, redundant_tests, prioritized_tests, analysis
        )
        
        logger.info("Gemini analysis complete")
        return result
    
    def _load_and_prepare_data(self) -> pd.DataFrame:
        """Load and prepare test data."""
        logger.info("Loading test data")
        
        # Load CSV
        loader = DataLoader(self.csv_path)
        df = loader.load_csv()
        df = loader.normalize_data(df)
        
        # Parse log if available
        if self.log_path:
            parser = LogParser(self.log_path)
            log_df = parser.parse_log()
            df = parser.merge_with_csv(df, log_df)
        
        # Compute features
        engineer = FeatureEngineer(df)
        df = engineer.compute_features()
        df = engineer.get_latest_per_testcase()
        
        return df
    
    def _gemini_analyze_test_suite(self, df: pd.DataFrame) -> Dict:
        """
        Ask Gemini to analyze the overall test suite.
        
        Args:
            df: Test data
            
        Returns:
            Gemini's analysis
        """
        if not self.copilot.model:
            return self._fallback_analysis(df)
        
        # Prepare data summary for Gemini
        summary = {
            'total_tests': len(df),
            'modules': df['module_name'].unique().tolist(),
            'coverage_range': {
                'min': float(df['coverage'].min()),
                'max': float(df['coverage'].max()),
                'mean': float(df['coverage'].mean())
            },
            'runtime_range': {
                'min': float(df['runtime_seconds'].min()),
                'max': float(df['runtime_seconds'].max()),
                'mean': float(df['runtime_seconds'].mean())
            },
            'pass_rate_range': {
                'min': float(df['pass_rate'].min()),
                'max': float(df['pass_rate'].max()),
                'mean': float(df['pass_rate'].mean())
            }
        }
        
        prompt = f"""
You are a VLSI verification expert analyzing a regression test suite.

Test Suite Summary:
{json.dumps(summary, indent=2)}

Sample Tests (first 5):
{df[['testcase_id', 'module_name', 'coverage', 'runtime_seconds', 'pass_rate']].head().to_string()}

Analyze this test suite and provide:
1. Overall quality assessment
2. Key patterns you observe
3. Potential issues or concerns
4. Recommendations for optimization

Respond in JSON format:
{{
    "quality_score": <0-100>,
    "key_patterns": ["pattern1", "pattern2", ...],
    "concerns": ["concern1", "concern2", ...],
    "recommendations": ["rec1", "rec2", ...]
}}
"""
        
        try:
            response = self.copilot._call_llm(prompt, "You are a VLSI verification expert.")
            logger.info(f"Gemini response received (length: {len(response)})")
            logger.debug(f"Response preview: {response[:500]}")
            # Extract JSON from response
            analysis = self._extract_json_from_response(response)
            if not analysis:
                logger.warning("Empty analysis from Gemini, using fallback")
                return self._fallback_analysis(df)
            return analysis
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return self._fallback_analysis(df)
    
    def _gemini_find_high_coverage_tests(self, df: pd.DataFrame, analysis: Dict) -> List[str]:
        """
        Ask Gemini to identify tests that give most coverage.
        
        Args:
            df: Test data
            analysis: Previous analysis
            
        Returns:
            List of high-coverage test IDs
        """
        if not self.copilot.model:
            return self._fallback_high_coverage(df)
        
        # Prepare test data for Gemini
        test_data = df[['testcase_id', 'module_name', 'coverage', 'coverage_gain', 
                        'runtime_seconds', 'efficiency_score_normalized']].to_dict('records')
        
        prompt = f"""
You are a VLSI verification expert selecting tests for maximum coverage.

Previous Analysis:
{json.dumps(analysis, indent=2)}

All Tests:
{json.dumps(test_data[:20], indent=2)}  # First 20 for context

Your task: Identify tests that give the MOST coverage value.

Consider:
1. Absolute coverage percentage
2. Coverage gain (incremental value)
3. Efficiency (coverage per unit time)
4. Module importance

Respond with JSON:
{{
    "high_coverage_tests": ["test_id1", "test_id2", ...],
    "reasoning": "Why these tests were selected"
}}

Select the top 30-40% of tests that provide maximum coverage value.
"""
        
        try:
            response = self.copilot._call_llm(prompt, "You are a VLSI verification expert.")
            result = self._extract_json_from_response(response)
            return result.get('high_coverage_tests', [])
        except Exception as e:
            logger.error(f"Gemini high-coverage selection failed: {e}")
            return self._fallback_high_coverage(df)
    
    def _gemini_find_redundant_tests(self, df: pd.DataFrame, analysis: Dict) -> List[Dict]:
        """
        Ask Gemini to identify consistently passing tests to exclude.
        
        Args:
            df: Test data
            analysis: Previous analysis
            
        Returns:
            List of redundant tests with reasons
        """
        if not self.copilot.model:
            return self._fallback_redundant(df)
        
        # Prepare test data
        test_data = df[['testcase_id', 'module_name', 'coverage', 'coverage_gain',
                        'pass_rate', 'failure_rate', 'runtime_seconds']].to_dict('records')
        
        prompt = f"""
You are a VLSI verification expert identifying redundant tests.

Previous Analysis:
{json.dumps(analysis, indent=2)}

All Tests:
{json.dumps(test_data[:20], indent=2)}

Your task: Identify tests that are CONSISTENTLY PASSING and provide LOW VALUE.

Criteria for redundancy:
1. Very high pass rate (>95%)
2. Low coverage gain (<1-2%)
3. Long runtime with minimal value
4. Duplicate coverage of other tests

Respond with JSON:
{{
    "redundant_tests": [
        {{
            "testcase_id": "test_id",
            "reason": "Why this test is redundant"
        }},
        ...
    ],
    "exclusion_summary": "Overall reasoning for exclusions"
}}

Be conservative - only exclude truly redundant tests.
"""
        
        try:
            response = self.copilot._call_llm(prompt, "You are a VLSI verification expert.")
            result = self._extract_json_from_response(response)
            return result.get('redundant_tests', [])
        except Exception as e:
            logger.error(f"Gemini redundancy detection failed: {e}")
            return self._fallback_redundant(df)
    
    def _gemini_prioritize_critical_tests(self, df: pd.DataFrame, analysis: Dict) -> List[Dict]:
        """
        Ask Gemini to prioritize critical path tests.
        
        Args:
            df: Test data
            analysis: Previous analysis
            
        Returns:
            List of prioritized tests with priority levels
        """
        if not self.copilot.model:
            return self._fallback_prioritize(df)
        
        # Prepare test data
        test_data = df[['testcase_id', 'module_name', 'coverage', 'runtime_seconds',
                        'pass_rate', 'failure_rate']].to_dict('records')
        
        prompt = f"""
You are a VLSI verification expert prioritizing critical path tests.

Previous Analysis:
{json.dumps(analysis, indent=2)}

All Tests:
{json.dumps(test_data[:20], indent=2)}

Your task: PRIORITIZE tests for regression execution.

Priority Criteria:
1. CRITICAL PATH: Tests for core functionality (CPU, memory, interrupts)
2. HIGH FAILURE RATE: Tests that catch bugs frequently
3. HIGH COVERAGE: Tests that cover important code paths
4. FAST EXECUTION: Quick tests for early feedback

Assign priority levels:
- P0 (Critical): Must run first, core functionality
- P1 (High): Important tests, run early
- P2 (Medium): Standard regression tests
- P3 (Low): Nice to have, run if time permits

Respond with JSON:
{{
    "prioritized_tests": [
        {{
            "testcase_id": "test_id",
            "priority": "P0|P1|P2|P3",
            "reason": "Why this priority"
        }},
        ...
    ],
    "prioritization_strategy": "Overall strategy explanation"
}}
"""
        
        try:
            response = self.copilot._call_llm(prompt, "You are a VLSI verification expert.")
            result = self._extract_json_from_response(response)
            return result.get('prioritized_tests', [])
        except Exception as e:
            logger.error(f"Gemini prioritization failed: {e}")
            return self._fallback_prioritize(df)
    
    def _generate_recommendations(self, df: pd.DataFrame, high_coverage: List[str],
                                  redundant: List[Dict], prioritized: List[Dict],
                                  analysis: Dict) -> Dict:
        """Generate final recommendations based on Gemini's analysis."""
        
        # Create sets for easy lookup
        high_coverage_set = set(high_coverage)
        redundant_set = set([t['testcase_id'] for t in redundant])
        
        # Build priority map
        priority_map = {t['testcase_id']: t for t in prioritized}
        
        # Generate ranked tests (high coverage, not redundant)
        ranked_tests = []
        for _, row in df.iterrows():
            test_id = row['testcase_id']
            
            if test_id in redundant_set:
                continue  # Skip redundant tests
            
            priority_info = priority_map.get(test_id, {})
            priority = priority_info.get('priority', 'P2')
            
            ranked_tests.append({
                'testcase_id': test_id,
                'module_name': row['module_name'],
                'coverage': float(row['coverage']),
                'runtime_seconds': float(row['runtime_seconds']),
                'pass_rate': float(row['pass_rate']),
                'priority': priority,
                'high_coverage': test_id in high_coverage_set,
                'gemini_reason': priority_info.get('reason', 'Standard test')
            })
        
        # Sort by priority (P0 > P1 > P2 > P3)
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        ranked_tests.sort(key=lambda x: priority_order.get(x['priority'], 2))
        
        # Generate result
        result = {
            'gemini_analysis': analysis,
            'ranked_tests': ranked_tests,
            'excluded_tests': redundant,
            'summary': {
                'total_tests': len(df),
                'selected': len(ranked_tests),
                'excluded': len(redundant),
                'high_coverage_tests': len([t for t in ranked_tests if t['high_coverage']]),
                'critical_tests': len([t for t in ranked_tests if t['priority'] == 'P0']),
                'optimization_ratio': round(len(ranked_tests) / len(df), 2) if len(df) > 0 else 0
            }
        }
        
        return result
    
    def _extract_json_from_response(self, response: str) -> Dict:
        """Extract JSON from Gemini's response."""
        try:
            logger.debug(f"Full response length: {len(response)}")
            logger.debug(f"First 500 chars: {response[:500]}")
            logger.debug(f"Last 200 chars: {response[-200:]}")
            
            # Remove markdown code blocks if present
            cleaned = response.replace('```json', '').replace('```', '').strip()
            
            # Try to find JSON in response - handle multi-line JSON
            start = cleaned.find('{')
            end = cleaned.rfind('}') + 1
            
            logger.debug(f"JSON boundaries: start={start}, end={end}")
            
            if start >= 0 and end > start:
                json_str = cleaned[start:end]
                logger.debug(f"Extracted JSON length: {len(json_str)}")
                # Clean up the JSON string - remove extra whitespace but preserve structure
                result = json.loads(json_str)
                logger.info(f"✅ Successfully extracted JSON with keys: {list(result.keys())}")
                return result
            else:
                # No JSON found, log the response for debugging
                logger.warning(f"❌ No JSON found. Response length: {len(response)}, preview: {response[:300]}")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error: {e}")
            logger.error(f"Attempted to parse: {json_str[:500] if 'json_str' in locals() else 'N/A'}")
            return {}
        except Exception as e:
            logger.error(f"❌ Failed to extract JSON: {e}")
            return {}
    
    def _fallback_analysis(self, df: pd.DataFrame) -> Dict:
        """Fallback analysis without Gemini."""
        return {
            'quality_score': 75,
            'key_patterns': ['Mixed coverage levels', 'Varying runtimes'],
            'concerns': ['Some tests may be redundant'],
            'recommendations': ['Review high pass-rate tests', 'Optimize long-running tests']
        }
    
    def _fallback_high_coverage(self, df: pd.DataFrame) -> List[str]:
        """Fallback high-coverage selection."""
        # Select top 40% by coverage
        threshold = df['coverage'].quantile(0.60)
        return df[df['coverage'] >= threshold]['testcase_id'].tolist()
    
    def _fallback_redundant(self, df: pd.DataFrame) -> List[Dict]:
        """Fallback redundancy detection."""
        redundant = df[(df['pass_rate'] > 0.95) & (df['coverage_gain'] < 1.0)]
        return [
            {
                'testcase_id': row['testcase_id'],
                'reason': f"High pass rate ({row['pass_rate']:.2%}), low coverage gain ({row['coverage_gain']:.2f}%)"
            }
            for _, row in redundant.iterrows()
        ]
    
    def _fallback_prioritize(self, df: pd.DataFrame) -> List[Dict]:
        """Fallback prioritization."""
        prioritized = []
        for _, row in df.iterrows():
            # Simple heuristic
            if row['failure_rate'] > 0.2:
                priority = 'P0'
            elif row['coverage'] > 90:
                priority = 'P1'
            elif row['coverage'] > 70:
                priority = 'P2'
            else:
                priority = 'P3'
            
            prioritized.append({
                'testcase_id': row['testcase_id'],
                'priority': priority,
                'reason': 'Rule-based prioritization'
            })
        
        return prioritized

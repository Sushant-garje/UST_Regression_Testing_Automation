"""
Unit tests for scoring engine.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from regression_manager.scoring_engine import ScoringEngine
from regression_manager.config import config


def test_score_computation():
    """Test basic score computation."""
    data = {
        'testcase_id': ['test1', 'test2', 'test3'],
        'module_name': ['mod1', 'mod2', 'mod3'],
        'coverage_gain': [10.0, 5.0, 15.0],
        'efficiency_score_normalized': [0.8, 0.5, 0.9],
        'failure_rate': [0.1, 0.3, 0.05],
        'is_redundant': [False, False, False],
        'coverage': [95.0, 85.0, 98.0],
        'runtime_seconds': [10, 20, 15]
    }
    df = pd.DataFrame(data)
    
    scorer = ScoringEngine(df)
    result = scorer.compute_scores()
    
    # Check that scores are computed
    assert 'final_score' in result.columns
    assert 'base_score' in result.columns
    
    # Scores should be in 0-1 range
    assert result['final_score'].min() >= 0
    assert result['final_score'].max() <= 1
    
    # test3 should have highest score (highest coverage gain, lowest failure rate)
    assert result.loc[result['testcase_id'] == 'test3', 'final_score'].iloc[0] > \
           result.loc[result['testcase_id'] == 'test1', 'final_score'].iloc[0]


def test_redundancy_penalty():
    """Test that redundant tests get penalized."""
    data = {
        'testcase_id': ['test1', 'test2'],
        'module_name': ['mod1', 'mod2'],
        'coverage_gain': [10.0, 10.0],
        'efficiency_score_normalized': [0.8, 0.8],
        'failure_rate': [0.1, 0.1],
        'is_redundant': [True, False],
        'coverage': [95.0, 95.0],
        'runtime_seconds': [10, 10]
    }
    df = pd.DataFrame(data)
    
    scorer = ScoringEngine(df)
    result = scorer.compute_scores()
    
    # Redundant test should have lower score
    redundant_score = result.loc[result['testcase_id'] == 'test1', 'final_score'].iloc[0]
    normal_score = result.loc[result['testcase_id'] == 'test2', 'final_score'].iloc[0]
    
    assert redundant_score < normal_score


def test_critical_module_boost():
    """Test critical module boost."""
    # Set critical modules
    config.critical_modules.modules = ['critical_mod']
    
    data = {
        'testcase_id': ['test1', 'test2'],
        'module_name': ['critical_mod', 'normal_mod'],
        'coverage_gain': [10.0, 10.0],
        'efficiency_score_normalized': [0.8, 0.8],
        'failure_rate': [0.1, 0.1],
        'is_redundant': [False, False],
        'coverage': [95.0, 95.0],
        'runtime_seconds': [10, 10]
    }
    df = pd.DataFrame(data)
    
    scorer = ScoringEngine(df)
    result = scorer.compute_scores()
    
    # Critical module test should have higher score
    critical_score = result.loc[result['testcase_id'] == 'test1', 'final_score'].iloc[0]
    normal_score = result.loc[result['testcase_id'] == 'test2', 'final_score'].iloc[0]
    
    assert critical_score > normal_score


def test_score_distribution():
    """Test score distribution statistics."""
    data = {
        'testcase_id': ['test1', 'test2', 'test3'],
        'module_name': ['mod1', 'mod2', 'mod3'],
        'coverage_gain': [10.0, 5.0, 15.0],
        'efficiency_score_normalized': [0.8, 0.5, 0.9],
        'failure_rate': [0.1, 0.3, 0.05],
        'is_redundant': [False, False, False],
        'coverage': [95.0, 85.0, 98.0],
        'runtime_seconds': [10, 20, 15]
    }
    df = pd.DataFrame(data)
    
    scorer = ScoringEngine(df)
    scorer.compute_scores()
    stats = scorer.get_score_distribution()
    
    # Check that all statistics are present
    assert 'mean' in stats
    assert 'median' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert 'q25' in stats
    assert 'q75' in stats


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

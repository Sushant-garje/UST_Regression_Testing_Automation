"""
Unit tests for redundancy detector.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from regression_manager.redundancy_detector import RedundancyDetector
from regression_manager.config import config


def test_redundancy_detection_high_pass_rate():
    """Test redundancy detection for high pass rate tests."""
    # Create test data
    data = {
        'testcase_id': ['test1', 'test2', 'test3'],
        'module_name': ['mod1', 'mod2', 'mod3'],
        'pass_rate': [0.98, 0.85, 0.96],
        'coverage_gain': [0.5, 5.0, 0.8],
        'coverage': [95.0, 90.0, 92.0],
        'runtime_seconds': [10, 15, 12]
    }
    df = pd.DataFrame(data)
    
    detector = RedundancyDetector(df)
    result = detector.detect_redundant()
    
    # test1 should be redundant (high pass rate + low coverage gain)
    assert result.loc[result['testcase_id'] == 'test1', 'is_redundant'].iloc[0] == True
    
    # test2 should not be redundant (high coverage gain)
    assert result.loc[result['testcase_id'] == 'test2', 'is_redundant'].iloc[0] == False
    
    # test3 should be redundant (high pass rate + low coverage gain)
    assert result.loc[result['testcase_id'] == 'test3', 'is_redundant'].iloc[0] == True


def test_redundancy_detection_low_pass_rate():
    """Test that low pass rate tests are not marked redundant."""
    data = {
        'testcase_id': ['test1'],
        'module_name': ['mod1'],
        'pass_rate': [0.70],
        'coverage_gain': [0.5],
        'coverage': [95.0],
        'runtime_seconds': [10]
    }
    df = pd.DataFrame(data)
    
    detector = RedundancyDetector(df)
    result = detector.detect_redundant()
    
    # Should not be redundant due to low pass rate
    assert result['is_redundant'].iloc[0] == False


def test_get_excluded_tests():
    """Test excluded tests extraction."""
    data = {
        'testcase_id': ['test1', 'test2'],
        'module_name': ['mod1', 'mod2'],
        'pass_rate': [0.98, 0.85],
        'coverage_gain': [0.5, 5.0],
        'coverage': [95.0, 90.0],
        'runtime_seconds': [10, 15]
    }
    df = pd.DataFrame(data)
    
    detector = RedundancyDetector(df)
    detector.detect_redundant()
    excluded = detector.get_excluded_tests()
    
    # Should have at least one excluded test
    assert len(excluded) >= 1
    assert 'testcase_id' in excluded[0]
    assert 'reason' in excluded[0]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

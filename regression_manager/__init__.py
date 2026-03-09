"""
Regression Manager Agent - Production-grade regression test optimization.
"""

from .regression_manager_agent import RegressionManagerAgent
from .config import config, RegressionConfig

__version__ = '1.0.0'
__all__ = ['RegressionManagerAgent', 'config', 'RegressionConfig']

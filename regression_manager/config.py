"""
Configuration module for Regression Manager Agent.
Centralized configuration for all scoring weights and thresholds.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ScoringWeights:
    """Weights for final regression score calculation."""
    coverage: float = 0.4
    efficiency: float = 0.3
    stability: float = 0.3
    

@dataclass
class RedundancyThresholds:
    """Thresholds for redundancy detection."""
    pass_rate_threshold: float = 0.95
    coverage_gain_threshold: float = 1.0  # percentage
    no_failure_window: int = 10  # last N runs


@dataclass
class CriticalModules:
    """Critical module configuration."""
    modules: List[str] = None
    critical_weight_multiplier: float = 1.5
    
    def __post_init__(self):
        if self.modules is None:
            self.modules = [
                "cpu_core",
                "memory_controller",
                "cache_controller",
                "interrupt_handler",
                "bus_arbiter"
            ]


@dataclass
class RegressionConfig:
    """Master configuration for regression manager."""
    scoring_weights: ScoringWeights = None
    redundancy_thresholds: RedundancyThresholds = None
    critical_modules: CriticalModules = None
    
    # General settings
    min_runtime_seconds: float = 0.1
    redundancy_penalty: float = 0.5
    rolling_window_size: int = 5
    
    def __post_init__(self):
        if self.scoring_weights is None:
            self.scoring_weights = ScoringWeights()
        if self.redundancy_thresholds is None:
            self.redundancy_thresholds = RedundancyThresholds()
        if self.critical_modules is None:
            self.critical_modules = CriticalModules()


# Global configuration instance
config = RegressionConfig()

"""
Coverage report parser for code and functional coverage analysis.
Parses various coverage report formats (VCS, Questa, etc.)
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

logger = logging.getLogger(__name__)


class CoverageParser:
    """Parses coverage reports from various EDA tools."""
    
    def __init__(self, report_path: str, report_type: str = 'auto'):
        """
        Initialize coverage parser.
        
        Args:
            report_path: Path to coverage report file
            report_type: Type of report ('vcs', 'questa', 'xcelium', 'auto')
        """
        self.report_path = Path(report_path)
        self.report_type = report_type
        
    def parse(self) -> Dict:
        """
        Parse coverage report.
        
        Returns:
            Dictionary with coverage metrics
        """
        if not self.report_path.exists():
            logger.warning(f"Coverage report not found: {self.report_path}")
            return {}
        
        logger.info(f"Parsing coverage report: {self.report_path}")
        
        with open(self.report_path, 'r') as f:
            content = f.read()
        
        if self.report_type == 'auto':
            self.report_type = self._detect_report_type(content)
        
        if self.report_type == 'vcs':
            return self._parse_vcs_report(content)
        elif self.report_type == 'questa':
            return self._parse_questa_report(content)
        elif self.report_type == 'xcelium':
            return self._parse_xcelium_report(content)
        else:
            return self._parse_generic_report(content)
    
    def _detect_report_type(self, content: str) -> str:
        """Detect coverage report type from content."""
        if 'VCS' in content or 'Synopsys' in content:
            return 'vcs'
        elif 'Questa' in content or 'ModelSim' in content:
            return 'questa'
        elif 'Xcelium' in content or 'Cadence' in content:
            return 'xcelium'
        return 'generic'
    
    def _parse_vcs_report(self, content: str) -> Dict:
        """Parse VCS coverage report."""
        coverage = {}
        
        # Line coverage
        line_match = re.search(r'Line Coverage\s*:\s*([\d.]+)%', content)
        if line_match:
            coverage['line_coverage'] = float(line_match.group(1))
        
        # Branch coverage
        branch_match = re.search(r'Branch Coverage\s*:\s*([\d.]+)%', content)
        if branch_match:
            coverage['branch_coverage'] = float(branch_match.group(1))
        
        # Toggle coverage
        toggle_match = re.search(r'Toggle Coverage\s*:\s*([\d.]+)%', content)
        if toggle_match:
            coverage['toggle_coverage'] = float(toggle_match.group(1))
        
        # FSM coverage
        fsm_match = re.search(r'FSM Coverage\s*:\s*([\d.]+)%', content)
        if fsm_match:
            coverage['fsm_coverage'] = float(fsm_match.group(1))
        
        # Functional coverage
        func_match = re.search(r'Functional Coverage\s*:\s*([\d.]+)%', content)
        if func_match:
            coverage['functional_coverage'] = float(func_match.group(1))
        
        # Overall coverage
        overall_match = re.search(r'Overall Coverage\s*:\s*([\d.]+)%', content)
        if overall_match:
            coverage['overall_coverage'] = float(overall_match.group(1))
        
        return coverage
    
    def _parse_questa_report(self, content: str) -> Dict:
        """Parse Questa coverage report."""
        coverage = {}
        
        # Statement coverage
        stmt_match = re.search(r'Statement\s+Coverage\s*=\s*([\d.]+)%', content)
        if stmt_match:
            coverage['statement_coverage'] = float(stmt_match.group(1))
        
        # Branch coverage
        branch_match = re.search(r'Branch\s+Coverage\s*=\s*([\d.]+)%', content)
        if branch_match:
            coverage['branch_coverage'] = float(branch_match.group(1))
        
        # Condition coverage
        cond_match = re.search(r'Condition\s+Coverage\s*=\s*([\d.]+)%', content)
        if cond_match:
            coverage['condition_coverage'] = float(cond_match.group(1))
        
        return coverage
    
    def _parse_xcelium_report(self, content: str) -> Dict:
        """Parse Xcelium coverage report."""
        coverage = {}
        
        # Block coverage
        block_match = re.search(r'Block\s+Coverage\s*:\s*([\d.]+)%', content)
        if block_match:
            coverage['block_coverage'] = float(block_match.group(1))
        
        # Expression coverage
        expr_match = re.search(r'Expression\s+Coverage\s*:\s*([\d.]+)%', content)
        if expr_match:
            coverage['expression_coverage'] = float(expr_match.group(1))
        
        return coverage
    
    def _parse_generic_report(self, content: str) -> Dict:
        """Parse generic coverage report."""
        coverage = {}
        
        # Try to find any percentage values
        percentages = re.findall(r'([\d.]+)%', content)
        if percentages:
            coverage['average_coverage'] = sum(float(p) for p in percentages) / len(percentages)
        
        return coverage
    
    def get_coverage_by_module(self, content: str) -> pd.DataFrame:
        """
        Extract per-module coverage data.
        
        Returns:
            DataFrame with module-level coverage
        """
        modules = []
        
        # Pattern for module coverage lines
        pattern = r'(\w+)\s+[\d.]+%\s+[\d.]+%\s+[\d.]+%'
        
        for match in re.finditer(pattern, content):
            modules.append({
                'module': match.group(1),
                'coverage': float(match.group(2)) if len(match.groups()) > 1 else 0.0
            })
        
        return pd.DataFrame(modules)


class FunctionalCoverageParser:
    """Parses functional coverage from SystemVerilog covergroups."""
    
    def __init__(self, report_path: str):
        """
        Initialize functional coverage parser.
        
        Args:
            report_path: Path to functional coverage report
        """
        self.report_path = Path(report_path)
    
    def parse_covergroups(self) -> List[Dict]:
        """
        Parse covergroup data.
        
        Returns:
            List of covergroup metrics
        """
        if not self.report_path.exists():
            logger.warning(f"Functional coverage report not found: {self.report_path}")
            return []
        
        covergroups = []
        
        with open(self.report_path, 'r') as f:
            content = f.read()
        
        # Parse covergroup sections
        cg_pattern = r'Covergroup\s+(\w+)\s*:\s*([\d.]+)%'
        
        for match in re.finditer(cg_pattern, content):
            covergroups.append({
                'covergroup': match.group(1),
                'coverage': float(match.group(2))
            })
        
        logger.info(f"Parsed {len(covergroups)} covergroups")
        return covergroups
    
    def parse_coverpoints(self) -> List[Dict]:
        """
        Parse coverpoint data.
        
        Returns:
            List of coverpoint metrics
        """
        if not self.report_path.exists():
            return []
        
        coverpoints = []
        
        with open(self.report_path, 'r') as f:
            content = f.read()
        
        # Parse coverpoint sections
        cp_pattern = r'Coverpoint\s+(\w+)\s*:\s*([\d.]+)%'
        
        for match in re.finditer(cp_pattern, content):
            coverpoints.append({
                'coverpoint': match.group(1),
                'coverage': float(match.group(2)),
                'bins_hit': 0,  # Would need more parsing
                'bins_total': 0
            })
        
        return coverpoints

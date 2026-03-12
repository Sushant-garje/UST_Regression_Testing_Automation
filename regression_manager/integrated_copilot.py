"""
Integrated VLSI Regression Testing Copilot.
Combines Gemini-powered test selection with Load Optimizer for resource allocation.
"""

import logging
from typing import Dict, Optional
from dotenv import load_dotenv

from .gemini_regression_agent import GeminiRegressionAgent
from .load_optimizer import LoadOptimizer
from .coverage_parser import CoverageParser

load_dotenv()
logger = logging.getLogger(__name__)


class IntegratedRegressionCopilot:
    """
    Complete VLSI Regression Testing Copilot.
    
    Architecture:
    1. Gemini AI: Test selection, redundancy detection, prioritization
    2. Load Optimizer: Dynamic resource allocation (CPU/GPU/Cloud)
    """
    
    def __init__(self, csv_path: str, log_path: Optional[str] = None,
                 coverage_report_path: Optional[str] = None):
        """
        Initialize integrated copilot.
        
        Args:
            csv_path: Path to CSV testcase data
            log_path: Optional path to simulation log
            coverage_report_path: Optional path to coverage report
        """
        self.csv_path = csv_path
        self.log_path = log_path
        self.coverage_report_path = coverage_report_path
        
        # Initialize Gemini-powered regression agent
        self.gemini_agent = GeminiRegressionAgent(csv_path, log_path)
        
        # Initialize Load Optimizer
        self.load_optimizer = LoadOptimizer()
        
        logger.info("Integrated Regression Copilot initialized")
    
    def run_complete_optimization(self) -> Dict:
        """
        Run complete regression optimization workflow.
        
        Workflow:
        1. Gemini analyzes tests and makes selection decisions
        2. Load Optimizer allocates selected tests to resources
        3. Generate comprehensive execution plan
        
        Returns:
            Complete optimization results with resource allocation
        """
        logger.info("=" * 80)
        logger.info("INTEGRATED REGRESSION COPILOT - COMPLETE WORKFLOW")
        logger.info("=" * 80)
        
        # Check if Gemini is available
        if not self.gemini_agent.copilot.model:
            logger.warning("⚠️  Gemini API not available - using fallback mode")
            logger.warning("⚠️  Set GOOGLE_API_KEY environment variable to enable AI features")
        
        # Phase 1: Gemini-powered test selection
        logger.info("\n[PHASE 1] Gemini AI: Test Selection & Prioritization")
        logger.info("-" * 80)
        
        gemini_result = self.gemini_agent.analyze_and_optimize()
        
        logger.info(f"✅ Gemini Analysis Complete:")
        logger.info(f"   - Total Tests: {gemini_result['summary']['total_tests']}")
        logger.info(f"   - Selected: {gemini_result['summary']['selected']}")
        logger.info(f"   - Excluded: {gemini_result['summary']['excluded']}")
        logger.info(f"   - Critical (P0): {gemini_result['summary']['critical_tests']}")
        
        # Phase 2: Load Optimizer resource allocation
        logger.info("\n[PHASE 2] Load Optimizer: Resource Allocation")
        logger.info("-" * 80)
        
        resource_allocation = self._allocate_resources(gemini_result)
        
        logger.info(f"✅ Resource Allocation Complete:")
        logger.info(f"   - CPU Tests: {resource_allocation['allocation_summary']['cpu_count']}")
        logger.info(f"   - GPU Tests: {resource_allocation['allocation_summary']['gpu_count']}")
        logger.info(f"   - Cloud Tests: {resource_allocation['allocation_summary']['cloud_count']}")
        logger.info(f"   - Estimated Cost: ${resource_allocation['cost_estimate']['total_cost']:.2f}")
        
        # Phase 3: Parse coverage (if available)
        coverage_data = None
        if self.coverage_report_path:
            logger.info("\n[PHASE 3] Coverage Analysis")
            logger.info("-" * 80)
            coverage_data = self._parse_coverage()
            logger.info(f"✅ Coverage Parsed")
        
        # Phase 4: Generate execution plan
        logger.info("\n[PHASE 4] Execution Plan Generation")
        logger.info("-" * 80)
        
        execution_plan = self._generate_execution_plan(
            gemini_result, resource_allocation, coverage_data
        )
        
        logger.info(f"✅ Execution Plan Ready")
        logger.info(f"   - Total Runtime: {execution_plan['estimated_total_runtime']:.2f}s")
        logger.info(f"   - Parallel Batches: {execution_plan['parallel_batches']}")
        
        # Combine all results
        complete_result = {
            'gemini_decisions': {
                'analysis': gemini_result['gemini_analysis'],
                'ranked_tests': gemini_result['ranked_tests'],
                'excluded_tests': gemini_result['excluded_tests']
            },
            'resource_allocation': resource_allocation,
            'coverage_analysis': coverage_data,
            'execution_plan': execution_plan,
            'summary': {
                **gemini_result['summary'],
                'estimated_cost': resource_allocation['cost_estimate']['total_cost'],
                'estimated_runtime': execution_plan['estimated_total_runtime']
            }
        }
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ COMPLETE OPTIMIZATION FINISHED")
        logger.info("=" * 80)
        
        return complete_result
    
    def _allocate_resources(self, gemini_result: Dict) -> Dict:
        """
        Allocate tests to CPU/GPU/Cloud resources based on complexity.
        
        Args:
            gemini_result: Gemini's test selection results
            
        Returns:
            Resource allocation details
        """
        import pandas as pd
        
        # Convert ranked tests to DataFrame
        tests_df = pd.DataFrame(gemini_result['ranked_tests'])
        
        # Add priority rank for optimizer
        tests_df['priority_rank'] = range(1, len(tests_df) + 1)
        
        # Allocate tests to resources
        allocated_df = self.load_optimizer.allocate_tests(tests_df)
        
        # Get allocation summary
        allocation_summary = {
            'cpu_count': len(allocated_df[allocated_df['resource_type'] == 'cpu']),
            'gpu_count': len(allocated_df[allocated_df['resource_type'] == 'gpu']),
            'cloud_count': len(allocated_df[allocated_df['resource_type'] == 'cloud'])
        }
        
        # Get cost estimate
        cost_estimate = self.load_optimizer.estimate_cost()
        
        # Get server usage
        server_usage = self.load_optimizer.get_server_usage_report()
        
        return {
            'allocated_tests': allocated_df.to_dict('records'),
            'allocation_summary': allocation_summary,
            'cost_estimate': cost_estimate,
            'server_usage': server_usage.to_dict('records') if not server_usage.empty else []
        }
    
    def _parse_coverage(self) -> Optional[Dict]:
        """Parse coverage report if available."""
        try:
            parser = CoverageParser(self.coverage_report_path)
            coverage_data = parser.parse()
            return coverage_data
        except Exception as e:
            logger.warning(f"Coverage parsing failed: {e}")
            return None
    
    def _generate_execution_plan(self, gemini_result: Dict, 
                                 resource_allocation: Dict,
                                 coverage_data: Optional[Dict]) -> Dict:
        """
        Generate detailed execution plan.
        
        Args:
            gemini_result: Gemini's decisions
            resource_allocation: Resource allocation details
            coverage_data: Coverage analysis
            
        Returns:
            Execution plan
        """
        allocated_tests = resource_allocation['allocated_tests']
        
        # Group tests by priority for batching
        priority_groups = {}
        for test in allocated_tests:
            priority = test.get('priority', 'P2')
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(test)
        
        # Calculate estimated runtime (considering parallel execution)
        total_runtime = 0
        parallel_batches = 0
        
        for priority in ['P0', 'P1', 'P2', 'P3']:
            if priority in priority_groups:
                tests = priority_groups[priority]
                # Assume parallel execution within priority group
                max_runtime = max([t['runtime_seconds'] for t in tests])
                total_runtime += max_runtime
                parallel_batches += 1
        
        # Generate execution batches
        execution_batches = []
        for priority in ['P0', 'P1', 'P2', 'P3']:
            if priority in priority_groups:
                execution_batches.append({
                    'priority': priority,
                    'tests': priority_groups[priority],
                    'test_count': len(priority_groups[priority]),
                    'estimated_runtime': max([t['runtime_seconds'] for t in priority_groups[priority]])
                })
        
        return {
            'execution_batches': execution_batches,
            'parallel_batches': parallel_batches,
            'estimated_total_runtime': total_runtime,
            'priority_distribution': {
                priority: len(tests) for priority, tests in priority_groups.items()
            }
        }
    
    def configure_resources(self, cpu_units: int, gpu_units: int, cloud_units: int):
        """
        Configure available resources for load optimization.
        
        Args:
            cpu_units: Number of CPU cores
            gpu_units: Number of GPUs
            cloud_units: Number of cloud instances
        """
        self.load_optimizer.configure_resources(cpu_units, gpu_units, cloud_units)
        logger.info(f"Resources configured: CPU={cpu_units}, GPU={gpu_units}, Cloud={cloud_units}")

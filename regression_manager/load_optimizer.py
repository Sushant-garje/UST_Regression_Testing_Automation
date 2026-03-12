"""
Load Optimizer Agent for dynamic resource allocation.
Allocates tests across CPU/GPU/Cloud resources based on complexity.
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd

logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Available resource types."""
    CPU = "cpu"
    GPU = "gpu"
    CLOUD = "cloud"


@dataclass
class ResourcePool:
    """Resource pool configuration."""
    resource_type: ResourceType
    available_units: int
    cost_per_hour: float
    performance_multiplier: float  # Relative to CPU


@dataclass
class TestAllocation:
    """Test allocation to resources."""
    testcase_id: str
    resource_type: ResourceType
    estimated_runtime: float
    priority: int
    server_id: Optional[str] = None


class LoadOptimizer:
    """
    Optimizes test allocation across heterogeneous resources.
    Implements dynamic load balancing for CPU/GPU/Cloud.
    """
    
    def __init__(self):
        """Initialize load optimizer with default resource pools."""
        self.resource_pools = {
            ResourceType.CPU: ResourcePool(
                resource_type=ResourceType.CPU,
                available_units=16,
                cost_per_hour=1.0,
                performance_multiplier=1.0
            ),
            ResourceType.GPU: ResourcePool(
                resource_type=ResourceType.GPU,
                available_units=4,
                cost_per_hour=3.0,
                performance_multiplier=5.0
            ),
            ResourceType.CLOUD: ResourcePool(
                resource_type=ResourceType.CLOUD,
                available_units=100,
                cost_per_hour=2.0,
                performance_multiplier=3.0
            )
        }
        
        self.allocations: List[TestAllocation] = []
        self.server_usage: Dict[str, Dict] = {}
    
    def configure_resources(self, cpu_units: int, gpu_units: int, cloud_units: int):
        """
        Configure available resources.
        
        Args:
            cpu_units: Number of CPU cores available
            gpu_units: Number of GPUs available
            cloud_units: Number of cloud instances available
        """
        self.resource_pools[ResourceType.CPU].available_units = cpu_units
        self.resource_pools[ResourceType.GPU].available_units = gpu_units
        self.resource_pools[ResourceType.CLOUD].available_units = cloud_units
        
        logger.info(f"Configured resources: CPU={cpu_units}, GPU={gpu_units}, Cloud={cloud_units}")
    
    def allocate_tests(self, tests_df: pd.DataFrame) -> pd.DataFrame:
        """
        Allocate tests to optimal resources.
        
        Args:
            tests_df: DataFrame with test information
            
        Returns:
            DataFrame with resource allocations
        """
        logger.info(f"Allocating {len(tests_df)} tests to resources")
        
        # Sort by priority (highest first)
        tests_sorted = tests_df.sort_values('priority_rank', ascending=True).copy()
        
        # Classify tests by complexity
        tests_sorted['complexity'] = self._classify_complexity(tests_sorted)
        
        # Allocate based on complexity and availability
        allocations = []
        
        for _, test in tests_sorted.iterrows():
            allocation = self._allocate_single_test(test)
            allocations.append(allocation)
        
        # Add allocation info to dataframe
        alloc_df = pd.DataFrame([{
            'testcase_id': a.testcase_id,
            'resource_type': a.resource_type.value,
            'estimated_runtime': a.estimated_runtime,
            'server_id': a.server_id
        } for a in allocations])
        
        result = tests_sorted.merge(alloc_df, on='testcase_id', how='left')
        
        logger.info(f"Allocation complete: {self._get_allocation_summary()}")
        
        return result
    
    def _classify_complexity(self, tests_df: pd.DataFrame) -> pd.Series:
        """
        Classify test complexity based on runtime and coverage.
        
        Returns:
            Series with complexity labels (low, medium, high)
        """
        # Ensure columns are numeric to avoid TypeError
        tests_df = tests_df.copy()
        tests_df['runtime_seconds'] = pd.to_numeric(tests_df['runtime_seconds'], errors='coerce')
        tests_df['coverage'] = pd.to_numeric(tests_df['coverage'], errors='coerce')
        # Use runtime and coverage as complexity indicators
        runtime_q75 = tests_df['runtime_seconds'].quantile(0.75)
        coverage_q75 = tests_df['coverage'].quantile(0.75)
        
        def classify(row):
            if row['runtime_seconds'] > runtime_q75 and row['coverage'] > coverage_q75:
                return 'high'
            elif row['runtime_seconds'] > runtime_q75 or row['coverage'] > coverage_q75:
                return 'medium'
            else:
                return 'low'
        
        return tests_df.apply(classify, axis=1)
    
    def _allocate_single_test(self, test: pd.Series) -> TestAllocation:
        """
        Allocate a single test to optimal resource.
        
        Args:
            test: Test information
            
        Returns:
            TestAllocation object
        """
        complexity = test['complexity']
        # Ensure runtime is float for arithmetic
        try:
            runtime = float(test['runtime_seconds'])
        except Exception:
            runtime = 0.0
        priority = test['priority_rank']
        
        # Allocation strategy
        if complexity == 'high' and self.resource_pools[ResourceType.GPU].available_units > 0:
            # High complexity -> GPU
            resource = ResourceType.GPU
            self.resource_pools[ResourceType.GPU].available_units -= 1
            estimated_runtime = runtime / self.resource_pools[ResourceType.GPU].performance_multiplier
            
        elif complexity == 'medium' and self.resource_pools[ResourceType.CLOUD].available_units > 0:
            # Medium complexity -> Cloud
            resource = ResourceType.CLOUD
            self.resource_pools[ResourceType.CLOUD].available_units -= 1
            estimated_runtime = runtime / self.resource_pools[ResourceType.CLOUD].performance_multiplier
            
        elif self.resource_pools[ResourceType.CPU].available_units > 0:
            # Low complexity or fallback -> CPU
            resource = ResourceType.CPU
            self.resource_pools[ResourceType.CPU].available_units -= 1
            estimated_runtime = runtime
            
        else:
            # All resources exhausted, queue for cloud
            resource = ResourceType.CLOUD
            estimated_runtime = runtime / self.resource_pools[ResourceType.CLOUD].performance_multiplier
        
        # Assign server ID
        server_id = self._assign_server(resource)
        
        allocation = TestAllocation(
            testcase_id=test['testcase_id'],
            resource_type=resource,
            estimated_runtime=estimated_runtime,
            priority=priority,
            server_id=server_id
        )
        
        self.allocations.append(allocation)
        
        # Track server usage
        if server_id not in self.server_usage:
            self.server_usage[server_id] = {
                'resource_type': resource.value,
                'tests_allocated': 0,
                'total_runtime': 0.0
            }
        
        self.server_usage[server_id]['tests_allocated'] += 1
        # Ensure estimated_runtime is float to avoid TypeError
        try:
            est_runtime_float = float(estimated_runtime)
        except Exception:
            est_runtime_float = 0.0
        self.server_usage[server_id]['total_runtime'] += est_runtime_float
        
        return allocation
    
    def _assign_server(self, resource_type: ResourceType) -> str:
        """Assign a server ID based on resource type."""
        if resource_type == ResourceType.CPU:
            return f"cpu_server_{len([a for a in self.allocations if a.resource_type == ResourceType.CPU]) % 4 + 1}"
        elif resource_type == ResourceType.GPU:
            return f"gpu_server_{len([a for a in self.allocations if a.resource_type == ResourceType.GPU]) % 2 + 1}"
        else:
            return f"cloud_instance_{len([a for a in self.allocations if a.resource_type == ResourceType.CLOUD]) % 10 + 1}"
    
    def _get_allocation_summary(self) -> str:
        """Get summary of resource allocation."""
        cpu_count = len([a for a in self.allocations if a.resource_type == ResourceType.CPU])
        gpu_count = len([a for a in self.allocations if a.resource_type == ResourceType.GPU])
        cloud_count = len([a for a in self.allocations if a.resource_type == ResourceType.CLOUD])
        
        return f"CPU={cpu_count}, GPU={gpu_count}, Cloud={cloud_count}"
    
    def get_server_usage_report(self) -> pd.DataFrame:
        """
        Get server usage report.
        
        Returns:
            DataFrame with server usage statistics
        """
        if not self.server_usage:
            return pd.DataFrame()
        
        report = []
        for server_id, usage in self.server_usage.items():
            report.append({
                'server_id': server_id,
                'resource_type': usage['resource_type'],
                'tests_allocated': usage['tests_allocated'],
                'total_runtime_hours': usage['total_runtime'] / 3600,
                'utilization': min(100, (usage['total_runtime'] / 3600) * 100)
            })
        
        return pd.DataFrame(report)
    
    def estimate_cost(self) -> Dict:
        """
        Estimate total cost of regression run.
        
        Returns:
            Dictionary with cost breakdown
        """
        cost_breakdown = {
            'cpu_cost': 0.0,
            'gpu_cost': 0.0,
            'cloud_cost': 0.0,
            'total_cost': 0.0
        }
        
        for allocation in self.allocations:
            runtime_hours = allocation.estimated_runtime / 3600
            pool = self.resource_pools[allocation.resource_type]
            cost = runtime_hours * pool.cost_per_hour
            
            if allocation.resource_type == ResourceType.CPU:
                cost_breakdown['cpu_cost'] += cost
            elif allocation.resource_type == ResourceType.GPU:
                cost_breakdown['gpu_cost'] += cost
            else:
                cost_breakdown['cloud_cost'] += cost
        
        cost_breakdown['total_cost'] = sum([
            cost_breakdown['cpu_cost'],
            cost_breakdown['gpu_cost'],
            cost_breakdown['cloud_cost']
        ])
        
        return cost_breakdown

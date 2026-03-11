"""
Run the integrated VLSI Regression Testing Copilot.
Demonstrates Gemini AI + Load Optimizer working together.
"""

import json
from dotenv import load_dotenv
from regression_manager.integrated_copilot import IntegratedRegressionCopilot

load_dotenv()


def main():
    """Run complete integrated workflow."""
    
    print("\n" + "=" * 80)
    print("  INTEGRATED VLSI REGRESSION TESTING COPILOT")
    print("  Gemini AI + Load Optimizer")
    print("=" * 80 + "\n")
    
    # Initialize integrated copilot
    print("Initializing copilot...")
    copilot = IntegratedRegressionCopilot(
        csv_path='rag_training_data.csv',
        log_path='sim.log'
    )
    
    # Configure resources
    print("Configuring resources...")
    copilot.configure_resources(
        cpu_units=16,
        gpu_units=4,
        cloud_units=50
    )
    
    # Run complete optimization
    print("\nRunning complete optimization...\n")
    result = copilot.run_complete_optimization()
    
    # Display results
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    
    print("\n[SUMMARY]")
    print("-" * 80)
    summary = result['summary']
    print(f"Total Tests:        {summary['total_tests']}")
    print(f"Selected Tests:     {summary['selected']}")
    print(f"Excluded Tests:     {summary['excluded']}")
    print(f"Critical Tests:     {summary['critical_tests']}")
    print(f"High Coverage:      {summary['high_coverage_tests']}")
    print(f"Optimization Ratio: {summary['optimization_ratio']:.1%}")
    print(f"Estimated Cost:     ${summary['estimated_cost']:.2f}")
    print(f"Estimated Runtime:  {summary['estimated_runtime']:.2f}s")
    
    print("\n[GEMINI ANALYSIS]")
    print("-" * 80)
    analysis = result['gemini_decisions']['analysis']
    print(f"Quality Score: {analysis.get('quality_score', 'N/A')}/100")
    print(f"\nKey Patterns:")
    for pattern in analysis.get('key_patterns', []):
        print(f"  • {pattern}")
    print(f"\nRecommendations:")
    for rec in analysis.get('recommendations', []):
        print(f"  • {rec}")
    
    print("\n[TOP 10 PRIORITIZED TESTS]")
    print("-" * 80)
    print(f"{'Rank':<6} {'Test ID':<30} {'Priority':<10} {'Coverage':<10} {'Resource':<10}")
    print("-" * 80)
    
    allocated_tests = result['resource_allocation']['allocated_tests']
    for i, test in enumerate(allocated_tests[:10], 1):
        print(f"{i:<6} {test['testcase_id']:<30} {test['priority']:<10} "
              f"{test['coverage']:<10.2f} {test.get('resource_type', 'N/A'):<10}")
    
    print("\n[RESOURCE ALLOCATION]")
    print("-" * 80)
    alloc_summary = result['resource_allocation']['allocation_summary']
    print(f"CPU Tests:   {alloc_summary['cpu_count']}")
    print(f"GPU Tests:   {alloc_summary['gpu_count']}")
    print(f"Cloud Tests: {alloc_summary['cloud_count']}")
    
    cost = result['resource_allocation']['cost_estimate']
    print(f"\n[COST BREAKDOWN]")
    print(f"  CPU Cost:   ${cost['cpu_cost']:.2f}")
    print(f"  GPU Cost:   ${cost['gpu_cost']:.2f}")
    print(f"  Cloud Cost: ${cost['cloud_cost']:.2f}")
    print(f"  Total Cost: ${cost['total_cost']:.2f}")
    
    print("\n[EXECUTION PLAN]")
    print("-" * 80)
    exec_plan = result['execution_plan']
    print(f"Parallel Batches: {exec_plan['parallel_batches']}")
    print(f"Total Runtime:    {exec_plan['estimated_total_runtime']:.2f}s")
    print(f"\nPriority Distribution:")
    for priority, count in exec_plan['priority_distribution'].items():
        print(f"  {priority}: {count} tests")
    
    print("\n[EXCLUDED TESTS]")
    print("-" * 80)
    excluded = result['gemini_decisions']['excluded_tests']
    print(f"Total Excluded: {len(excluded)}")
    for i, test in enumerate(excluded[:5], 1):
        print(f"\n{i}. {test['testcase_id']}")
        print(f"   Reason: {test['reason']}")
    
    # Save results
    output_file = 'integrated_copilot_results.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n\n[SUCCESS] Full results saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] INTEGRATED COPILOT COMPLETE")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()

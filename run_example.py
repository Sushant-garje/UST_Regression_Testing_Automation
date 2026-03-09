"""
Quick start script to run the Regression Manager Agent.
"""

import logging
import json
from pathlib import Path
from regression_manager import RegressionManagerAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run the regression manager agent with example data."""
    
    print("=" * 80)
    print("REGRESSION MANAGER AGENT - QUICK START")
    print("=" * 80)
    
    # Check if data files exist
    csv_path = Path('rag_training_data.csv')
    log_path = Path('sim.log')
    
    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        logger.info("Please ensure rag_training_data.csv is in the current directory")
        return
    
    if not log_path.exists():
        logger.warning(f"Log file not found: {log_path}")
        logger.info("Proceeding without log data")
        log_path = None
    
    # Initialize and run agent
    logger.info("Initializing Regression Manager Agent...")
    agent = RegressionManagerAgent(
        csv_path=str(csv_path),
        log_path=str(log_path) if log_path else None
    )
    
    logger.info("Running optimization...")
    result = agent.run()
    
    # Display results
    print("\n" + "=" * 80)
    print("OPTIMIZATION RESULTS")
    print("=" * 80)
    
    print("\n--- SUMMARY ---")
    summary = result['summary']
    print(f"Total Tests:        {summary['total_tests']}")
    print(f"Selected Tests:     {summary['selected']}")
    print(f"Excluded Tests:     {summary['excluded']}")
    print(f"Optimization Ratio: {summary['optimization_ratio']:.2%}")
    
    print("\n--- TOP 10 HIGHEST PRIORITY TESTS ---")
    print(f"{'Rank':<6} {'Testcase ID':<30} {'Score':<8} {'Action':<12} {'Coverage':<10} {'Runtime':<10}")
    print("-" * 80)
    for test in result['ranked_tests'][:10]:
        print(f"{test['priority_rank']:<6} {test['testcase_id']:<30} {test['score']:<8.4f} "
              f"{test['action']:<12} {test['coverage']:<10.2f} {test['runtime_seconds']:<10.2f}")
    
    if result['excluded_tests']:
        print(f"\n--- EXCLUDED TESTS ({len(result['excluded_tests'])}) ---")
        for i, test in enumerate(result['excluded_tests'][:5], 1):
            print(f"\n{i}. {test['testcase_id']}")
            print(f"   Module: {test['module_name']}")
            print(f"   Pass Rate: {test['pass_rate']:.2%}")
            print(f"   Coverage Gain: {test['coverage_gain']:.2f}%")
            print(f"   Reason: {test['reason'][:100]}...")
    
    # Save results to file
    output_file = 'regression_optimization_results.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n\nFull results saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("OPTIMIZATION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()

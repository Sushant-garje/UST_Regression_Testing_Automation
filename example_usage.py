"""
Example usage of Regression Manager Agent.
Demonstrates both programmatic and API usage.
"""

import json
from regression_manager import RegressionManagerAgent


def example_programmatic_usage():
    """Example of using the agent programmatically."""
    print("=" * 80)
    print("EXAMPLE: Programmatic Usage")
    print("=" * 80)
    
    # Initialize agent
    agent = RegressionManagerAgent(
        csv_path='rag_training_data.csv',
        log_path='sim.log'
    )
    
    # Run optimization
    result = agent.run()
    
    # Print results
    print("\n--- SUMMARY ---")
    print(json.dumps(result['summary'], indent=2))
    
    print("\n--- TOP 10 RANKED TESTS ---")
    for test in result['ranked_tests'][:10]:
        print(f"  {test['testcase_id']}: score={test['score']:.4f}, action={test['action']}")
    
    print(f"\n--- EXCLUDED TESTS ({len(result['excluded_tests'])}) ---")
    for test in result['excluded_tests'][:5]:
        print(f"  {test['testcase_id']}: {test['reason'][:80]}...")
    
    return result


def example_api_request():
    """Example API request format."""
    print("\n" + "=" * 80)
    print("EXAMPLE: API Request")
    print("=" * 80)
    
    request_example = {
        "csv_path": "rag_training_data.csv",
        "log_path": "sim.log"
    }
    
    print("\nPOST /optimize-regression")
    print("Content-Type: application/json")
    print("\nRequest Body:")
    print(json.dumps(request_example, indent=2))
    
    print("\n\nTo start the API server, run:")
    print("  python -m regression_manager.api_service")
    print("\nOr with uvicorn:")
    print("  uvicorn regression_manager.api_service:app --reload")
    
    print("\n\nExample curl command:")
    print('  curl -X POST "http://localhost:8000/optimize-regression" \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"csv_path": "rag_training_data.csv", "log_path": "sim.log"}\'')


def example_config_update():
    """Example configuration update."""
    print("\n" + "=" * 80)
    print("EXAMPLE: Configuration Update")
    print("=" * 80)
    
    from regression_manager.config import config
    
    print("\nCurrent Configuration:")
    print(f"  Coverage Weight: {config.scoring_weights.coverage}")
    print(f"  Efficiency Weight: {config.scoring_weights.efficiency}")
    print(f"  Stability Weight: {config.scoring_weights.stability}")
    print(f"  Pass Rate Threshold: {config.redundancy_thresholds.pass_rate_threshold}")
    print(f"  Critical Modules: {config.critical_modules.modules[:3]}...")
    
    print("\n\nTo update via API:")
    update_example = {
        "coverage_weight": 0.5,
        "efficiency_weight": 0.3,
        "stability_weight": 0.2,
        "critical_modules": ["cpu_core", "memory_controller", "jk_ff"]
    }
    print("PUT /config")
    print(json.dumps(update_example, indent=2))


if __name__ == '__main__':
    # Run programmatic example
    result = example_programmatic_usage()
    
    # Show API examples
    example_api_request()
    example_config_update()
    
    print("\n" + "=" * 80)
    print("Examples complete!")
    print("=" * 80)

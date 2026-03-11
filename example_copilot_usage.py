"""
Example usage of the complete VLSI Regression Testing Copilot.
Demonstrates all features including LLM integration and resource optimization.
"""

import json
import os
from dotenv import load_dotenv
from regression_manager import RegressionManagerAgent
from regression_manager.llm_copilot import RegressionCopilot
from regression_manager.load_optimizer import LoadOptimizer
from regression_manager.coverage_parser import CoverageParser

# Load environment variables from .env file
load_dotenv()
from regression_manager.coverage_parser import



def example_full_workflow():
    """Complete workflow with all features enabled."""
    print("=" * 80)
    print("VLSI REGRESSION TESTING COPILOT - FULL WORKFLOW")
    print("=" * 80)
    
    # Get API key from environment (optional)
    llm_api_key = os.getenv('GOOGLE_API_KEY')  # Google Gemini API key
    
    if not llm_api_key:
        print("\n⚠️  No Google API key found.")
        print("To enable AI copilot features:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable: export GOOGLE_API_KEY='your-key-here'")
        print("\nContinuing without AI features...\n")
    
    # Initialize agent with all features
    agent = RegressionManagerAgent(
        csv_path='rag_training_data.csv',
        log_path='sim.log',
        coverage_report_path=None,  # Add if available
        enable_load_optimizer=True,
        enable_llm_copilot=bool(llm_api_key),  # Enable if API key available
        llm_api_key=llm_api_key
    )
    
    # Run optimization
    print("\n🚀 Running regression optimization...")
    result = agent.run()
    
    # Display results
    print("\n📊 OPTIMIZATION RESULTS")
    print("-" * 80)
    print(f"Total Tests: {result['summary']['total_tests']}")
    print(f"Selected: {result['summary']['selected']}")
    print(f"Excluded: {result['summary']['excluded']}")
    print(f"Optimization Ratio: {result['summary']['optimization_ratio']:.1%}")
    
    # Resource allocation
    if 'resource_allocation' in result:
        print("\n💻 RESOURCE ALLOCATION")
        print("-" * 80)
        cost = result['resource_allocation']['cost_estimate']
        print(f"CPU Cost: ${cost['cpu_cost']:.2f}")
        print(f"GPU Cost: ${cost['gpu_cost']:.2f}")
        print(f"Cloud Cost: ${cost['cloud_cost']:.2f}")
        print(f"Total Cost: ${cost['total_cost']:.2f}")
        
        print("\n📈 Server Usage:")
        for server in result['resource_allocation']['server_usage'][:5]:
            print(f"  {server['server_id']}: {server['tests_allocated']} tests, "
                  f"{server['total_runtime_hours']:.2f}h")
    
    # LLM insights
    if 'llm_insights' in result:
        print("\n🤖 AI COPILOT INSIGHTS")
        print("-" * 80)
        print(result['llm_insights'])
    
    return result


def example_copilot_chat():
    """Example of interactive copilot chat."""
    print("\n" + "=" * 80)
    print("COPILOT CHAT INTERFACE")
    print("=" * 80)
    
    llm_api_key = os.getenv('GOOGLE_API_KEY')
    
    if not llm_api_key:
        print("\n⚠️  No API key found. Set GOOGLE_API_KEY environment variable.")
        print("Get your key from: https://makersuite.google.com/app/apikey")
        return
    
    copilot = RegressionCopilot(api_key=llm_api_key)
    
    # Example questions
    questions = [
        "What are the best practices for regression test selection?",
        "How can I reduce regression runtime by 30%?",
        "Which modules should I mark as critical?",
        "Explain the coverage gain metric"
    ]
    
    for question in questions:
        print(f"\n👤 User: {question}")
        response = copilot.chat(question)
        print(f"🤖 Copilot: {response[:200]}...")  # Truncate for display


def example_resource_optimization():
    """Example of resource load optimization."""
    print("\n" + "=" * 80)
    print("RESOURCE LOAD OPTIMIZATION")
    print("=" * 80)
    
    # Initialize optimizer
    optimizer = LoadOptimizer()
    
    # Configure resources
    optimizer.configure_resources(
        cpu_units=16,
        gpu_units=4,
        cloud_units=50
    )
    
    print("\n✅ Resources configured:")
    print("  - 16 CPU cores")
    print("  - 4 GPUs")
    print("  - 50 Cloud instances")
    
    # Load test data
    import pandas as pd
    df = pd.read_csv('rag_training_data.csv')
    
    # Create mock prioritized tests
    df['priority_rank'] = range(1, len(df) + 1)
    df['testcase_id'] = df['module'] + '_' + df['test'] + '_seed' + df['seed'].astype(str)
    df['runtime_seconds'] = df['sim_time']
    df['coverage'] = df['coverage']
    
    # Allocate tests
    df_allocated = optimizer.allocate_tests(df.head(50))
    
    print("\n📊 Allocation Summary:")
    print(df_allocated.groupby('resource_type').size())
    
    # Cost estimate
    cost = optimizer.estimate_cost()
    print(f"\n💰 Estimated Cost: ${cost['total_cost']:.2f}")
    
    # Server usage
    usage = optimizer.get_server_usage_report()
    print(f"\n🖥️  Servers Used: {len(usage)}")
    print(usage.head().to_string())


def example_coverage_parsing():
    """Example of coverage report parsing."""
    print("\n" + "=" * 80)
    print("COVERAGE REPORT PARSING")
    print("=" * 80)
    
    # Check if coverage report exists
    if not os.path.exists('sim.log'):
        print("\n⚠️  No coverage report found")
        return
    
    # Parse coverage (using log as example)
    parser = CoverageParser('sim.log', report_type='auto')
    coverage = parser.parse()
    
    print("\n📈 Coverage Metrics:")
    for metric, value in coverage.items():
        print(f"  {metric}: {value}")


def example_api_usage():
    """Example API usage with all features."""
    print("\n" + "=" * 80)
    print("API USAGE EXAMPLES")
    print("=" * 80)
    
    print("\n1. Optimize Regression with All Features:")
    print("""
curl -X POST "http://localhost:8000/optimize-regression" \\
     -H "Content-Type: application/json" \\
     -d '{
       "csv_path": "rag_training_data.csv",
       "log_path": "sim.log",
       "enable_load_optimizer": true,
       "enable_llm_copilot": true,
       "llm_api_key": "your-api-key"
     }'
""")
    
    print("\n2. Chat with Copilot:")
    print("""
curl -X POST "http://localhost:8000/copilot/chat" \\
     -H "Content-Type: application/json" \\
     -d '{
       "message": "How can I improve my regression efficiency?",
       "llm_api_key": "your-api-key"
     }'
""")
    
    print("\n3. Configure Resources:")
    print("""
curl -X POST "http://localhost:8000/resources/configure" \\
     -H "Content-Type: application/json" \\
     -d '{
       "cpu_units": 32,
       "gpu_units": 8,
       "cloud_units": 100
     }'
""")
    
    print("\n4. Parse Coverage Report:")
    print("""
curl -X POST "http://localhost:8000/coverage/parse" \\
     -F "coverage_file=@coverage.rpt" \\
     -F "report_type=vcs"
""")
    
    print("\n5. Get Resource Usage:")
    print("""
curl -X GET "http://localhost:8000/resources/usage"
""")


def main():
    """Run all examples."""
    
    # Full workflow
    result = example_full_workflow()
    
    # Resource optimization
    example_resource_optimization()
    
    # Coverage parsing
    example_coverage_parsing()
    
    # Copilot chat (if API key available)
    if os.getenv('GOOGLE_API_KEY'):
        example_copilot_chat()
    else:
        print("\n⚠️  Skipping copilot chat - no API key found")
        print("Set GOOGLE_API_KEY to enable AI features")
        print("Get your key from: https://makersuite.google.com/app/apikey")
    
    # API examples
    example_api_usage()
    
    print("\n" + "=" * 80)
    print("✅ ALL EXAMPLES COMPLETE")
    print("=" * 80)
    
    print("\n📚 Next Steps:")
    print("1. Set up LLM API key for copilot features")
    print("2. Configure your resource pools")
    print("3. Add coverage report paths")
    print("4. Start the API server: uvicorn regression_manager.api_service:app --reload")
    print("5. Try the copilot chat interface")


if __name__ == '__main__':
    main()

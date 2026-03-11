"""
Test script for Google Gemini integration.
Verifies that the AI copilot is working correctly.
"""

import os
from dotenv import load_dotenv
from regression_manager.llm_copilot import RegressionCopilot

# Load environment variables from .env file
load_dotenv()


def test_gemini_connection():
    """Test basic Gemini connection."""
    print("=" * 80)
    print("TESTING GOOGLE GEMINI INTEGRATION")
    print("=" * 80)
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("\n❌ GOOGLE_API_KEY not found in environment")
        print("\nTo set up:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Run: export GOOGLE_API_KEY='your-key-here'")
        return False
    
    print(f"\n✅ API key found: {api_key[:10]}...")
    
    # Initialize copilot
    print("\n📡 Initializing Gemini copilot...")
    copilot = RegressionCopilot(api_key=api_key)
    
    if not copilot.model:
        print("❌ Failed to initialize Gemini model")
        return False
    
    print(f"✅ Gemini model initialized: {copilot.model_name}")
    
    # Test simple query
    print("\n🧪 Testing simple query...")
    try:
        response = copilot.chat("What is regression testing in VLSI?")
        print(f"\n✅ Response received ({len(response)} characters)")
        print(f"\n📝 Sample response:\n{response[:300]}...")
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False
    
    # Test analysis
    print("\n🧪 Testing regression analysis...")
    try:
        test_result = {
            'summary': {
                'total_tests': 100,
                'selected': 75,
                'excluded': 25,
                'optimization_ratio': 0.75
            },
            'ranked_tests': [
                {
                    'testcase_id': 'cpu_test_1',
                    'score': 0.95,
                    'coverage': 98.5,
                    'runtime_seconds': 120
                }
            ],
            'excluded_tests': []
        }
        
        insights = copilot.analyze_regression_results(test_result)
        print(f"\n✅ Analysis completed ({len(insights)} characters)")
        print(f"\n📊 Sample insights:\n{insights[:300]}...")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False
    
    # Test explanation
    print("\n🧪 Testing test score explanation...")
    try:
        test_data = {
            'testcase_id': 'memory_test_1',
            'score': 0.87,
            'coverage': 95.0,
            'runtime_seconds': 145.0,
            'pass_rate': 0.92,
            'action': 'run_first'
        }
        
        explanation = copilot.explain_test_score(test_data)
        print(f"\n✅ Explanation generated ({len(explanation)} characters)")
        print(f"\n💡 Sample explanation:\n{explanation[:300]}...")
        
    except Exception as e:
        print(f"❌ Explanation failed: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - GEMINI INTEGRATION WORKING")
    print("=" * 80)
    
    return True


def test_fallback_mode():
    """Test fallback mode without API key."""
    print("\n" + "=" * 80)
    print("TESTING FALLBACK MODE (NO API KEY)")
    print("=" * 80)
    
    # Initialize without API key
    copilot = RegressionCopilot(api_key=None)
    
    if copilot.model:
        print("⚠️  Model initialized despite no API key")
        return False
    
    print("\n✅ Correctly detected missing API key")
    
    # Test fallback analysis
    test_result = {
        'summary': {
            'total_tests': 100,
            'selected': 75,
            'excluded': 25,
            'optimization_ratio': 0.75
        },
        'ranked_tests': [],
        'excluded_tests': []
    }
    
    insights = copilot.analyze_regression_results(test_result)
    print(f"\n✅ Fallback analysis working ({len(insights)} characters)")
    print(f"\n📝 Fallback output:\n{insights[:200]}...")
    
    print("\n" + "=" * 80)
    print("✅ FALLBACK MODE WORKING")
    print("=" * 80)
    
    return True


if __name__ == '__main__':
    print("\n🚀 Starting Gemini Integration Tests\n")
    
    # Test with API key
    success = test_gemini_connection()
    
    # Test fallback mode
    test_fallback_mode()
    
    if success:
        print("\n✅ Gemini integration is fully functional!")
        print("\nYou can now use:")
        print("  - python example_copilot_usage.py")
        print("  - uvicorn regression_manager.api_service:app --reload")
    else:
        print("\n⚠️  Set up GOOGLE_API_KEY to enable AI features")

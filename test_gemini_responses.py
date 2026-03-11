"""
Test Gemini responses to understand what format it's returning.
"""

import json
from dotenv import load_dotenv
from regression_manager.llm_copilot import RegressionCopilot

load_dotenv()


def test_simple_json_response():
    """Test if Gemini can return JSON."""
    print("\n" + "=" * 80)
    print("Testing Gemini JSON Response")
    print("=" * 80)
    
    copilot = RegressionCopilot()
    
    if not copilot.model:
        print("❌ Gemini not initialized. Check API key.")
        return
    
    print(f"✅ Gemini initialized: {copilot.model_name}")
    
    # Simple test prompt
    prompt = """
Analyze this test data and respond in JSON format:

Test: jk_ff_test_seed1
Coverage: 97.5%
Runtime: 145s
Pass Rate: 100%

Respond with JSON:
{
    "quality_score": <0-100>,
    "priority": "P0|P1|P2|P3",
    "recommendation": "brief recommendation"
}
"""
    
    print("\n📤 Sending prompt to Gemini...")
    response = copilot._call_llm(prompt, "You are a VLSI verification expert.")
    
    print(f"\n📥 Response received (length: {len(response)} chars)")
    print("\n" + "-" * 80)
    print("RAW RESPONSE:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    
    # Try to extract JSON
    print("\n🔍 Attempting JSON extraction...")
    
    # Remove markdown code blocks
    cleaned = response.replace('```json', '').replace('```', '').strip()
    
    # Find JSON
    start = cleaned.find('{')
    end = cleaned.rfind('}') + 1
    
    if start >= 0 and end > start:
        json_str = cleaned[start:end]
        print(f"\n✅ Found JSON (length: {len(json_str)} chars)")
        print("\nExtracted JSON:")
        print(json_str)
        
        try:
            parsed = json.loads(json_str)
            print("\n✅ Successfully parsed JSON:")
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON parse error: {e}")
    else:
        print("\n❌ No JSON found in response")


def test_complex_analysis():
    """Test more complex analysis prompt."""
    print("\n\n" + "=" * 80)
    print("Testing Complex Analysis")
    print("=" * 80)
    
    copilot = RegressionCopilot()
    
    if not copilot.model:
        print("❌ Gemini not initialized")
        return
    
    test_data = {
        'total_tests': 51,
        'coverage_range': {'min': 85.0, 'max': 100.0, 'mean': 95.5},
        'runtime_range': {'min': 145.0, 'max': 145.0, 'mean': 145.0}
    }
    
    prompt = f"""
You are a VLSI verification expert analyzing a regression test suite.

Test Suite Summary:
{json.dumps(test_data, indent=2)}

Analyze this test suite and provide:
1. Overall quality assessment
2. Key patterns you observe
3. Recommendations for optimization

Respond in JSON format:
{{
    "quality_score": <0-100>,
    "key_patterns": ["pattern1", "pattern2"],
    "recommendations": ["rec1", "rec2"]
}}
"""
    
    print("\n📤 Sending complex prompt...")
    response = copilot._call_llm(prompt, "You are a VLSI verification expert.")
    
    print(f"\n📥 Response received (length: {len(response)} chars)")
    print("\n" + "-" * 80)
    print("RAW RESPONSE:")
    print("-" * 80)
    print(response[:1000])  # First 1000 chars
    print("-" * 80)


if __name__ == '__main__':
    test_simple_json_response()
    test_complex_analysis()

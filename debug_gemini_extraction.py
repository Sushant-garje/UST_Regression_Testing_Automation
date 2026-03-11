"""
Debug Gemini JSON extraction.
"""

import json

# Sample response from Gemini (from the log)
response1 = """
{
  "quality_score": 25,
  "key_patterns": [
    "Most tests (at least the samples) run for the maximum observed duration of 145 seconds, suggesting a prevalence of long-running simulations or timeou"""

response2 = """
{
  "high_coverage_tests": [
    "jk_ff_test_seed16",
    "jk_ff_test_seed26",
    "jk_ff_test_seed23",
    "jk_ff_test_seed24",
    "jk_ff_test_seed13",
"""

# These are truncated in the log, but the actual response should be complete
# The issue is the logger is showing "Response preview" which is truncated

print("The issue is that the logger is showing truncated previews.")
print("The actual JSON extraction should work if the full response is there.")
print("\nLet's test with a complete JSON:")

complete_json = """{
  "quality_score": 75,
  "key_patterns": ["pattern1", "pattern2"],
  "recommendations": ["rec1", "rec2"]
}"""

# Remove markdown
cleaned = complete_json.replace('```json', '').replace('```', '').strip()

# Extract JSON
start = cleaned.find('{')
end = cleaned.rfind('}') + 1

if start >= 0 and end > start:
    json_str = cleaned[start:end]
    print(f"\nExtracted JSON string (length: {len(json_str)}):")
    print(json_str)
    
    try:
        result = json.loads(json_str)
        print("\n✅ Successfully parsed:")
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        print(f"\n❌ Parse error: {e}")

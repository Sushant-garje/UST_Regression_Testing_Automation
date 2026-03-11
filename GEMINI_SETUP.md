# Google Gemini Integration Setup Guide

## Quick Setup (3 Steps)

### Step 1: Get Your Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 2: Configure Environment

**Option A: Using .env file (Recommended)**

1. Open the `.env` file in the project root
2. Add your API key:
```
GOOGLE_API_KEY=your-api-key-here
```

**Option B: Using environment variable**

```bash
# Linux/Mac
export GOOGLE_API_KEY='your-api-key-here'

# Windows PowerShell
$env:GOOGLE_API_KEY='your-api-key-here'

# Windows CMD
set GOOGLE_API_KEY=your-api-key-here
```

### Step 3: Test Integration

```bash
python test_gemini_integration.py
```

You should see:
```
✅ API key found
✅ Gemini model initialized: gemini-2.5-flash
✅ Response received
✅ ALL TESTS PASSED - GEMINI INTEGRATION WORKING
```

---

## Using Gemini Features

### 1. Basic Chat

```python
from regression_manager.llm_copilot import RegressionCopilot

copilot = RegressionCopilot()  # Automatically loads from .env
response = copilot.chat("What are best practices for regression testing?")
print(response)
```

### 2. Analyze Regression Results

```python
from regression_manager import RegressionManagerAgent

agent = RegressionManagerAgent(
    csv_path='rag_training_data.csv',
    log_path='sim.log',
    enable_llm_copilot=True  # Enable AI features
)

result = agent.run()

# AI insights automatically included
if 'llm_insights' in result:
    print(result['llm_insights'])
```

### 3. Explain Test Scores

```python
copilot = RegressionCopilot()

explanation = copilot.explain_test_score({
    'testcase_id': 'cpu_test_1',
    'score': 0.87,
    'coverage': 95.0,
    'runtime_seconds': 145.0,
    'pass_rate': 0.92
})

print(explanation)
```

### 4. Get Critical Module Suggestions

```python
import pandas as pd

test_history = pd.read_csv('rag_training_data.csv')
critical_modules = copilot.suggest_critical_modules(test_history)
print(f"Suggested critical modules: {critical_modules}")
```

---

## API Usage with Gemini

### Start API Server

```bash
uvicorn regression_manager.api_service:app --reload
```

The API will automatically load the GOOGLE_API_KEY from .env

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/copilot/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "How can I reduce regression time by 30%?"
     }'
```

### Optimize with AI Insights

```bash
curl -X POST "http://localhost:8000/optimize-regression" \
     -H "Content-Type: application/json" \
     -d '{
       "csv_path": "rag_training_data.csv",
       "log_path": "sim.log",
       "enable_llm_copilot": true
     }'
```

---

## Troubleshooting

### Issue: "No Google API key provided"

**Solution:**
1. Check if `.env` file exists in project root
2. Verify `GOOGLE_API_KEY=your-key` is set (no spaces around =)
3. Make sure you're running from the project root directory

### Issue: "google.generativeai not installed"

**Solution:**
```bash
pip install google-generativeai
```

### Issue: API key not working

**Solution:**
1. Verify your API key is correct
2. Check if API key has proper permissions
3. Try generating a new API key from Google AI Studio

### Issue: Rate limit errors

**Solution:**
- Free tier has rate limits
- Wait a few seconds between requests
- Consider upgrading to paid tier for higher limits

---

## Features Available with Gemini

### ✅ Natural Language Analysis
Ask questions about your regression results in plain English

### ✅ Test Score Explanations
Get detailed explanations of why tests received certain scores

### ✅ Critical Module Suggestions
AI analyzes failure patterns and suggests which modules are critical

### ✅ Best Practice Recommendations
Get VLSI-specific advice and recommendations

### ✅ Interactive Chat
Have conversations about your verification workflow

### ✅ Context-Aware Responses
Copilot understands your test data and provides relevant insights

---

## Example Conversations

### Example 1: Optimization Advice

**You:** "How can I reduce my regression runtime by 30%?"

**Gemini:** "Based on VLSI regression best practices, here are strategies to reduce runtime by 30%:

1. **Redundancy Elimination**: Identify and exclude tests with >95% pass rate and <1% coverage gain
2. **Parallel Execution**: Distribute tests across CPU/GPU/Cloud resources
3. **Smart Prioritization**: Run high-coverage tests first for early failure detection
4. **Test Clustering**: Group similar tests to optimize resource allocation
5. **Coverage-Driven Selection**: Focus on tests that provide unique coverage

The Regression Manager Agent implements these strategies automatically."

### Example 2: Test Analysis

**You:** "Why did test cpu_core_test_1 get a score of 0.87?"

**Gemini:** "Test cpu_core_test_1 received a score of 0.87 because:

1. **High Coverage (95%)**: Provides excellent code coverage
2. **Reasonable Runtime (145s)**: Not too slow, good efficiency
3. **Good Stability (92% pass rate)**: Reliable but catches some bugs

The score reflects a balance of coverage value, execution efficiency, and test reliability. This is a high-priority test that should run early in your regression."

### Example 3: Module Prioritization

**You:** "Which modules should I mark as critical?"

**Gemini:** "Based on your test history, I recommend marking these as critical:

1. **cpu_core** - High failure rate (15%), core functionality
2. **memory_controller** - Frequent failures, impacts system stability
3. **interrupt_handler** - Critical for system operation
4. **cache_controller** - Performance-critical component

These modules show higher failure rates and are essential to system functionality. Marking them as critical will boost their test priority by 1.5x."

---

## Advanced Configuration

### Custom Model Settings

Edit `regression_manager/llm_copilot.py`:

```python
generation_config = {
    "temperature": 0.7,      # Creativity (0.0-1.0)
    "top_p": 0.95,          # Nucleus sampling
    "top_k": 40,            # Top-k sampling
    "max_output_tokens": 2048  # Response length
}
```

### Safety Settings

```python
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
```

---

## Cost Considerations

### Free Tier
- 60 requests per minute
- 1,500 requests per day
- Sufficient for most development and testing

### Paid Tier
- Higher rate limits
- More requests per day
- Better for production use

### Cost Optimization Tips
1. Cache common responses
2. Batch similar queries
3. Use fallback mode for non-critical features
4. Enable AI only when needed

---

## Fallback Mode

If no API key is provided, the system automatically uses rule-based fallback:

```python
copilot = RegressionCopilot(api_key=None)

# Still works, but uses rule-based analysis instead of AI
insights = copilot.analyze_regression_results(result)
```

This ensures the system works even without Gemini, though with less sophisticated insights.

---

## Security Best Practices

### ✅ DO:
- Store API key in .env file (not in code)
- Add .env to .gitignore
- Use environment variables in production
- Rotate API keys periodically

### ❌ DON'T:
- Commit API keys to version control
- Share API keys in documentation
- Hardcode API keys in source code
- Use same key across multiple projects

---

## Next Steps

1. ✅ Set up your API key in .env
2. ✅ Run test_gemini_integration.py
3. ✅ Try example_copilot_usage.py
4. ✅ Start using AI features in your workflow
5. ✅ Explore the chat interface
6. ✅ Integrate with your CI/CD pipeline

---

## Support

For Gemini-specific issues:
- Google AI Studio: https://ai.google.dev/
- API Documentation: https://ai.google.dev/docs
- Rate Limits: https://ai.google.dev/pricing

For integration issues:
- Check SETUP_GUIDE.md
- Run test_gemini_integration.py
- Review logs for error messages

---

**Ready to use Google Gemini AI for VLSI regression testing!** 🚀

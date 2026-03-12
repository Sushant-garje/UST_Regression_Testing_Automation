"""
LLM-powered Copilot for VLSI Regression Testing using Google Gemini.
Provides natural language interface and intelligent insights.
"""

import logging
import json
from typing import Dict, List, Optional
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class RegressionCopilot:
    """
    Gemini-powered copilot for regression testing insights.
    Provides natural language interface and recommendations.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize regression copilot with Google Gemini.
        
        Args:
            api_key: Google API key for Gemini (or set GOOGLE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.conversation_history = []
        self.model_name = "gemini-2.5-flash-lite"
        
        # Initialize Gemini client
        self._init_gemini_client()
    
    def _init_gemini_client(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
            
            if not self.api_key:
                logger.warning("No Google API key provided. Set GOOGLE_API_KEY environment variable.")
                self.client = None
                self.model = None
                return
            
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Initialize model with safety settings
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,  # Increased for longer responses
            }
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            self.client = genai
            logger.info(f"Initialized Google Gemini client ({self.model_name})")
            
        except ImportError:
            logger.warning("Google Generative AI not installed. Install with: pip install google-generativeai")
            self.client = None
            self.model = None
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None
            self.model = None
    
    def analyze_regression_results(self, results: Dict) -> str:
        """
        Analyze regression results and provide insights.
        
        Args:
            results: Regression optimization results
            
        Returns:
            Natural language analysis
        """
        if not self.client:
            return self._fallback_analysis(results)
        
        # Prepare context
        summary = results.get('summary', {})
        ranked_tests = results.get('ranked_tests', [])[:10]
        excluded_tests = results.get('excluded_tests', [])
        
        context = f"""
Regression Test Analysis:

Summary:
- Total Tests: {summary.get('total_tests', 0)}
- Selected Tests: {summary.get('selected', 0)}
- Excluded Tests: {summary.get('excluded', 0)}
- Optimization Ratio: {summary.get('optimization_ratio', 0):.1%}

Top 10 Priority Tests:
{json.dumps(ranked_tests, indent=2)}

Excluded Tests: {len(excluded_tests)}

Please provide:
1. Key insights about the regression suite
2. Potential issues or concerns
3. Recommendations for improvement
4. Resource optimization suggestions
"""
        
        try:
            system_context = "You are a VLSI regression testing expert. Analyze the following regression test results and provide actionable insights."
            response = self._call_llm(context, system_context)
            return response
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return self._fallback_analysis(results)
    
    def explain_test_score(self, test_data: Dict) -> str:
        """
        Explain why a test received its score.
        
        Args:
            test_data: Test information including score components
            
        Returns:
            Natural language explanation
        """
        if not self.client:
            return self._fallback_test_explanation(test_data)
        
        context = f"""
Test: {test_data.get('testcase_id', 'Unknown')}
Score: {test_data.get('score', 0):.4f}
Priority Rank: {test_data.get('priority_rank', 'N/A')}
Action: {test_data.get('action', 'N/A')}
Coverage: {test_data.get('coverage', 0):.2f}%
Runtime: {test_data.get('runtime_seconds', 0):.2f}s
Pass Rate: {test_data.get('pass_rate', 0):.2%}

Explain in simple terms why this test received this score and priority.
"""
        
        try:
            system_context = "You are a VLSI verification expert. Explain test scores in simple, technical terms."
            response = self._call_llm(context, system_context)
            return response
        except Exception as e:
            logger.error(f"Gemini explanation failed: {e}")
            return self._fallback_test_explanation(test_data)
    
    def suggest_critical_modules(self, test_history: pd.DataFrame) -> List[str]:
        """
        Suggest which modules should be marked as critical.
        
        Args:
            test_history: Historical test data
            
        Returns:
            List of suggested critical modules
        """
        if not self.client:
            return self._fallback_critical_modules(test_history)
        
        # Analyze failure patterns
        failure_by_module = test_history.groupby('module_name').agg({
            'pass_fail': ['sum', 'count', 'mean']
        }).reset_index()
        
        context = f"""
Module Failure Analysis:
{failure_by_module.to_string()}

Based on this data, which modules should be marked as critical for regression testing?
Consider:
1. Modules with high failure rates
2. Modules with frequent failures
3. Modules that are core to system functionality

Provide a list of 5-10 critical modules with brief justification.
"""
        
        try:
            system_context = "You are a VLSI verification expert. Analyze failure patterns and suggest critical modules."
            response = self._call_llm(context, system_context)
            # Extract module names from response
            modules = self._extract_module_names(response)
            return modules
        except Exception as e:
            logger.error(f"Gemini suggestion failed: {e}")
            return self._fallback_critical_modules(test_history)
    
    def chat(self, user_message: str, context: Optional[Dict] = None) -> str:
        """
        Chat interface for regression testing questions.
        
        Args:
            user_message: User's question or command
            context: Optional context (test results, configuration, etc.)
            
        Returns:
            Copilot response
        """
        if not self.client:
            return "LLM client not initialized. Please configure API key."
        
        # Build conversation context
        system_prompt = """You are a VLSI regression testing expert copilot. 
You help engineers optimize regression test suites, analyze coverage, 
allocate resources, and improve verification efficiency.

You have access to:
- Test execution history
- Coverage reports
- Resource utilization data
- Failure patterns

Provide concise, actionable advice."""
        
        # Add context if provided
        if context:
            context_str = f"\n\nCurrent Context:\n{json.dumps(context, indent=2)}"
            user_message = user_message + context_str
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        try:
            response = self._call_llm_chat(system_prompt, self.conversation_history)
            
            # Add response to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': response
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return f"Error: {str(e)}"
    
    def _call_llm(self, prompt: str, system_context: str = "") -> str:
        """Call Gemini with prompt."""
        if not self.model:
            return "Gemini not available. Please set GOOGLE_API_KEY."
        
        try:
            # Combine system context with prompt
            full_prompt = f"{system_context}\n\n{prompt}" if system_context else prompt
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            # Check if response was blocked or empty
            if not response.text:
                logger.warning("Empty response from Gemini")
                return ""
            
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API call failed: {error_msg}")
            
            # Check for quota errors
            if "quota" in error_msg.lower() or "429" in error_msg:
                logger.warning("⚠️ Gemini API quota exceeded. Using fallback mode.")
                return ""
            
            return ""
    
    def _call_llm_chat(self, system_prompt: str, messages: List[Dict]) -> str:
        """Call Gemini with conversation history."""
        if not self.model:
            return "Gemini not available. Please set GOOGLE_API_KEY."
        
        try:
            # Start chat session
            chat = self.model.start_chat(history=[])
            
            # Build conversation context
            conversation = f"{system_prompt}\n\n"
            for msg in messages:
                role = "User" if msg['role'] == 'user' else "Assistant"
                conversation += f"{role}: {msg['content']}\n\n"
            
            # Get response
            response = chat.send_message(conversation)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini chat failed: {e}")
            return f"Error in chat: {str(e)}"
    
    def _fallback_analysis(self, results: Dict) -> str:
        """Fallback analysis without LLM."""
        summary = results.get('summary', {})
        
        analysis = f"""
Regression Analysis (Rule-Based):

Total Tests: {summary.get('total_tests', 0)}
Selected: {summary.get('selected', 0)}
Excluded: {summary.get('excluded', 0)}
Optimization: {summary.get('optimization_ratio', 0):.1%}

Key Insights:
- {summary.get('excluded', 0)} tests were excluded as redundant
- Top priority tests should be run first for early failure detection
- Resource allocation can be optimized based on test complexity

Recommendations:
- Review excluded tests to ensure no critical tests were removed
- Monitor pass rates of high-priority tests
- Consider parallel execution for faster results
"""
        return analysis
    
    def _fallback_test_explanation(self, test_data: Dict) -> str:
        """Fallback test explanation without LLM."""
        score = test_data.get('score', 0)
        coverage = test_data.get('coverage', 0)
        runtime = test_data.get('runtime_seconds', 0)
        pass_rate = test_data.get('pass_rate', 0)
        
        explanation = f"""
Test Score Explanation:

Score: {score:.4f}

This test received this score based on:
1. Coverage: {coverage:.2f}% - {'High' if coverage > 90 else 'Medium' if coverage > 70 else 'Low'}
2. Runtime: {runtime:.2f}s - {'Fast' if runtime < 60 else 'Medium' if runtime < 300 else 'Slow'}
3. Pass Rate: {pass_rate:.2%} - {'Stable' if pass_rate > 0.9 else 'Unstable'}

Priority: {test_data.get('action', 'N/A')}
"""
        return explanation
    
    def _fallback_critical_modules(self, test_history: pd.DataFrame) -> List[str]:
        """Fallback critical module suggestion without LLM."""
        # Simple heuristic: modules with lowest pass rates
        if 'module_name' not in test_history.columns:
            return []
        
        module_stats = test_history.groupby('module_name')['pass_fail'].agg(['mean', 'count'])
        critical = module_stats[module_stats['mean'] < 0.8].sort_values('mean').head(5)
        
        return critical.index.tolist()
    
    def _extract_module_names(self, text: str) -> List[str]:
        """Extract module names from LLM response."""
        # Simple extraction - look for common module name patterns
        import re
        modules = re.findall(r'\b[a-z_]+(?:_[a-z]+)*\b', text.lower())
        # Filter to likely module names
        return [m for m in modules if len(m) > 3 and '_' in m][:10]

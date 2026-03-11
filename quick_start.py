"""
Quick Start Script for VLSI Regression Testing Copilot
Guides you through setup and first run with Google Gemini
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def check_dependencies():
    """Check if all dependencies are installed."""
    print_header("STEP 1: Checking Dependencies")
    
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('google-generativeai', 'google.generativeai'),
        ('python-dotenv', 'dotenv')
    ]
    
    missing = []
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - NOT INSTALLED")
            missing.append(display_name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def check_gemini_setup():
    """Check if Gemini API key is configured."""
    print_header("STEP 2: Checking Google Gemini Setup")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        print("\nTo set up Google Gemini:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Open the .env file in this directory")
        print("3. Add your key: GOOGLE_API_KEY=your-key-here")
        print("\nOr run: export GOOGLE_API_KEY='your-key-here'")
        print("\n⚠️  Continuing without AI features (fallback mode)")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test connection
    try:
        from regression_manager.llm_copilot import RegressionCopilot
        copilot = RegressionCopilot()
        
        if copilot.model:
            print(f"✅ Gemini model initialized: {copilot.model_name}")
            return True
        else:
            print("❌ Failed to initialize Gemini model")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def check_data_files():
    """Check if required data files exist."""
    print_header("STEP 3: Checking Data Files")
    
    required_files = {
        'rag_training_data.csv': 'Test data CSV',
        'sim.log': 'Simulation log (optional)'
    }
    
    all_found = True
    for file, description in required_files.items():
        if Path(file).exists():
            print(f"✅ {file} - {description}")
        else:
            print(f"⚠️  {file} - {description} - NOT FOUND")
            if file == 'rag_training_data.csv':
                all_found = False
    
    if not all_found:
        print("\n⚠️  Required data file missing: rag_training_data.csv")
        print("This file should contain your test execution history")
        return False
    
    return True


def run_basic_example():
    """Run basic regression optimization."""
    print_header("STEP 4: Running Basic Example")
    
    try:
        from regression_manager import RegressionManagerAgent
        
        print("Initializing Regression Manager Agent...")
        agent = RegressionManagerAgent(
            csv_path='rag_training_data.csv',
            log_path='sim.log' if Path('sim.log').exists() else None,
            enable_load_optimizer=True,
            enable_llm_copilot=bool(os.getenv('GOOGLE_API_KEY'))
        )
        
        print("Running optimization...")
        result = agent.run()
        
        print("\n✅ Optimization Complete!")
        print(f"\nResults:")
        print(f"  Total Tests: {result['summary']['total_tests']}")
        print(f"  Selected: {result['summary']['selected']}")
        print(f"  Excluded: {result['summary']['excluded']}")
        print(f"  Optimization Ratio: {result['summary']['optimization_ratio']:.1%}")
        
        if 'llm_insights' in result:
            print(f"\n🤖 AI Insights:")
            print(result['llm_insights'][:300] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running example: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_chat():
    """Test AI chat functionality."""
    print_header("STEP 5: Testing AI Chat (Optional)")
    
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  Skipping - No API key configured")
        return True
    
    try:
        from regression_manager.llm_copilot import RegressionCopilot
        
        copilot = RegressionCopilot()
        
        print("Asking Gemini: 'What is regression testing in VLSI?'")
        response = copilot.chat("What is regression testing in VLSI? Answer in 2 sentences.")
        
        print(f"\n🤖 Gemini Response:")
        print(response)
        
        print("\n✅ AI chat working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def show_next_steps():
    """Show next steps for the user."""
    print_header("Next Steps")
    
    print("✅ Setup complete! Here's what you can do next:\n")
    
    print("1. Run full example with AI features:")
    print("   python example_copilot_usage.py\n")
    
    print("2. Start the API server:")
    print("   uvicorn regression_manager.api_service:app --reload\n")
    
    print("3. Test Gemini integration:")
    print("   python test_gemini_integration.py\n")
    
    print("4. Interactive Python session:")
    print("   python")
    print("   >>> from regression_manager.llm_copilot import RegressionCopilot")
    print("   >>> copilot = RegressionCopilot()")
    print("   >>> copilot.chat('How can I optimize my regression suite?')\n")
    
    print("5. Read documentation:")
    print("   - GEMINI_SETUP.md - Gemini integration guide")
    print("   - SETUP_GUIDE.md - Complete setup guide")
    print("   - COMPLETE_SOLUTION_GUIDE.md - Full solution documentation\n")
    
    print("6. Configure for your environment:")
    print("   - Edit .env file for API keys and settings")
    print("   - Edit regression_manager/config.py for scoring weights\n")


def main():
    """Main quick start flow."""
    print("\n" + "🚀" * 40)
    print("  VLSI REGRESSION TESTING COPILOT - QUICK START")
    print("🚀" * 40)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Check Gemini setup
    gemini_available = check_gemini_setup()
    
    # Step 3: Check data files
    if not check_data_files():
        print("\n❌ Please ensure rag_training_data.csv is in the current directory")
        sys.exit(1)
    
    # Step 4: Run basic example
    if not run_basic_example():
        print("\n❌ Basic example failed. Check error messages above.")
        sys.exit(1)
    
    # Step 5: Test AI chat (if available)
    if gemini_available:
        test_ai_chat()
    
    # Show next steps
    show_next_steps()
    
    print("\n" + "=" * 80)
    print("  ✅ QUICK START COMPLETE!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()

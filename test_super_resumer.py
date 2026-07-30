"""
Super Resumer Incremental Testing Script
Tests each component individually to identify issues
"""

import sys
import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SuperResumerTester:
    """Incremental tester for Super Resumer components."""
    
    def __init__(self):
        self.test_results = []
        self.essential_imports = []
        
    def record_test(self, test_name: str, passed: bool, message: str = ""):
        """Record a test result."""
        result = {
            "test": test_name,
            "passed": passed,
            "message": message
        }
        self.test_results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status}: {test_name} - {message}")
        
    def test_1_basic_imports(self):
        """Test 1: Basic Python imports"""
        logger.info("=" * 50)
        logger.info("TEST 1: Basic Imports")
        logger.info("=" * 50)
        
        try:
            import streamlit
            self.record_test("Streamlit import", True)
            self.essential_imports.append("streamlit")
        except ImportError as e:
            self.record_test("Streamlit import", False, str(e))
            
        try:
            import pandas
            self.record_test("Pandas import", True)
            self.essential_imports.append("pandas")
        except ImportError as e:
            self.record_test("Pandas import", False, str(e))
            
        try:
            import requests
            self.record_test("Requests import", True)
            self.essential_imports.append("requests")
        except ImportError as e:
            self.record_test("Requests import", False, str(e))
            
        try:
            import dotenv
            self.record_test("Python-dotenv import", True)
            self.essential_imports.append("dotenv")
        except ImportError as e:
            self.record_test("Python-dotenv import", False, str(e))
    
    def test_2_langchain_imports(self):
        """Test 2: LangChain and AI imports"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 2: LangChain and AI Imports")
        logger.info("=" * 50)
        
        try:
            import langchain
            self.record_test("LangChain import", True)
            self.essential_imports.append("langchain")
        except ImportError as e:
            self.record_test("LangChain import", False, str(e))
            
        try:
            from langchain.embeddings import OpenAIEmbeddings
            self.record_test("OpenAI Embeddings import", True)
        except ImportError as e:
            self.record_test("OpenAI Embeddings import", False, str(e))
            
        try:
            from langchain.vectorstores import FAISS
            self.record_test("FAISS import", True)
        except ImportError as e:
            self.record_test("FAISS import", False, str(e))
            
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            self.record_test("Text Splitter import", True)
        except ImportError as e:
            self.record_test("Text Splitter import", False, str(e))
            
        try:
            from langchain.chat_models import ChatOpenAI
            self.record_test("ChatOpenAI import", True)
        except ImportError as e:
            self.record_test("ChatOpenAI import", False, str(e))
            
        try:
            from langgraph.graph import StateGraph
            self.record_test("LangGraph StateGraph import", True)
        except ImportError as e:
            self.record_test("LangGraph StateGraph import", False, str(e))
    
    def test_3_environment_setup(self):
        """Test 3: Environment variables and configuration"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 3: Environment Setup")
        logger.info("=" * 50)
        
        # Test .env file exists
        if os.path.exists('.env'):
            self.record_test(".env file exists", True)
        else:
            self.record_test(".env file exists", False, "Create .env file with API keys")
            
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test API keys
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key and openrouter_key != "your_openrouter_api_key_here":
            self.record_test("OpenRouter API key configured", True)
        else:
            self.record_test("OpenRouter API key configured", False, "Add OPENROUTER_API_KEY to .env")
            
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key_here":
            self.record_test("OpenAI API key configured", True)
        else:
            self.record_test("OpenAI API key configured", False, "Optional fallback")
    
    def test_4_resume_files(self):
        """Test 4: Resume file access"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 4: Resume Files")
        logger.info("=" * 50)
        
        from core.config import Settings
        
        config = Settings()
        
        # Test C# resume
        if os.path.exists(config.RESUME_C_SHARP):
            self.record_test(f"C# resume exists: {config.RESUME_C_SHARP}", True)
            # Test if readable
            try:
                with open(config.RESUME_C_SHARP, 'r') as f:
                    content = f.read()
                if len(content) > 100:
                    self.record_test("C# resume readable and has content", True)
                else:
                    self.record_test("C# resume readable and has content", False, "Resume seems too short")
            except Exception as e:
                self.record_test("C# resume readable", False, str(e))
        else:
            self.record_test(f"C# resume exists: {config.RESUME_C_SHARP}", False, "File not found")
            
        # Test Python AI resume
        if os.path.exists(config.RESUME_PYTHON_AI):
            self.record_test(f"Python AI resume exists: {config.RESUME_PYTHON_AI}", True)
            try:
                with open(config.RESUME_PYTHON_AI, 'r') as f:
                    content = f.read()
                if len(content) > 100:
                    self.record_test("Python AI resume readable and has content", True)
                else:
                    self.record_test("Python AI resume readable and has content", False, "Resume seems too short")
            except Exception as e:
                self.record_test("Python AI resume readable", False, str(e))
        else:
            self.record_test(f"Python AI resume exists: {config.RESUME_PYTHON_AI}", False, "File not found")
    
    def test_5_config_loading(self):
        """Test 5: Configuration loading"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 5: Configuration Loading")
        logger.info("=" * 50)
        
        try:
            from core.config import Settings
            config = Settings()
            
            self.record_test("Config class import", True)
            
            # Test config values
            if config.LOCATION == "Bangalore":
                self.record_test("Location configured correctly", True)
            else:
                self.record_test("Location configured correctly", False, f"Expected Bangalore, got {config.LOCATION}")
                
            if config.MIN_SALARY_LPA == 7:
                self.record_test("Min salary configured correctly", True)
            else:
                self.record_test("Min salary configured correctly", False, f"Expected 7, got {config.MIN_SALARY_LPA}")
                
            if config.MATCH_THRESHOLD == 85:
                self.record_test("Match threshold configured correctly", True)
            else:
                self.record_test("Match threshold configured correctly", False, f"Expected 85, got {config.MATCH_THRESHOLD}")
                
        except Exception as e:
            self.record_test("Config loading", False, str(e))
    
    def test_6_resume_loading(self):
        """Test 6: Resume loading and processing"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 6: Resume Loading and Processing")
        logger.info("=" * 50)
        
        try:
            from core.config import Settings
            from agents.super_resumer_matcher import SuperResumerMatcher
            
            config = Settings()
            matcher = SuperResumerMatcher(config)
            
            self.record_test("Matcher initialization", True)
            
            # Test resume loading
            csharp_text = matcher.load_resume(config.RESUME_C_SHARP)
            if csharp_text and len(csharp_text) > 100:
                self.record_test("C# resume loaded successfully", True)
            else:
                self.record_test("C# resume loaded successfully", False, f"Loaded {len(csharp_text)} characters")
                
            python_text = matcher.load_resume(config.RESUME_PYTHON_AI)
            if python_text and len(python_text) > 100:
                self.record_test("Python AI resume loaded successfully", True)
            else:
                self.record_test("Python AI resume loaded successfully", False, f"Loaded {len(python_text)} characters")
                
        except Exception as e:
            self.record_test("Resume loading", False, str(e))
    
    def test_7_vector_store_creation(self):
        """Test 7: Vector store creation (requires API key)"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 7: Vector Store Creation")
        logger.info("=" * 50)
        
        try:
            from core.config import Settings
            from agents.super_resumer_matcher import SuperResumerMatcher
            from dotenv import load_dotenv
            import os
            
            load_dotenv()
            config = Settings()
            
            if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_openrouter_api_key_here":
                self.record_test("Vector store creation", False, "OpenRouter API key not configured")
                return
                
            matcher = SuperResumerMatcher(config)
            matcher.load_resumes()
            
            if matcher.csharp_vectorstore:
                self.record_test("C# vector store created", True)
            else:
                self.record_test("C# vector store created", False, "Vector store is None")
                
            if matcher.python_vectorstore:
                self.record_test("Python AI vector store created", True)
            else:
                self.record_test("Python AI vector store created", False, "Vector store is None")
                
        except Exception as e:
            self.record_test("Vector store creation", False, str(e))
    
    def test_8_simple_job_matching(self):
        """Test 8: Simple job matching without API"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 8: Simple Job Matching (without API)")
        logger.info("=" * 50)
        
        try:
            from core.config import Settings
            from agents.super_resumer_matcher import SuperResumerMatcher
            
            config = Settings()
            matcher = SuperResumerMatcher(config)
            
            # Test tech stack detection
            csharp_job = "Looking for C# developer with .NET and Azure experience"
            python_job = "Seeking Python AI engineer with TensorFlow and PyTorch experience"
            
            csharp_stack = matcher.detect_tech_stack(csharp_job)
            if csharp_stack == 'csharp':
                self.record_test("C# tech stack detection", True)
            else:
                self.record_test("C# tech stack detection", False, f"Detected {csharp_stack}")
                
            python_stack = matcher.detect_tech_stack(python_job)
            if python_stack == 'python_ai':
                self.record_test("Python AI tech stack detection", True)
            else:
                self.record_test("Python AI tech stack detection", False, f"Detected {python_stack}")
                
        except Exception as e:
            self.record_test("Tech stack detection", False, str(e))
    
    def test_9_dashboard_components(self):
        """Test 9: Dashboard component imports"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 9: Dashboard Components")
        logger.info("=" * 50)
        
        try:
            from ui.super_resumer_dashboard import SuperResumerDashboard
            self.record_test("Dashboard class import", True)
            
            # Test basic initialization (without rendering)
            dashboard = SuperResumerDashboard()
            self.record_test("Dashboard initialization", True)
            
        except Exception as e:
            self.record_test("Dashboard components", False, str(e))
    
    def test_10_orchestrator_components(self):
        """Test 10: Orchestrator components"""
        logger.info("\n" + "=" * 50)
        logger.info("TEST 10: Orchestrator Components")
        logger.info("=" * 50)
        
        try:
            from core.config import Settings
            from core.super_resumer_orchestrator import SuperResumerOrchestrator
            
            config = Settings()
            
            # Test basic initialization (without full workflow)
            orchestrator = SuperResumerOrchestrator(config)
            self.record_test("Orchestrator initialization", True)
            
        except Exception as e:
            self.record_test("Orchestrator components", False, str(e))
    
    def print_summary(self):
        """Print test summary."""
        logger.info("\n" + "=" * 50)
        logger.info("TEST SUMMARY")
        logger.info("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['passed']])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        
        if failed_tests > 0:
            logger.info("\n" + "=" * 50)
            logger.info("FAILED TESTS:")
            logger.info("=" * 50)
            for result in self.test_results:
                if not result['passed']:
                    logger.info(f"❌ {result['test']}: {result['message']}")
        
        logger.info("\n" + "=" * 50)
        if failed_tests == 0:
            logger.info("🎉 All tests passed! Application should work without errors.")
        else:
            logger.info(f"⚠️  {failed_tests} test(s) failed. Please fix these issues.")
            logger.info("Run: pip install -r requirements.txt")
            logger.info("Ensure .env file has valid API keys")
            logger.info("Ensure resume files exist and have content")
        logger.info("=" * 50)
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Run all tests sequentially."""
        logger.info("🧪 Starting Super Resumer Incremental Tests")
        logger.info("=" * 50)
        
        self.test_1_basic_imports()
        self.test_2_langchain_imports()
        self.test_3_environment_setup()
        self.test_4_resume_files()
        self.test_5_config_loading()
        self.test_6_resume_loading()
        self.test_7_vector_store_creation()
        self.test_8_simple_job_matching()
        self.test_9_dashboard_components()
        self.test_10_orchestrator_components()
        
        return self.print_summary()


def main():
    """Main function to run tests."""
    tester = SuperResumerTester()
    all_passed = tester.run_all_tests()
    
    if all_passed:
        logger.info("\n✅ Your application should work without errors!")
        logger.info("Run: streamlit run run_super_resumer.py")
    else:
        logger.info("\n❌ Please fix the failed tests before running the application.")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Script to pre-load and cache the OpenAI model on application startup.

This script is run during Docker container initialization to:
1. Validate configuration
2. Initialize LangChain components
3. Test model connection
4. Cache model for faster responses

This ensures the model is loaded ONCE and cached for all subsequent requests.
"""

import os
import sys
import django

# Add project root to Python path
sys.path.insert(0, '/app')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from dotenv import load_dotenv
from chatbot.utils.config import Config
from chatbot.utils.langchain_utils import LangChainFactory, test_llm_connection

# Load environment variables
load_dotenv()


def validate_configuration():
    """
    Validates all required configuration.
    
    Returns:
        bool: True if configuration is valid.
    """
    print("\n" + "="*60)
    print(" STEP 1: Validating Configuration")
    print("="*60)
    
    config = Config.validate_configuration()
    
    if not config['is_valid']:
        print("\n Configuration validation failed!")
        for error in config['errors']:
            print(f"   • {error}")
        return False
    
    # Print configuration summary
    Config.print_configuration()
    
    return True


def initialize_langchain():
    """
    Initializes LangChain components.
    
    Returns:
        bool: True if initialization successful.
    """
    print("\n" + "="*60)
    print("STEP 2: Initializing LangChain Components")
    print("="*60)
    
    try:
        # Create LLM instance (will be cached)
        print("   Creating ChatOpenAI instance...")
        llm = LangChainFactory.create_llm()
        print(f"LLM initialized: {llm.model_name}")
        
        # Create memory instance
        print("   Creating ConversationBufferMemory...")
        memory = LangChainFactory.create_memory()
        print("Memory initialized")
        
        # Create prompt template
        print("   Creating PromptTemplate...")
        prompt = LangChainFactory.create_text_prompt()
        print("Prompt template created")
        
        return True
        
    except Exception as e:
        print(f"\n LangChain initialization failed: {str(e)}")
        return False


def test_model_connection():
    """
    Tests the model connection with a simple query.
    
    Returns:
        bool: True if connection test successful.
    """
    print("\n" + "="*60)
    print("STEP 3: Testing Model Connection")
    print("="*60)
    
    print("   Sending test query to OpenAI...")
    
    if test_llm_connection():
        print("Model connection successful!")
        return True
    else:
        print("Model connection failed!")
        return False


def initialize_dag():
    """
    Initializes the LangGraph DAG workflow.
    
    Returns:
        bool: True if DAG initialization successful.
    """
    print("\n" + "="*60)
    print("STEP 4: Initializing LangGraph DAG")
    print("="*60)
    
    try:
        from chatbot.workflows.chatbot_graph import get_chatbot_dag
        
        print("   Building DAG workflow...")
        dag = get_chatbot_dag()
        print("DAG initialized and cached!")
        
        # Print DAG visualization
        print(dag.visualize_dag())
        
        return True
        
    except Exception as e:
        print(f"\n DAG initialization failed: {str(e)}")
        return False


def main():
    """
    Main function to orchestrate model loading.
    """
    print("\n" + "*" * 30)
    print(" SMART CHATBOT - MODEL INITIALIZATION")
    print("*" * 30)
    
    # Step 1: Validate configuration
    if not validate_configuration():
        print("\n Startup failed: Invalid configuration")
        sys.exit(1)
    
    # Step 2: Initialize LangChain components
    if not initialize_langchain():
        print("\n Startup failed: LangChain initialization error")
        sys.exit(1)
    
    # Step 3: Test model connection
    if not test_model_connection():
        print("\n Warning: Model connection test failed")
        print("   The application will start but may not work properly.")
        print("   Please check your OPENAI_API_KEY and internet connection.")
    
    # Step 4: Initialize DAG
    if not initialize_dag():
        print("\nStartup failed: DAG initialization error")
        sys.exit(1)
    
    # Success!
    print("\n" + "*" * 30)
    print("MODEL LOADED AND CACHED SUCCESSFULLY!")
    print("*" * 30)
    print("\n Application is ready to serve requests!")
    print("   All components initialized and cached.")
    print("   Subsequent requests will use cached model for faster responses.\n")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
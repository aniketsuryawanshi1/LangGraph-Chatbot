"""
LangChain utilities for initializing and managing LLM components.

This module provides helper functions to initialize LangChain components
with proper configuration and caching.
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from .config import Config


class LangChainFactory:
    """
    Factory class for creating LangChain components.
    Uses static methods to create properly configured instances.
    """
    
    # Class-level cache for LLM instance (singleton pattern)
    _llm_instance: Optional[ChatOpenAI] = None
    
    @staticmethod
    def create_llm(
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        force_new: bool = False
    ) -> ChatOpenAI:
        """
        Creates and caches a ChatOpenAI instance.
        Returns cached instance on subsequent calls unless force_new=True.
        
        Args:
            temperature: Model temperature (0-1). Uses config default if None.
            max_tokens: Maximum tokens in response. Uses config default if None.
            force_new: If True, creates new instance instead of using cache.
            
        Returns:
            ChatOpenAI: Configured ChatOpenAI instance.
            
        Example:
            >>> llm = LangChainFactory.create_llm()
            >>> response = llm.invoke("Hello!")
        """
        # Return cached instance if available and not forcing new
        if LangChainFactory._llm_instance is not None and not force_new:
            return LangChainFactory._llm_instance
        
        # Get configuration
        api_key = Config.get_openai_api_key()
        model_name = Config.get_model_name()
        
        # Use provided values or fall back to config defaults
        if temperature is None:
            temperature = Config.get_model_temperature()
        if max_tokens is None:
            max_tokens = Config.get_max_tokens()
        
        # Create LLM instance with configuration
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            max_tokens=max_tokens,
            cache=Config.get_cache_enabled()
        )
        
        # Cache the instance
        LangChainFactory._llm_instance = llm
        
        return llm
    
    @staticmethod
    def create_memory(
        memory_key: str = "chat_history",
        return_messages: bool = True
    ) -> ConversationBufferMemory:
        """
        Creates a ConversationBufferMemory instance for storing chat history.
        
        Args:
            memory_key: Key to store memory under (default: "chat_history").
            return_messages: Whether to return as message objects (default: True).
            
        Returns:
            ConversationBufferMemory: Configured memory instance.
            
        Example:
            >>> memory = LangChainFactory.create_memory()
            >>> memory.save_context({"input": "Hi"}, {"output": "Hello!"})
        """
        return ConversationBufferMemory(
            memory_key=memory_key,
            return_messages=return_messages
        )
    
    @staticmethod
    def create_text_prompt() -> PromptTemplate:
        """
        Creates a PromptTemplate for text-based conversations.
        
        Returns:
            PromptTemplate: Configured prompt template for text queries.
            
        Example:
            >>> prompt = LangChainFactory.create_text_prompt()
            >>> formatted = prompt.format(user_query="Hello", chat_history="")
        """
        return PromptTemplate(
            input_variables=["user_query", "chat_history"],
            template="""You are a helpful and friendly AI assistant. Based on the conversation history and the user's current query, provide a clear, informative, and helpful response.

Chat History:
{chat_history}

User Query: {user_query}

Assistant Response:"""
        )
    
    @staticmethod
    def create_calculation_prompt() -> PromptTemplate:
        """
        Creates a PromptTemplate for calculation-based queries.
        
        Returns:
            PromptTemplate: Configured prompt template for calculations.
        """
        return PromptTemplate(
            input_variables=["expression", "result"],
            template="""The user asked for a calculation.

Expression: {expression}
Result: {result}

Provide a clear and friendly response explaining the calculation result."""
        )
    
    @staticmethod
    def clear_llm_cache() -> None:
        """
        Clears the cached LLM instance.
        Useful for testing or when configuration changes.
        """
        LangChainFactory._llm_instance = None
    
    @staticmethod
    def get_llm_info() -> dict:
        """
        Gets information about the current LLM instance.
        
        Returns:
            dict: Dictionary containing LLM configuration details.
        """
        if LangChainFactory._llm_instance is None:
            return {
                'initialized': False,
                'model': None,
                'temperature': None
            }
        
        llm = LangChainFactory._llm_instance
        return {
            'initialized': True,
            'model': llm.model_name,
            'temperature': llm.temperature,
            'max_tokens': llm.max_tokens,
            'cache_enabled': hasattr(llm, 'cache') and llm.cache
        }


def initialize_langchain_components() -> tuple[ChatOpenAI, ConversationBufferMemory, PromptTemplate]:
    """
    Convenience function to initialize all core LangChain components at once.
    
    Returns:
        tuple: (llm, memory, prompt_template)
        
    Example:
        >>> llm, memory, prompt = initialize_langchain_components()
    """
    llm = LangChainFactory.create_llm()
    memory = LangChainFactory.create_memory()
    prompt = LangChainFactory.create_text_prompt()
    
    return llm, memory, prompt


def test_llm_connection() -> bool:
    """
    Tests the LLM connection with a simple query.
    
    Returns:
        bool: True if connection successful, False otherwise.
        
    Example:
        >>> if test_llm_connection():
        ...     print("LLM is ready!")
    """
    try:
        llm = LangChainFactory.create_llm()
        response = llm.invoke("Say 'OK' if you're working.")
        return bool(response.content)
    except Exception as e:
        print(f"LLM connection test failed: {str(e)}")
        return False
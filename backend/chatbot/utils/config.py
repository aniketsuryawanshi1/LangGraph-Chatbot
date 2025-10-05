"""
Configuration utilities for the chatbot application.

This module provides helper functions to retrieve and validate
configuration values from environment variables and Django settings.
"""

import os
from typing import Optional
from django.conf import settings


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


class Config:
    """
    Configuration helper class with static methods.
    Provides centralized access to all configuration values.
    """
    
    @staticmethod
    def get_openai_api_key() -> str:
        """
        Retrieves the OpenAI API key from environment variables.
        
        Returns:
            str: The OpenAI API key.
            
        Raises:
            ConfigError: If API key is not found or is empty.
        """
        api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)
        
        if not api_key:
            raise ConfigError(
                "OPENAI_API_KEY not found in environment variables or settings. "
                "Please set it in your .env file."
            )
        
        return api_key
    
    @staticmethod
    def get_model_name() -> str:
        """
        Retrieves the OpenAI model name from environment variables.
        
        Returns:
            str: The model name (defaults to 'gpt-3.5-turbo').
        """
        return os.getenv('MODEL') or getattr(settings, 'MODEL_NAME', 'gpt-3.5-turbo')
    
    @staticmethod
    def get_model_temperature() -> float:
        """
        Retrieves the model temperature setting.
        
        Returns:
            float: Temperature value between 0 and 1 (default: 0.7).
        """
        temp_str = os.getenv('MODEL_TEMPERATURE', '0.7')
        try:
            temperature = float(temp_str)
            # Validate temperature range
            if not 0 <= temperature <= 1:
                raise ValueError("Temperature must be between 0 and 1")
            return temperature
        except (ValueError, TypeError):
            return 0.7  # Default fallback
    
    @staticmethod
    def get_cache_enabled() -> bool:
        """
        Checks if caching is enabled.
        
        Returns:
            bool: True if caching is enabled (default: True).
        """
        cache_enabled = os.getenv('CACHE_ENABLED', 'True')
        return cache_enabled.lower() in ('true', '1', 'yes')
    
    @staticmethod
    def get_cache_directory() -> str:
        """
        Retrieves the cache directory path.
        
        Returns:
            str: Path to the cache directory.
        """
        return os.getenv('CACHE_DIR') or getattr(settings, 'CACHE_DIR', '/app/cache')
    
    @staticmethod
    def get_max_tokens() -> Optional[int]:
        """
        Retrieves the maximum tokens setting for model responses.
        
        Returns:
            Optional[int]: Maximum tokens or None for unlimited.
        """
        max_tokens = os.getenv('MAX_TOKENS')
        if max_tokens:
            try:
                return int(max_tokens)
            except (ValueError, TypeError):
                pass
        return None
    
    @staticmethod
    def validate_configuration() -> dict:
        """
        Validates all required configuration values.
        
        Returns:
            dict: Dictionary containing validation results and config values.
            
        Example:
            >>> config = Config.validate_configuration()
            >>> print(config['is_valid'])
            True
        """
        errors = []
        config = {}
        
        # Validate API key
        try:
            config['api_key'] = Config.get_openai_api_key()
        except ConfigError as e:
            errors.append(str(e))
            config['api_key'] = None
        
        # Get other configuration values
        config['model_name'] = Config.get_model_name()
        config['temperature'] = Config.get_model_temperature()
        config['cache_enabled'] = Config.get_cache_enabled()
        config['cache_dir'] = Config.get_cache_directory()
        config['max_tokens'] = Config.get_max_tokens()
        
        config['is_valid'] = len(errors) == 0
        config['errors'] = errors
        
        return config
    
    @staticmethod
    def print_configuration() -> None:
        """
        Prints the current configuration (useful for debugging).
        Masks sensitive information like API keys.
        """
        config = Config.validate_configuration()
        
        print("=" * 60)
        print(" Configuration Summary")
        print("=" * 60)
        
        if config['api_key']:
            # Mask API key for security
            masked_key = config['api_key'][:8] + "*" * 20 + config['api_key'][-4:]
            print(f"API Key: {masked_key}")
        else:
            print("API Key:  NOT SET")
        
        print(f"Model Name: {config['model_name']}")
        print(f"Temperature: {config['temperature']}")
        print(f"Cache Enabled: {config['cache_enabled']}")
        print(f"Cache Directory: {config['cache_dir']}")
        print(f"Max Tokens: {config['max_tokens'] or 'Unlimited'}")
        
        if config['errors']:
            print("\nConfiguration Errors:")
            for error in config['errors']:
                print(f"   - {error}")
        else:
            print("\nConfiguration Valid!")
        
        print("=" * 60)


def get_openai_config() -> tuple[str, str]:
    """
    Convenience function to get API key and model name together.
    
    Returns:
        tuple[str, str]: A tuple of (api_key, model_name).
        
    Raises:
        ConfigError: If configuration is invalid.
    """
    api_key = Config.get_openai_api_key()
    model_name = Config.get_model_name()
    return api_key, model_name
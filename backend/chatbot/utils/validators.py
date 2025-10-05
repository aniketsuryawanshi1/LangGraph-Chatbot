"""
Input validators for the chatbot application.

This module provides validation functions for user inputs,
queries, and other data that needs validation.
"""

import re
from typing import Optional, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class QueryValidator:
    """
    Validator class for user queries.
    Uses static methods for stateless validation.
    """
    
    # Maximum query length
    MAX_QUERY_LENGTH = 5000
    MIN_QUERY_LENGTH = 1
    
    @staticmethod
    def validate_query(query: str) -> Tuple[bool, Optional[str]]:
        """
        Validates a user query.
        
        Args:
            query: The user's input query string.
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
            
        Example:
            >>> is_valid, error = QueryValidator.validate_query("Hello")
            >>> if not is_valid:
            ...     print(error)
        """
        # Check if query is None or not a string
        if query is None:
            return False, "Query cannot be None"
        
        if not isinstance(query, str):
            return False, "Query must be a string"
        
        # Strip whitespace
        query = query.strip()
        
        # Check minimum length
        if len(query) < QueryValidator.MIN_QUERY_LENGTH:
            return False, "Query is too short"
        
        # Check maximum length
        if len(query) > QueryValidator.MAX_QUERY_LENGTH:
            return False, f"Query is too long (max {QueryValidator.MAX_QUERY_LENGTH} characters)"
        
        # Check for potentially harmful content (basic sanitization)
        if QueryValidator._contains_harmful_content(query):
            return False, "Query contains potentially harmful content"
        
        return True, None
    
    @staticmethod
    def _contains_harmful_content(query: str) -> bool:
        """
        Checks for potentially harmful content in query.
        
        Args:
            query: The query string to check.
            
        Returns:
            bool: True if harmful content detected.
        """
        # Basic checks for SQL injection, XSS, etc.
        harmful_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS attempts
            r'javascript:',  # JavaScript protocol
            r'on\w+\s*=',  # Event handlers
        ]
        
        query_lower = query.lower()
        return any(re.search(pattern, query_lower, re.IGNORECASE) for pattern in harmful_patterns)
    
    @staticmethod
    def is_calculation_query(query: str) -> bool:
        """
        Determines if a query is a calculation request.
        
        Args:
            query: The user's query string.
            
        Returns:
            bool: True if query appears to be a calculation request.
            
        Example:
            >>> QueryValidator.is_calculation_query("What is 5 + 3?")
            True
        """
        query_lower = query.lower()
        
        # Patterns that indicate calculation
        calculation_indicators = [
            r'\d+\s*[\+\-\*\/\^\%\(\)]\s*\d+',  # Math operations
            r'\bcalculate\b',
            r'\bcompute\b',
            r'\bsolve\b',
            r'\bwhat is \d+',
            r'\bmath\b',
            r'\bsum of\b',
            r'\bproduct of\b',
            r'\bdifference\b',
            r'\bquotient\b',
        ]
        
        return any(re.search(pattern, query_lower) for pattern in calculation_indicators)
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """
        Sanitizes a user query by removing potentially harmful content.
        
        Args:
            query: The query to sanitize.
            
        Returns:
            str: Sanitized query string.
        """
        # Remove HTML tags
        query = re.sub(r'<[^>]+>', '', query)
        
        # Remove excessive whitespace
        query = re.sub(r'\s+', ' ', query)
        
        # Strip leading/trailing whitespace
        query = query.strip()
        
        return query


class SessionValidator:
    """
    Validator for session-related data.
    """
    
    @staticmethod
    def validate_session_id(session_id: Optional[str]) -> Tuple[bool, Optional[str]]:
        """
        Validates a session ID.
        
        Args:
            session_id: The session identifier.
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not session_id:
            return False, "Session ID is required"
        
        if not isinstance(session_id, str):
            return False, "Session ID must be a string"
        
        # Check length (UUIDs are typically 36 characters)
        if len(session_id) > 255:
            return False, "Session ID is too long"
        
        # Check for valid characters (alphanumeric and hyphens)
        if not re.match(r'^[a-zA-Z0-9\-_]+$', session_id):
            return False, "Session ID contains invalid characters"
        
        return True, None


def validate_and_sanitize_query(query: str) -> str:
    """
    Convenience function to validate and sanitize a query in one step.
    
    Args:
        query: The user's query string.
        
    Returns:
        str: Sanitized query string.
        
    Raises:
        ValidationError: If validation fails.
        
    Example:
        >>> clean_query = validate_and_sanitize_query(user_input)
    """
    # Validate
    is_valid, error = QueryValidator.validate_query(query)
    if not is_valid:
        raise ValidationError(error)
    
    # Sanitize
    return QueryValidator.sanitize_query(query)
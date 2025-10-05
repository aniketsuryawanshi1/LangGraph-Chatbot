"""
Main chatbot service layer.

This service orchestrates the entire chatbot workflow:
- Receives user queries
- Processes through LangGraph DAG
- Manages conversation history
- Saves to database
"""

import uuid
from typing import Dict, Optional
from chatbot.workflows.chatbot_graph import get_chatbot_dag
from chatbot.services.cache_service import CacheService
from chatbot.services.message_service import MessageService
from chatbot.utils.validators import validate_and_sanitize_query, ValidationError


class ChatbotService:
    """
    Main service for chatbot operations.
    Coordinates between DAG workflow, caching, and database.
    """
    
    @staticmethod
    def process_chat_message(
        user_query: str,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Processes a user chat message through the entire workflow.
        
        This is the main entry point for chat operations.
        
        Workflow:
        1. Validate and sanitize input
        2. Generate or retrieve session ID
        3. Get conversation history from cache/database
        4. Process through LangGraph DAG
        5. Save to database
        6. Update cache
        7. Return response
        
        Args:
            user_query: The user's input message.
            session_id: Optional session ID (generated if not provided).
            
        Returns:
            Dict: Response containing:
                - success: bool
                - session_id: str
                - response: str
                - query_type: str
                - error: str (if any)
                
        Example:
            >>> result = ChatbotService.process_chat_message("Hello!")
            >>> print(result['response'])
        """
        try:
            # Step 1: Validate and sanitize input
            try:
                clean_query = validate_and_sanitize_query(user_query)
            except ValidationError as e:
                return {
                    'success': False,
                    'session_id': session_id or '',
                    'response': f"Invalid query: {str(e)}",
                    'query_type': '',
                    'error': str(e)
                }
            
            # Step 2: Generate or validate session ID
            if not session_id:
                session_id = ChatbotService._generate_session_id()
            
            # Step 3: Get conversation history
            history = ChatbotService._get_conversation_history(session_id)
            
            # Step 4: Process through DAG
            dag = get_chatbot_dag()
            result = dag.process_query(
                user_query=clean_query,
                session_id=session_id,
                session_history=history
            )
            
            if not result['success']:
                return {
                    'success': False,
                    'session_id': session_id,
                    'response': result['response'],
                    'query_type': result['query_type'],
                    'error': result['error']
                }
            
            # Step 5: Save to database
            try:
                MessageService.save_conversation(
                    session_id=session_id,
                    user_message=clean_query,
                    bot_response=result['response'],
                    query_type=result['query_type'],
                    metadata={
                        'calculation_result': result.get('calculation_result', '')
                    }
                )
            except Exception as db_error:
                # Log error but don't fail the request
                print(f"Database save failed: {str(db_error)}")
            
            # Step 6: Update cache
            CacheService.save_session_history(
                session_id=session_id,
                history=result['chat_history']
            )
            
            # Step 7: Return response
            return {
                'success': True,
                'session_id': session_id,
                'response': result['response'],
                'query_type': result['query_type'],
                'calculation_result': result.get('calculation_result', ''),
                'error': ''
            }
            
        except Exception as e:
            return {
                'success': False,
                'session_id': session_id or '',
                'response': 'An unexpected error occurred. Please try again.',
                'query_type': '',
                'error': str(e)
            }
    
    @staticmethod
    def get_session_history(session_id: str, limit: int = 20) -> Dict:
        """
        Retrieves conversation history for a session.
        
        Args:
            session_id: Session to retrieve.
            limit: Maximum number of messages.
            
        Returns:
            Dict: Contains session_id and history list.
        """
        # Try cache first
        cached_history = CacheService.get_session_history(session_id)
        
        if cached_history:
            return {
                'success': True,
                'session_id': session_id,
                'history': cached_history[:limit],
                'source': 'cache'
            }
        
        # Fall back to database
        messages = MessageService.get_session_history(session_id, limit=limit)
        history = MessageService.format_history_for_api(messages)
        
        # Update cache
        if history:
            CacheService.save_session_history(session_id, history)
        
        return {
            'success': True,
            'session_id': session_id,
            'history': history,
            'source': 'database'
        }
    
    @staticmethod
    def clear_session(session_id: str) -> Dict:
        """
        Clears a conversation session.
        
        Args:
            session_id: Session to clear.
            
        Returns:
            Dict: Status of operation.
        """
        # Clear from cache
        cache_cleared = CacheService.clear_session(session_id)
        
        # Clear from database
        db_count = MessageService.delete_session_history(session_id)
        
        return {
            'success': True,
            'session_id': session_id,
            'cache_cleared': cache_cleared,
            'messages_deleted': db_count
        }
    
    @staticmethod
    def _generate_session_id() -> str:
        """
        Generates a unique session ID.
        
        Returns:
            str: UUID-based session identifier.
        """
        return f"session-{uuid.uuid4()}"
    
    @staticmethod
    def _get_conversation_history(session_id: str) -> list:
        """
        Gets conversation history from cache or database.
        
        Args:
            session_id: Session to retrieve.
            
        Returns:
            list: List of message dictionaries.
        """
        # Try cache first
        cached_history = CacheService.get_session_history(session_id)
        if cached_history:
            return cached_history
        
        # Fall back to database
        messages = MessageService.get_session_history(session_id, limit=20)
        history = MessageService.format_history_for_api(messages)
        
        # Update cache for next time
        if history:
            CacheService.save_session_history(session_id, history)
        
        return history
    
    @staticmethod
    def get_statistics() -> Dict:
        """
        Gets chatbot usage statistics.
        
        Returns:
            Dict: Statistics about sessions and messages.
        """
        return {
            'total_messages': MessageService.get_message_count(),
            'active_sessions': CacheService.get_session_count(),
            'recent_sessions': MessageService.get_recent_sessions(limit=5)
        }
    
    @staticmethod
    def cleanup_expired_sessions() -> Dict:
        """
        Cleans up expired sessions from cache.
        
        Returns:
            Dict: Number of sessions cleaned up.
        """
        cleaned = CacheService.cleanup_expired_sessions()
        return {
            'success': True,
            'sessions_cleaned': cleaned
        }
"""
Message service for handling chat message operations.

This service manages saving, retrieving, and processing chat messages
in the PostgreSQL database.
"""

from typing import List, Optional
from django.db.models import QuerySet

from django.db.models import Q
from chatbot.models import ChatMessage


class MessageService:
    """
    Service for managing chat messages in the database.
    Uses static methods for stateless operations.
    """
    
    @staticmethod
    def save_message(
        session_id: str,
        message: str,
        message_type: str,
        query_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> ChatMessage:
        """
        Saves a chat message to the database.
        
        Args:
            session_id: Unique session identifier.
            message: The message content.
            message_type: Type of message ('user' or 'bot').
            query_type: Type of query ('text' or 'calculation').
            metadata: Additional metadata (optional).
            
        Returns:
            ChatMessage: The created message instance.
            
        Example:
            >>> MessageService.save_message(
            ...     "session-123",
            ...     "Hello!",
            ...     ChatMessage.USER
            ... )
        """
        return ChatMessage.objects.create(
            session_id=session_id,
            message=message,
            message_type=message_type,
            query_type=query_type,
            metadata=metadata
        )
    
    @staticmethod
    def save_conversation(
        session_id: str,
        user_message: str,
        bot_response: str,
        query_type: str,
        metadata: Optional[dict] = None
    ) -> tuple[ChatMessage, ChatMessage]:
        """
        Saves both user message and bot response as a conversation pair.
        
        Args:
            session_id: Unique session identifier.
            user_message: The user's message.
            bot_response: The bot's response.
            query_type: Type of query detected.
            metadata: Additional metadata (optional).
            
        Returns:
            tuple[ChatMessage, ChatMessage]: (user_msg, bot_msg)
            
        Example:
            >>> user_msg, bot_msg = MessageService.save_conversation(
            ...     "session-123",
            ...     "What is 2+2?",
            ...     "The result is 4",
            ...     "calculation"
            ... )
        """
        # Save user message
        user_msg = MessageService.save_message(
            session_id=session_id,
            message=user_message,
            message_type=ChatMessage.USER,
            query_type=query_type,
            metadata=metadata
        )
        
        # Save bot response
        bot_msg = MessageService.save_message(
            session_id=session_id,
            message=bot_response,
            message_type=ChatMessage.BOT,
            metadata=metadata
        )
        
        return user_msg, bot_msg
    
    @staticmethod
    def get_session_history(
        session_id: str,
        limit: Optional[int] = None
    ) -> QuerySet[ChatMessage]:
        """
        Retrieves chat history for a session from database.
        
        Args:
            session_id: Session to retrieve.
            limit: Maximum number of messages to return (optional).
            
        Returns:
            QuerySet[ChatMessage]: Queryset of messages ordered by timestamp.
            
        Example:
            >>> messages = MessageService.get_session_history("session-123", limit=20)
        """
        queryset = ChatMessage.objects.filter(
            session_id=session_id
        ).order_by('timestamp')
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @staticmethod
    def get_recent_sessions(limit: int = 10) -> List[str]:
        """
        Gets list of recent session IDs.
        
        Args:
            limit: Maximum number of sessions to return.
            
        Returns:
            List[str]: List of session IDs.
        """
        return list(
            ChatMessage.objects.values_list('session_id', flat=True)
            .distinct()
            .order_by('-timestamp')[:limit]
        )
    
    @staticmethod
    def delete_session_history(session_id: str) -> int:
        """
        Deletes all messages for a session.
        
        Args:
            session_id: Session to delete.
            
        Returns:
            int: Number of messages deleted.
        """
        deleted, _ = ChatMessage.objects.filter(session_id=session_id).delete()
        return deleted
    
    @staticmethod
    def get_message_count(session_id: Optional[str] = None) -> int:
        """
        Gets count of messages.
        
        Args:
            session_id: Optional session to filter by.
            
        Returns:
            int: Number of messages.
        """
        if session_id:
            return ChatMessage.objects.filter(session_id=session_id).count()
        return ChatMessage.objects.count()
    
    @staticmethod
    def format_history_for_api(messages: QuerySet[ChatMessage]) -> List[dict]:
        """
        Formats message queryset for API response.
        
        Args:
            messages: Queryset of ChatMessage objects.
            
        Returns:
            List[dict]: List of formatted message dictionaries.
        """
        return [
            {
                'type': msg.message_type,
                'content': msg.message,
                'query_type': msg.query_type,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    
    @staticmethod
    def search_messages(
        query: str,
        session_id: Optional[str] = None
    ) -> QuerySet[ChatMessage]:
        """
        Searches messages by content.
        
        Args:
            query: Search query string.
            session_id: Optional session to filter by.
            
        Returns:
            QuerySet[ChatMessage]: Matching messages.
        """
        filters = Q(message__icontains=query)
        
        if session_id:
            filters &= Q(session_id=session_id)
        
        return ChatMessage.objects.filter(filters).order_by('-timestamp')
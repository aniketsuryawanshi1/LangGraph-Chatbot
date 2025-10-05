"""
Cache service for managing conversation sessions and history.

This service provides caching functionality for chat sessions
to improve performance and maintain conversation context.
"""

from typing import Optional, Dict, List
from datetime import datetime, timedelta


class CacheService:
    """
    Service for caching chat sessions and history.
    Uses in-memory storage (can be extended to Redis/Memcached).
    """
    
    # In-memory cache storage
    _session_cache: Dict[str, Dict] = {}
    
    # Cache expiration time (in minutes)
    CACHE_EXPIRATION_MINUTES = 60
    
    @staticmethod
    def get_session_history(session_id: str) -> List[Dict]:
        """
        Retrieves chat history for a session from cache.
        
        Args:
            session_id: Unique session identifier.
            
        Returns:
            List[Dict]: List of chat messages for the session.
            
        Example:
            >>> history = CacheService.get_session_history("session-123")
        """
        session_data = CacheService._session_cache.get(session_id)
        
        if not session_data:
            return []
        
        # Check if cache has expired
        if CacheService._is_expired(session_data['timestamp']):
            # Remove expired session
            CacheService.clear_session(session_id)
            return []
        
        return session_data.get('history', [])
    
    @staticmethod
    def save_session_history(session_id: str, history: List[Dict]) -> None:
        """
        Saves chat history for a session to cache.
        
        Args:
            session_id: Unique session identifier.
            history: List of chat messages to cache.
            
        Example:
            >>> CacheService.save_session_history("session-123", messages)
        """
        CacheService._session_cache[session_id] = {
            'history': history,
            'timestamp': datetime.now()
        }
    
    @staticmethod
    def clear_session(session_id: str) -> bool:
        """
        Clears cache for a specific session.
        
        Args:
            session_id: Session to clear.
            
        Returns:
            bool: True if session was cleared, False if not found.
        """
        if session_id in CacheService._session_cache:
            del CacheService._session_cache[session_id]
            return True
        return False
    
    @staticmethod
    def clear_all_sessions() -> int:
        """
        Clears all cached sessions.
        
        Returns:
            int: Number of sessions cleared.
        """
        count = len(CacheService._session_cache)
        CacheService._session_cache.clear()
        return count
    
    @staticmethod
    def cleanup_expired_sessions() -> int:
        """
        Removes all expired sessions from cache.
        
        Returns:
            int: Number of expired sessions removed.
        """
        expired_sessions = [
            session_id
            for session_id, data in CacheService._session_cache.items()
            if CacheService._is_expired(data['timestamp'])
        ]
        
        for session_id in expired_sessions:
            CacheService.clear_session(session_id)
        
        return len(expired_sessions)
    
    @staticmethod
    def get_session_count() -> int:
        """
        Gets the number of active sessions in cache.
        
        Returns:
            int: Number of cached sessions.
        """
        return len(CacheService._session_cache)
    
    @staticmethod
    def session_exists(session_id: str) -> bool:
        """
        Checks if a session exists in cache and is not expired.
        
        Args:
            session_id: Session to check.
            
        Returns:
            bool: True if session exists and is valid.
        """
        session_data = CacheService._session_cache.get(session_id)
        if not session_data:
            return False
        
        return not CacheService._is_expired(session_data['timestamp'])
    
    @staticmethod
    def _is_expired(timestamp: datetime) -> bool:
        """
        Checks if a timestamp has expired.
        
        Args:
            timestamp: Timestamp to check.
            
        Returns:
            bool: True if expired.
        """
        expiration_time = timedelta(minutes=CacheService.CACHE_EXPIRATION_MINUTES)
        return datetime.now() - timestamp > expiration_time
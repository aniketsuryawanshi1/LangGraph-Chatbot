"""
Django REST Framework serializers for chatbot API.

Serializers handle validation and conversion between
Python objects and JSON format.
"""

from rest_framework import serializers
from chatbot.models import ChatMessage


class ChatRequestSerializer(serializers.Serializer):
    """
    Serializer for incoming chat requests.
    
    Validates user input before processing.
    """
    
    query = serializers.CharField(
        required=True,
        max_length=5000,
        help_text="User's query or message"
    )
    
    session_id = serializers.CharField(
        required=False,
        max_length=255,
        allow_null=True,
        allow_blank=True,
        help_text="Optional session ID for conversation continuity"
    )
    
    def validate_query(self, value: str) -> str:
        """
        Validates the query field.
        
        Args:
            value: The query string.
            
        Returns:
            str: Validated query.
            
        Raises:
            serializers.ValidationError: If query is invalid.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Query cannot be empty")
        
        return value.strip()


class ChatResponseSerializer(serializers.Serializer):
    """
    Serializer for chat responses.
    
    Formats the chatbot's response for API output.
    """
    
    success = serializers.BooleanField()
    session_id = serializers.CharField()
    response = serializers.CharField()
    query_type = serializers.CharField()
    calculation_result = serializers.CharField(required=False, allow_blank=True)
    error = serializers.CharField(required=False, allow_blank=True)


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatMessage model.
    
    Used for retrieving message history.
    """
    
    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'session_id',
            'message',
            'message_type',
            'query_type',
            'timestamp',
            'metadata'
        ]
        read_only_fields = ['id', 'timestamp']


class SessionHistorySerializer(serializers.Serializer):
    """
    Serializer for session history responses.
    """
    
    success = serializers.BooleanField()
    session_id = serializers.CharField()
    history = serializers.ListField(
        child=serializers.DictField()
    )
    source = serializers.CharField(required=False)


class SessionClearSerializer(serializers.Serializer):
    """
    Serializer for session clear responses.
    """
    
    success = serializers.BooleanField()
    session_id = serializers.CharField()
    cache_cleared = serializers.BooleanField()
    messages_deleted = serializers.IntegerField()


class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for chatbot statistics.
    """
    
    total_messages = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    recent_sessions = serializers.ListField(
        child=serializers.CharField()
    )
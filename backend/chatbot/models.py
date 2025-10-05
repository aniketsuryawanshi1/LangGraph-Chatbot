"""
Database models for the chatbot application.
Stores chat history in PostgreSQL database.
"""

from django.db import models
from django.utils import timezone


class ChatMessage(models.Model):
    """
    Model to store chat messages and history.
    Each message represents either a user query or a bot response.
    """
    
    # Message types
    USER = 'user'
    BOT = 'bot'
    MESSAGE_TYPE_CHOICES = [
        (USER, 'User'),
        (BOT, 'Bot'),
    ]
    
    # Query types detected by the decision node
    TEXT = 'text'
    CALCULATION = 'calculation'
    QUERY_TYPE_CHOICES = [
        (TEXT, 'Text Query'),
        (CALCULATION, 'Calculation Query'),
    ]
    
    # Session ID to group related conversations
    session_id = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Unique identifier for the conversation session"
    )
    
    # Message content
    message = models.TextField(
        help_text="The actual message content"
    )
    
    # Message type (user or bot)
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        help_text="Whether this message is from user or bot"
    )
    
    # Query type (only for user messages)
    query_type = models.CharField(
        max_length=20,
        choices=QUERY_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Type of query detected (text or calculation)"
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text="When this message was created"
    )
    
    # Metadata (optional JSON field for additional info)
    metadata = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text="Additional metadata about the message"
    )
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        indexes = [
            models.Index(fields=['session_id', 'timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.message_type} - {self.message[:50]}..."
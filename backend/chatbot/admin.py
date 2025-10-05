"""
Django admin configuration for chatbot models.
"""

from django.contrib import admin
from chatbot.models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ChatMessage model.
    """
    
    list_display = [
        'id',
        'session_id',
        'message_type',
        'query_type',
        'message_preview',
        'timestamp'
    ]
    
    list_filter = [
        'message_type',
        'query_type',
        'timestamp'
    ]
    
    search_fields = [
        'session_id',
        'message'
    ]
    
    readonly_fields = [
        'timestamp'
    ]
    
    ordering = ['-timestamp']
    
    def message_preview(self, obj):
        """
        Shows a preview of the message content.
        """
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    
    message_preview.short_description = 'Message Preview'
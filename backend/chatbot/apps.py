f"""
Django app configuration for chatbot application.
"""

from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    """
    Configuration for the chatbot application.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    verbose_name = 'Smart Chatbot'
    
    def ready(self):
        """
        Called when Django starts.
        Use this to initialize components that should load once.
        """
        # Import to ensure models are registered
        from chatbot.models import ChatMessage
        
        # Print startup message
        print("Chatbot application loaded.")
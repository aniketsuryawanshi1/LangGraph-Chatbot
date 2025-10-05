"""
URL configuration for chatbot API endpoints.
"""

from django.urls import path
from chatbot.views import (
    ChatAPIView,
    SessionHistoryAPIView,
    SessionClearAPIView,
    StatisticsAPIView,
    HealthCheckAPIView
)

app_name = 'chatbot'

urlpatterns = [
    # Main chat endpoint
    path('chat/', ChatAPIView.as_view(), name='chat'),
    
    # Session management endpoints
    path('chat/history/<str:session_id>/', SessionHistoryAPIView.as_view(), name='session-history'),
    path('chat/session/<str:session_id>/', SessionClearAPIView.as_view(), name='session-clear'),
    
    # Statistics endpoint
    path('chat/statistics/', StatisticsAPIView.as_view(), name='statistics'),
    
    # Health check
    path('chat/health/', HealthCheckAPIView.as_view(), name='health'),
]
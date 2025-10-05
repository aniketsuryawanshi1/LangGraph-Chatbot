"""
views for chatbot API endpoints.

Provides RESTful API endpoints for:
- Chat communication
- Session history
- Statistics
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from chatbot.services.chatbot_service import ChatbotService
from chatbot.serializers import (
    ChatRequestSerializer,
    ChatResponseSerializer,
    SessionHistorySerializer,
    SessionClearSerializer,
    StatisticsSerializer
)


class ChatAPIView(APIView):
    """
    Main chat endpoint for processing user queries.
    
    POST /api/chat/
    """
    
    @extend_schema(
        request=ChatRequestSerializer,
        responses={200: ChatResponseSerializer},
        description="Process a chat message and get AI response"
    )
    def post(self, request):
        """
        Process a chat message through the LangGraph DAG workflow.
        
        Request Body:
            {
                "query": "Your message here",
                "session_id": "optional-session-id"
            }
        
        Response:
            {
                "success": true,
                "session_id": "session-uuid",
                "response": "AI response here",
                "query_type": "text" or "calculation",
                "calculation_result": "result if calculation",
                "error": ""
            }
        """
        # Validate input
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'error': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract data
        user_query = serializer.validated_data['query']
        session_id = serializer.validated_data.get('session_id')
        
        # Process through chatbot service
        result = ChatbotService.process_chat_message(
            user_query=user_query,
            session_id=session_id
        )
        
        # Return response
        response_serializer = ChatResponseSerializer(data=result)
        if response_serializer.is_valid():
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(result, status=status.HTTP_200_OK)


class SessionHistoryAPIView(APIView):
    """
    Endpoint for retrieving conversation history.
    
    GET /api/chat/history/<session_id>/
    """
    
    @extend_schema(
        responses={200: SessionHistorySerializer},
        description="Get conversation history for a session"
    )
    def get(self, request, session_id):
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: The session identifier.
        
        Response:
            {
                "success": true,
                "session_id": "session-uuid",
                "history": [
                    {
                        "type": "user",
                        "content": "Hello",
                        "timestamp": "2024-01-01T12:00:00Z"
                    },
                    ...
                ],
                "source": "cache" or "database"
            }
        """
        limit = int(request.query_params.get('limit', 20))
        
        result = ChatbotService.get_session_history(
            session_id=session_id,
            limit=limit
        )
        
        serializer = SessionHistorySerializer(data=result)
        if serializer.is_valid():
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(result, status=status.HTTP_200_OK)


class SessionClearAPIView(APIView):
    """
    Endpoint for clearing a conversation session.
    
    DELETE /api/chat/session/<session_id>/
    """
    
    @extend_schema(
        responses={200: SessionClearSerializer},
        description="Clear conversation history for a session"
    )
    def delete(self, request, session_id):
        """
        Clear conversation history for a session.
        
        Args:
            session_id: The session identifier.
        
        Response:
            {
                "success": true,
                "session_id": "session-uuid",
                "cache_cleared": true,
                "messages_deleted": 10
            }
        """
        result = ChatbotService.clear_session(session_id)
        
        serializer = SessionClearSerializer(data=result)
        if serializer.is_valid():
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(result, status=status.HTTP_200_OK)


class StatisticsAPIView(APIView):
    """
    Endpoint for chatbot usage statistics.
    
    GET /api/chat/statistics/
    """
    
    @extend_schema(
        responses={200: StatisticsSerializer},
        description="Get chatbot usage statistics"
    )
    def get(self, request):
        """
        Get chatbot usage statistics.
        
        Response:
            {
                "total_messages": 100,
                "active_sessions": 5,
                "recent_sessions": ["session-1", "session-2", ...]
            }
        """
        result = ChatbotService.get_statistics()
        
        serializer = StatisticsSerializer(data=result)
        if serializer.is_valid():
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(result, status=status.HTTP_200_OK)


class HealthCheckAPIView(APIView):
    """
    Health check endpoint.
    
    GET /api/chat/health/
    """
    
    def get(self, request):
        """
        Simple health check endpoint.
        
        Response:
            {
                "status": "healthy",
                "service": "chatbot"
            }
        """
        return Response(
            {
                'status': 'healthy',
                'service': 'chatbot',
                'version': '1.0.0'
            },
            status=status.HTTP_200_OK
        )
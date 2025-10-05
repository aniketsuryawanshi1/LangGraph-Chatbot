"""
LangGraph DAG implementation for chatbot workflow.

This module defines the Directed Acyclic Graph (DAG) for the chatbot.
The workflow has no cycles and flows from input to output.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from .nodes import GraphState, WorkflowNodes


class ChatbotDAG:
    """
    Main chatbot DAG (Directed Acyclic Graph) using LangGraph.
    
    This class builds and manages the workflow graph with:
    - Multiple nodes (functions) for different tasks
    - Edges (transitions) between nodes
    - Conditional routing based on query type
    """
    
    def __init__(self):
        """Initialize the chatbot DAG with all nodes."""
        print("Initializing Chatbot DAG...")
        
        # Initialize workflow nodes
        self.nodes = WorkflowNodes()
        
        # Build the graph
        self.graph = self._build_dag()
        
        print("Chatbot DAG initialized successfully!")
    
    def _build_dag(self) -> StateGraph:
        """
        Builds the DAG workflow using LangGraph.
        
        Returns:
            StateGraph: Compiled workflow graph.
        """
        print("Building DAG structure...")
        
        # Create the state graph
        workflow = StateGraph(GraphState)
        

        # ADD NODES (Each node is a function/task)

        workflow.add_node("input_node", self.nodes.input_node)
        workflow.add_node("decision_node", self.nodes.decision_node)
        workflow.add_node("llm_node", self.nodes.llm_node)
        workflow.add_node("tool_node", self.nodes.tool_node)
        workflow.add_node("memory_node", self.nodes.memory_node)
        workflow.add_node("output_node", self.nodes.output_node)
        
        print("   ✓ Nodes added: 6 nodes")
        

        # DEFINE EDGES (Data/state transitions)

        
        # Set entry point (start of DAG)
        workflow.set_entry_point("input_node")
        
        # Input -> Decision (unconditional edge)
        workflow.add_edge("input_node", "decision_node")
        
        # Decision -> {LLM OR Tool} (conditional edge - routing logic)
        workflow.add_conditional_edges(
            "decision_node",
            self._route_query,
            {
                "text": "llm_node",
                "calculation": "tool_node"
            }
        )
        
        # LLM -> Memory (unconditional edge)
        workflow.add_edge("llm_node", "memory_node")
        
        # Tool -> Memory (unconditional edge)
        workflow.add_edge("tool_node", "memory_node")
        
        # Memory -> Output (unconditional edge)
        workflow.add_edge("memory_node", "output_node")
        
        # Output -> END (exit point)
        workflow.add_edge("output_node", END)
        
        print("   ✓ Edges added: 7 edges (1 conditional, 6 unconditional)")
        
        # Compile the graph
        compiled_graph = workflow.compile()
        
        print("   ✓ DAG compiled successfully")
        
        return compiled_graph
    
    @staticmethod
    def _route_query(state: GraphState) -> Literal["text", "calculation"]:
        """
        Router function for conditional edges.
        
        This is the decision logic that creates multiple paths in the DAG.
        Based on query_type, it routes to either LLM or Tool node.
        
        Args:
            state: Current graph state.
            
        Returns:
            str: Next node to execute ("text" or "calculation").
        """
        return state['query_type']
    
    def process_query(
        self,
        user_query: str,
        session_id: str,
        session_history: list = None
    ) -> dict:
        """
        Main method to process a user query through the DAG.
        
        This executes the entire workflow from start to end.
        
        Args:
            user_query: The user's input message.
            session_id: Unique identifier for the conversation session.
            session_history: Previous conversation history (optional).
        
        Returns:
            dict: Contains response, query_type, history, and any errors.
            
        Example:
            >>> dag = ChatbotDAG()
            >>> result = dag.process_query("What is 5 + 3?", "session-123")
            >>> print(result['response'])
            The result of 5 + 3 is 8
        """
        print("\n" + "*" * 30)
        print(f"STARTING DAG EXECUTION")
        print("*" * 30)
        print(f"Query: {user_query}")
        print(f"Session: {session_id}")
        print("*" * 30)
        
        # Initialize state for the DAG
        initial_state: GraphState = {
            'user_query': user_query,
            'session_id': session_id,
            'query_type': '',
            'response': '',
            'calculation_result': '',
            'error': '',
            'chat_history': session_history or []
        }
        
        try:
            # Execute the DAG (flows through all nodes)
            final_state = self.graph.invoke(initial_state)
            
            print("\n" + "*" * 30)
            print(f"DAG EXECUTION COMPLETED")
            print("*" * 30)
            
            # Return the results
            return {
                'success': True,
                'response': final_state['response'],
                'query_type': final_state['query_type'],
                'chat_history': final_state['chat_history'],
                'calculation_result': final_state.get('calculation_result', ''),
                'error': final_state.get('error', '')
            }
            
        except Exception as e:
            print("\n" + "*" * 30)
            print(f"DAG EXECUTION FAILED")
            print(f"Error: {str(e)}")
            print("*" * 30)
            
            return {
                'success': False,
                'response': 'An error occurred while processing your request.',
                'query_type': '',
                'chat_history': session_history or [],
                'calculation_result': '',
                'error': str(e)
            }
    
    def visualize_dag(self) -> str:
        """
        Returns a text visualization of the DAG structure.
        
        Returns:
            str: ASCII art representation of the DAG.
        """
        return """
                Properties:
                - No cycles (DAG property)
                - Multiple decision paths
                - Directed flow from input to output
                """



# SINGLETON PATTERN - Cache the DAG instance

_chatbot_dag_instance = None


def get_chatbot_dag() -> ChatbotDAG:
    """
    Get the singleton ChatbotDAG instance.
    
    This ensures the DAG and model are loaded only once and cached.
    Subsequent calls return the cached instance for better performance.
    
    Returns:
        ChatbotDAG: The singleton chatbot DAG instance.
        
    Example:
        >>> dag = get_chatbot_dag()
        >>> result = dag.process_query("Hello!", "session-1")
    """
    global _chatbot_dag_instance
    
    if _chatbot_dag_instance is None:
        print("\n" + "="*60)
        print("Creating new ChatbotDAG instance (first time)")
        print("="*60)
        _chatbot_dag_instance = ChatbotDAG()
        print("="*60)
        print("ChatbotDAG instance created and cached!")
        print("="*60 + "\n")
    else:
        print("Using cached ChatbotDAG instance")
    
    return _chatbot_dag_instance


def clear_dag_cache() -> None:
    """
    Clears the cached DAG instance.
    Useful for testing or when configuration changes.
    """
    global _chatbot_dag_instance
    _chatbot_dag_instance = None
    print("DAG cache cleared")
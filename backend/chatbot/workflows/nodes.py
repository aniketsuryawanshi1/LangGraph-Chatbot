"""
Individual node implementations for the chatbot workflow.

Each node represents a specific task in the DAG:
- Input Node: Receives and validates user query
- Decision Node: Routes to appropriate handler
- LLM Node: Generates text responses
- Tool Node: Performs calculations
- Memory Node: Stores conversation history
- Output Node: Prepares final response
"""

import re
from typing import TypedDict
import numexpr
from chatbot.utils.langchain_utils import LangChainFactory
from chatbot.utils.validators import QueryValidator


class GraphState(TypedDict):
    """
    State object that flows through the workflow graph.
    Contains all information needed for processing a query.
    """
    user_query: str
    query_type: str
    response: str
    calculation_result: str
    error: str
    chat_history: list
    session_id: str


class WorkflowNodes:
    """
    Container class for all workflow node implementations.
    Each method represents a node in the DAG.
    """
    
    def __init__(self):
        """Initialize the workflow nodes with LangChain components."""
        # Initialize LLM and prompt template
        self.llm = LangChainFactory.create_llm()
        self.text_prompt = LangChainFactory.create_text_prompt()
        self.calc_prompt = LangChainFactory.create_calculation_prompt()
    
    @staticmethod
    def input_node(state: GraphState) -> GraphState:
        """
        INPUT NODE (DAG Entry Point)
        ============================
        Receives and validates user query.
        
        Flow: [START] -> Input Node -> Decision Node
        
        Args:
            state: Current graph state.
            
        Returns:
            GraphState: Updated state with validated query.
        """
        print(f"\n{'='*60}")
        print(f"INPUT NODE: Receiving user query")
        print(f"{'='*60}")
        
        # Validate that user query exists
        if not state.get('user_query'):
            state['error'] = "No user query provided"
            print(f"Error: {state['error']}")
            return state
        
        # Validate query using validator
        is_valid, error = QueryValidator.validate_query(state['user_query'])
        if not is_valid:
            state['error'] = error
            print(f"Validation Error: {error}")
            return state
        
        # Sanitize query
        state['user_query'] = QueryValidator.sanitize_query(state['user_query'])
        
        # Initialize empty fields if not present
        if 'chat_history' not in state:
            state['chat_history'] = []
        
        if 'error' not in state:
            state['error'] = ''
        
        print(f"Query validated: {state['user_query'][:50]}...")
        
        return state
    
    @staticmethod
    def decision_node(state: GraphState) -> GraphState:
        """
        DECISION NODE (Router)

        Detects query type and routes to appropriate handler.
        
        Flow: Input Node -> [DECISION NODE] -> {LLM Node OR Tool Node}
        
        This is the key routing logic in the DAG.
        
        Args:
            state: Current graph state.
            
        Returns:
            GraphState: Updated state with query_type set.
        """
        print(f"\n{'='*60}")
        print(f"DECISION NODE: Analyzing query type")
        print(f"{'='*60}")
        
        # Use validator to determine query type
        is_calculation = QueryValidator.is_calculation_query(state['user_query'])
        
        if is_calculation:
            state['query_type'] = 'calculation'
            print(f"Decision: CALCULATION detected")
            print(f"Routing to: TOOL NODE")
        else:
            state['query_type'] = 'text'
            print(f"Decision: TEXT query detected")
            print(f"Routing to: LLM NODE")
        
        return state
    
    def llm_node(self, state: GraphState) -> GraphState:
        """
        LLM NODE (Text Generation)

        Generates text-based responses using ChatOpenAI.
        
        Flow: Decision Node -> [LLM NODE] -> Memory Node
        
        Args:
            state: Current graph state.
            
        Returns:
            GraphState: Updated state with LLM response.
        """
        print(f"\n{'='*60}")
        print(f"LLM NODE: Generating text response")
        print(f"{'='*60}")
        
        try:
            # Format chat history for context
            history_str = self._format_chat_history(state.get('chat_history', []))
            
            # Create the prompt with context
            prompt = self.text_prompt.format(
                user_query=state['user_query'],
                chat_history=history_str
            )
            
            print(f"Calling OpenAI API...")
            
            # Get response from LLM
            response = self.llm.invoke(prompt)
            state['response'] = response.content
            
            print(f"Response generated")
            print(f"Preview: {state['response'][:80]}...")
            
        except Exception as e:
            state['error'] = f"LLM error: {str(e)}"
            state['response'] = "I apologize, but I encountered an error processing your request. Please try again."
            print(f"Error: {str(e)}")
        
        return state
    
    @staticmethod
    def tool_node(state: GraphState) -> GraphState:
        """
        TOOL NODE (Calculation)

        Performs mathematical calculations using numexpr.
        
        Flow: Decision Node -> [TOOL NODE] -> Memory Node
        
        Args:
            state: Current graph state.
            
        Returns:
            GraphState: Updated state with calculation result.
        """
        print(f"\n{'='*60}")
        print(f" TOOL NODE: Performing calculation")
        print(f"{'='*60}")
        
        try:
            user_query = state['user_query']
            
            # Extract mathematical expression
            expression = WorkflowNodes._extract_math_expression(user_query)
            
            print(f"    Expression: {expression}")
            
            # Evaluate using numexpr (safe evaluation)
            result = numexpr.evaluate(expression).item()
            
            state['calculation_result'] = str(result)
            state['response'] = f"The result of {expression} is {result}"
            
            print(f"    Calculation complete")
            print(f"    Result: {expression} = {result}")
            
        except Exception as e:
            state['error'] = f"Calculation error: {str(e)}"
            state['response'] = "I couldn't perform that calculation. Please provide a valid mathematical expression."
            print(f"   Error: {str(e)}")
        
        return state
    
    @staticmethod
    def memory_node(state: GraphState) -> GraphState:
        """
        MEMORY NODE (History Storage)

        Stores conversation history for context.
        
        Flow: {LLM Node OR Tool Node} -> [MEMORY NODE] -> Output Node
        
        Args:
            state: Current graph state.
            
        Returns:
            GraphState: Updated state with stored history.
        """
        print(f"\n{'='*60}")
        print(f" MEMORY NODE: Storing conversation history")
        print(f"{'='*60}")
        
        # Append user message
        state['chat_history'].append({
            'type': 'user',
            'content': state['user_query'],
            'query_type': state.get('query_type', 'text')
        })
        
        # Append assistant response
        state['chat_history'].append({
            'type': 'assistant',
            'content': state['response']
        })
        
        # Keep only last 10 exchanges (20 messages) to manage memory
        if len(state['chat_history']) > 20:
            state['chat_history'] = state['chat_history'][-20:]
        
        print(f"   History updated")
        print(f"   Total messages in history: {len(state['chat_history'])}")
        
        return state
    
    @staticmethod
    def output_node(state: GraphState) -> GraphState:
        """
        OUTPUT NODE (DAG Exit Point)

        Prepares the final response for the user.
        
        Flow: Memory Node -> [OUTPUT NODE] -> [END]
        
        Args:
            state: Current graph state.
            
        Returns:
            GraphState: Final state with prepared response.
        """
        print(f"\n{'='*60}")
        print(f" OUTPUT NODE: Preparing final response")
        print(f"{'='*60}")
        
        # Ensure response exists
        if not state.get('response'):
            state['response'] = "I'm sorry, I couldn't generate a response."
        
        print(f"   Response ready")
        print(f"   Final response: {state['response'][:80]}...")
        print(f"{'='*60}\n")
        
        return state
    
    @staticmethod
    def _format_chat_history(history: list) -> str:
        """
        Helper method to format chat history for LLM prompts.
        
        Args:
            history: List of chat messages.
            
        Returns:
            str: Formatted history string.
        """
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history[-10:]:  # Use last 10 messages for context
            role = "User" if msg['type'] == 'user' else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def _extract_math_expression(query: str) -> str:
        """
        Helper method to extract mathematical expression from query.
        
        Args:
            query: User's query string.
            
        Returns:
            str: Extracted mathematical expression.
        """
        # Remove common words
        expression = re.sub(
            r'(calculate|compute|what is|solve|the|result|of|=|\?)',
            '',
            query,
            flags=re.IGNORECASE
        )
        
        # Clean up whitespace
        expression = expression.strip()
        
        # If expression is empty, use original query
        if not expression:
            expression = query
        
        return expression
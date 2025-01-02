"""
Core chatbot functionality using LangChain components.
Implements the chat logic and message handling.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from typing import Dict, Any

class Chatbot:
    def __init__(self, api_key: str, model_name: str, system_prompt: str):
        """Initialize the chatbot with necessary components."""
        self.model = ChatOpenAI(
            api_key=api_key,
            model=model_name,
            temperature=0.7
        )
        
        # Create the chat prompt template
        self.template = ChatPromptTemplate([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}")
        ])
        
        # Create the base chain
        self.chain = self.template | self.model
        
    def create_chain_with_history(self, get_session_history):
        """Create a chain with message history capability."""
        return RunnableWithMessageHistory(
            self.chain,
            get_session_history,
            input_messages_key="user_input",
            history_messages_key="history"
        )

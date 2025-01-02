"""
Configuration settings and environment variable management for the chatbot application.
Centralizes all configuration-related code for better maintainability.
"""
import os
from dotenv import load_dotenv, find_dotenv
import streamlit as st

class Config:
    """Configuration manager for the chatbot application."""
    
    @staticmethod
    def load_environment():
        """
        Initialize environment variables from .env file and Streamlit secrets.
        Returns a dictionary with configuration values, prioritizing user-provided API key.
        """
        # Load from .env file if it exists
        _ = load_dotenv(find_dotenv())
        
        # Initialize configuration with default values
        config = {
            "MODEL_NAME": "gpt-4o-mini",
            "DEFAULT_SYSTEM_PROMPT": "You are a helpful AI assistant called Nebula that uses gpt-4o-mini as the base model."
        }
        
        # Get API key from Streamlit session state (user input) or environment
        if 'openai_api_key' in st.session_state:
            config["OPENAI_API_KEY"] = st.session_state.openai_api_key
        else:
            config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
            
        return config
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate the format of the OpenAI API key.
        Basic validation to check if the key follows the expected pattern.
        """
        return api_key.startswith('sk-') and len(api_key) > 40
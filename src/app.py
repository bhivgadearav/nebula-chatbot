"""
Main Streamlit application file.
Implements the user interface and coordinates between different components.
"""
import streamlit as st
from config import Config
from session_manager import SessionManager
from chatbot import Chatbot
import time
from PIL import Image
nebula_favicon = Image.open("src/pubic/favicon-16x16.png") 
nebula_chat_icon = Image.open("src/pubic/robot.jpg")

def render_api_key_input():
    """
    Render the API key input interface.
    Returns True if a valid API key is available, False otherwise.
    """
    api_key_container = st.container()
    
    with api_key_container:
        if 'openai_api_key' not in st.session_state:
            st.session_state.openai_api_key = None
            
        api_key_input = st.text_input(
            "Enter your OpenAI API key:",
            type="password",
            key="api_key_input",
            help="Your API key will be stored only for this session and won't be saved permanently."
        )
        
        if api_key_input:
            if Config.validate_api_key(api_key_input):
                st.session_state.openai_api_key = api_key_input
                return True
            else:
                st.error("Invalid API key format. Please check your API key.")
                st.session_state.openai_api_key = None
                return False
                
        if not st.session_state.openai_api_key:
            st.warning(
                "Please enter your OpenAI API key to use the chatbot. "
                "If you don't have one, you can get it from https://platform.openai.com/api-keys"
            )
            return False
            
        return True

def initialize_state():
    """Initialize the application state in Streamlit's session state."""
    # Initialize session manager if not exists
    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = SessionManager()
        st.session_state.session_manager.create_session()
    
    # Initialize chatbot if API key is available
    if 'openai_api_key' in st.session_state and st.session_state.openai_api_key:
        if 'chatbot' not in st.session_state:
            env_vars = Config.load_environment()
            st.session_state.chatbot = Chatbot(
                api_key=env_vars["OPENAI_API_KEY"],
                model_name=env_vars["MODEL_NAME"],
                system_prompt=env_vars["DEFAULT_SYSTEM_PROMPT"]
            )

def render_sidebar():
    """Render the sidebar with session management controls."""
    with st.sidebar:
        st.title("Chat Sessions")
        
        # Only show session management if API key is valid
        if st.session_state.get('openai_api_key'):
            # New chat button
            if st.button("New Chat"):
                session_id = st.session_state.session_manager.create_session()
                st.rerun()
            
            # Session selection
            sessions = st.session_state.session_manager.get_all_sessions()
            current_session = st.session_state.session_manager.get_current_session()
            
            st.write("Select Chat:")
            for session_id, session in sessions.items():
                if st.sidebar.button(
                    session.name,
                    key=f"session_{session_id}",
                    use_container_width=True,
                    type="secondary" if session_id != current_session.id else "primary"
                ):
                    st.session_state.session_manager.switch_session(session_id)
                    st.rerun()

def render_chat_interface():
    """Render the main chat interface."""
    st.title("Ask Nebula Anything")
    st.link_button("Open Source Code", "https://github.com/bhivgadearav/nebula-chatbot.git", help=None, type="secondary", icon=None, disabled=False, use_container_width=False)
    
    # Check for valid API key first
    if not st.session_state.get('openai_api_key'):
        return
    
    # Get current session
    current_session = st.session_state.session_manager.get_current_session()
    if not current_session:
        st.warning("No active chat session.")
        return
    
    # Display chat history
    for message in current_session.history.messages:
        with st.chat_message(message.type):
            st.write(message.content)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        with st.chat_message("human"):
            st.write(prompt)
        
        try:
            # Get chatbot response
            chain_with_history = st.session_state.chatbot.create_chain_with_history(
                lambda session_id: st.session_state.session_manager.get_history(session_id)
            )
            
            with st.chat_message("assistant", avatar=nebula_chat_icon):
                with st.spinner('Finding the best answer for you...'):
                    response = chain_with_history.invoke(
                        {"user_input": prompt},
                        config={"configurable": {"session_id": current_session.id}}
                    )
                    if response:
                        return
                st.write(response.content)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if "API key" in str(e):
                st.session_state.openai_api_key = None
                st.rerun()

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Nebula",
        page_icon=nebula_favicon,
        layout="wide"
    )
    
    # First, handle API key input
    if not render_api_key_input():
        return
    
    initialize_state()
    render_sidebar()
    render_chat_interface()

if __name__ == "__main__":
    main()
"""
Handles session management and chat history for multiple conversations.
Provides a clean interface for creating, retrieving, and switching between chat sessions.
"""
import uuid
from typing import Dict, Optional
from dataclasses import dataclass
from langchain_core.chat_history import InMemoryChatMessageHistory

@dataclass
class Session:
    """Data class to store session information"""
    id: str
    name: str
    history: InMemoryChatMessageHistory

class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._current_session_id: Optional[str] = None
    
    def create_session(self, name: Optional[str] = None) -> str:
        """Create a new chat session and set it as current."""
        session_id = str(uuid.uuid4())
        session_name = name or f"Chat {len(self._sessions) + 1}"
        self._sessions[session_id] = Session(
            id=session_id,
            name=session_name,
            history=InMemoryChatMessageHistory()
        )
        self._current_session_id = session_id
        return session_id
    
    def get_current_session(self) -> Optional[Session]:
        """Get the currently active session."""
        if self._current_session_id:
            return self._sessions.get(self._current_session_id)
        return None
    
    def switch_session(self, session_id: str) -> bool:
        """Switch to an existing session."""
        if session_id in self._sessions:
            self._current_session_id = session_id
            return True
        return False
    
    def get_all_sessions(self) -> Dict[str, Session]:
        """Get all available sessions."""
        return self._sessions
    
    def get_history(self, session_id: str) -> Optional[InMemoryChatMessageHistory]:
        """Get chat history for a specific session."""
        session = self._sessions.get(session_id)
        return session.history if session else None

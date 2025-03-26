from typing import Dict, List, Optional
from datetime import datetime
from models.decision import DecisionHistory

class SessionStorage:
    def __init__(self):
        self._storage: Dict[str, List[DecisionHistory]] = {}

    def add_decision(self, session_id: str, decision: DecisionHistory) -> None:
        """Add a decision to the session's history"""
        if session_id not in self._storage:
            self._storage[session_id] = []
        self._storage[session_id].append(decision)

    def get_history(self, session_id: str) -> List[DecisionHistory]:
        """Get all decisions for a session"""
        return self._storage.get(session_id, [])

    def clear_session(self, session_id: str) -> None:
        """Clear all decisions for a session"""
        if session_id in self._storage:
            del self._storage[session_id]

    def get_all_sessions(self) -> List[str]:
        """Get all active session IDs"""
        return list(self._storage.keys())

# Singleton instance of the storage
session_storage = SessionStorage()

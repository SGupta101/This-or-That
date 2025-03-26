from models.decision import DecisionHistory
from typing import Dict, List, Optional
from collections import defaultdict

class SessionStorage:
    def __init__(self):
        # Dictionary of session_id -> {decision_id -> DecisionHistory}
        self._storage: Dict[str, Dict[str, DecisionHistory]] = defaultdict(dict)
        # Dictionary of session_id -> List[decision_id] to maintain order
        self._order: Dict[str, List[str]] = defaultdict(list)

    def add_decision(self, session_id: str, decision: DecisionHistory) -> None:
        """Add a decision to the session's history"""
        decision_id = decision.decision_id
        self._storage[session_id][decision_id] = decision
        self._order[session_id].append(decision_id)

    def get_decision(self, session_id: str, decision_id: str) -> Optional[DecisionHistory]:
        """Get a specific decision by ID"""
        return self._storage.get(session_id, {}).get(decision_id)

    def get_session(self, session_id:str):
        return self._stroage.get(session_id, {})

    def get_history(self, session_id: str) -> List[DecisionHistory]:
        """Get all decisions for a session in order"""
        return [
            self._storage[session_id][decision_id]
            for decision_id in self._order.get(session_id, [])
        ]

    def update_decision(self, session_id: str, decision_id: str, update: dict) -> None:
        """Update a specific decision"""
        decision = self.get_decision(session_id, decision_id)
        if decision:
            for key, value in update.items():
                setattr(decision, key, value)

    def clear_session(self, session_id: str) -> None:
        """Clear all decisions for a session"""
        if session_id in self._storage:
            del self._storage[session_id]
            del self._order[session_id]

    def get_all_sessions(self) -> List[str]:
        """Get all active session IDs"""
        return list(self._storage.keys())

# Singleton instance of the storage
session_storage = SessionStorage()
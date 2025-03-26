from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DecisionRequest(BaseModel):
    """Request model for making a decision"""
    option_a: str
    option_b: str
    use_reasoning: bool = False  # Default to random if not specified

class DecisionResponse(BaseModel):
    """Response model for decision result"""
    choice: str
    reasoning: Optional[str] = None
    decision_type: str  # "random" or "reasoned"
    timestamp: datetime

class DecisionHistory(BaseModel):
    """Model for storing decision history"""
    session_id: str
    decision_id: str  # Unique ID for each decision
    option_a: str
    option_b: str
    app_choice: str  # What the app suggested
    app_reasoning: Optional[str]  # Reasoning provided by the app
    user_final_choice: Optional[str] = None  # What the user decided (can be None)
    decision_type: str  # "random" or "reasoned"
    timestamp: datetime
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
    option_a: str
    option_b: str
    choice: str
    reasoning: Optional[str]
    decision_type: str
    timestamp: datetime
    user_final_choice: Optional[str] = None

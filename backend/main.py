from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from utils.session_storage import session_storage
from utils.openai_helper import get_reasoned_decision
from models.decision import DecisionRequest, DecisionResponse, DecisionHistory
import uuid
import random

app = FastAPI(title="Decision Maker API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for health check
@app.get("/")
async def root():
    return {"status": "healthy", "version": "1.0.0"}

# POST /api/decide
# Make a decision between two options
@app.post("/api/decide")
async def make_decision(request: DecisionRequest, session_id: str = None):
    print("request inside backend:", request)
    # If no session_id is provided, create a new one
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Generate a unique decision ID
    decision_id = str(uuid.uuid4())
    print("request:", request)
    print("session_id:", session_id)
    
    if request.user_reasoning:
        openai_response = get_reasoned_decision(request.option_a, request.option_b)
        print("OpenAI response:", openai_response)
        if openai_response is None:
            print("raising http exception")
            raise HTTPException(status_code=500, detail="Failed to get reasoned decision")
        choice = openai_response["choice"]
        reasoning = openai_response["reasoning"]
        decision_type = "reasoned"
    else:
        choice = random.choice([request.option_a, request.option_b])
        reasoning = None
        decision_type = "random"

    # Create the response
    response = DecisionResponse(
        choice=choice,
        reasoning=reasoning,
        decision_type=decision_type,
        timestamp=datetime.now(),
        decision_id=decision_id,
        session_id=session_id
    )

    # Store the decision in session history
    decision_history = DecisionHistory(
        session_id=session_id,
        decision_id=decision_id,
        option_a=request.option_a,
        option_b=request.option_b,
        app_choice=choice,
        app_reasoning=reasoning,
        user_final_choice=None,
        decision_type=decision_type,
        timestamp=datetime.now()
    )
    session_storage.add_decision(session_id, decision_history)
    return response

# GET /api/history
# Get the decision history for the current session
@app.get("/api/history")
async def get_history(session_id: str):
    history = session_storage.get_history(session_id)
    return {
        "decisions": [
            {
                "decision_id": decision.decision_id,
                "options": {
                    "option_a": decision.option_a,
                    "option_b": decision.option_b
                },
                "app_decision": {
                    "choice": decision.app_choice,
                    "reasoning": decision.app_reasoning
                },
                "user_decision": {
                    "choice": decision.user_final_choice or "No final choice made"
                },
                "decision_type": decision.decision_type,
                "timestamp": decision.timestamp
            }
            for decision in history
        ]
    }

# POST /api/history/{decision_id}/final-choice
# Record the user's final choice for a decision
@app.post("/api/history/{decision_id}/final-choice")
async def record_final_choice(decision_id: str, choice: str, session_id: str):
    session_storage.update_decision(
        session_id,
        decision_id,
        {"user_final_choice": choice}
    )
    return {"status": "success"}

# GET /api/session
# Get current session information
@app.get("/api/session")
async def get_session(session_id: str):
    return session_storage.get_session(session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

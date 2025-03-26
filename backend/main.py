from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from utils.session_storage import session_storage
from utils.openai_helper import get_reasoned_decision

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
async def make_decision(request: DecisionRequest):
    # If no session_id is provided, create a new one
    if not request.session_id:
        request.session_id = str(uuid.uuid4())
    
    # Generate a unique decision ID
    decision_id = str(uuid.uuid4())
    
    if request.decision_type == "random":
        choice = random.choice([request.option_a, request.option_b])
        reasoning = None
        decision_type = "random"
    elif request.decision_type == "reasoned":
        openai_response = get_reasoned_decision(request.option_a, request.option_b)
        if openai_response is None:
            raise HTTPException(status_code=500, detail="Failed to get reasoned decision")
        choice = openai_response["choice"]
        reasoning = openai_response["reasoning"]
        decision_type = "reasoned"
    else:
        raise HTTPException(status_code=400, detail="Invalid decision type")

    # Create the response
    response = DecisionResponse(
        choice=choice,
        reasoning=reasoning,
        decision_type=decision_type,
        timestamp=datetime.now(),
        decision_id=decision_id  # Add decision ID to response
    )

    # Store the decision in session history
    decision_history = DecisionHistory(
        session_id=request.session_id,
        decision_id=decision_id,
        option_a=request.option_a,
        option_b=request.option_b,
        app_choice=choice,
        app_reasoning=reasoning,
        user_final_choice=None,  # No user choice yet
        decision_type=decision_type,
        timestamp=datetime.now()
    )
    session_storage.add_decision(request.session_id, decision_history)

    return response

# GET /api/history
# Get the decision history for the current session
@app.get("/api/history")
async def get_history():
    # Implementation will go here
    pass

# POST /api/history/{decision_id}/final-choice
# Record the user's final choice for a decision
@app.post("/api/history/{decision_id}/final-choice")
async def record_final_choice(decision_id: str, choice: str):
    # Implementation will go here
    pass

# GET /api/session
# Get current session information
@app.get("/api/session")
async def get_session():
    # Implementation will go here
    pass

# GET /
# Check if the server is running
@app.get("/")
async def root():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

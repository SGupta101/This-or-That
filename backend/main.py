from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="This-or-That Decision API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class DecisionRequest(BaseModel):
    optionA: str
    optionB: str
    mode: str = "ai"  # "ai" or "random"
    context: Optional[str] = None

@app.post("/api/decide")
async def decide(request: DecisionRequest):
    try:
        if request.mode == "random":
            choice = random.choice([request.optionA, request.optionB])
            return {"decision": choice, "explanation": "Randomly selected!"}
        
        # AI decision will be implemented in models/decision.py
        from models.decision import ai_decision
        return await ai_decision(request.optionA, request.optionB, request.context)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history(limit: int = 10):
    try:
        from database.supabase import get_recent_decisions
        return await get_recent_decisions(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)

async def get_recent_decisions(limit: int = 10):
    """Get recent decisions from the database"""
    try:
        response = supabase.table("decisions").select("*").limit(limit).order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

async def save_decision(optionA: str, optionB: str, choice: str, explanation: str):
    """Save a decision to the database"""
    try:
        data = {
            "option_a": optionA,
            "option_b": optionB,
            "choice": choice,
            "explanation": explanation
        }
        response = supabase.table("decisions").insert(data).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

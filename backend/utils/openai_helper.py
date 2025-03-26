import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_reasoned_decision(option_a: str, option_b: str) -> dict:
    """
    Get a reasoned decision from OpenAI
    
    Args:
        option_a: First option
        option_b: Second option
        
    Returns:
        dict: Contains choice and reasoning
    """
    
    prompt = f"""
    You are a decision-making assistant. 
    Please choose between these two options and provide a clear, concise explanation for your choice:
    
    Options:
    1. {option_a}
    2. {option_b}
    
    Your response should be in this JSON format:
    {
        "choice": "Option 1 or Option 2",
        "reasoning": "Clear and concise explanation for why you chose this option"
    }
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful decision-making assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7  # Controls randomness (0.7 is a good balance)
        )
        
        # Extract the choice and reasoning from the response
        content = response.choices[0].message.content
        
        # Parse the JSON response
        try:
            import json
            decision = json.loads(content)
            return {
                "choice": decision["choice"],
                "reasoning": decision["reasoning"]
            }
        except json.JSONDecodeError:
            # If OpenAI didn't return JSON, try to parse the text
            if "Option 1" in content:
                choice = option_a
            elif "Option 2" in content:
                choice = option_b
            else:
                choice = random.choice([option_a, option_b])
            
            return {
                "choice": choice,
                "reasoning": "Could not parse reasoning. Please try again."
            }
            
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None
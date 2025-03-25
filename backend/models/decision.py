from sentence_transformers import SentenceTransformer, util
import numpy as np

# Initialize the model (this will download it the first time)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Predefined criteria for evaluation
CRITERIA = [
    "is healthy",
    "is productive",
    "is relaxing",
    "is cost-effective",
    "is time-efficient"
]

async def ai_decision(optionA: str, optionB: str, context: str = None):
    # Encode the options
    optionA_embedding = model.encode(optionA, convert_to_tensor=True)
    optionB_embedding = model.encode(optionB, convert_to_tensor=True)
    
    # Encode criteria
    criteria_embeddings = model.encode(CRITERIA, convert_to_tensor=True)
    
    # Calculate scores for each option against criteria
    scoresA = util.pytorch_cos_sim(optionA_embedding, criteria_embeddings)[0]
    scoresB = util.pytorch_cos_sim(optionB_embedding, criteria_embeddings)[0]
    
    # Convert to numpy for easier manipulation
    scoresA = scoresA.cpu().numpy()
    scoresB = scoresB.cpu().numpy()
    
    # Calculate overall score
    scoreA = np.mean(scoresA)
    scoreB = np.mean(scoresB)
    
    # Make decision
    if scoreA > scoreB:
        choice = optionA
        winning_criteria = CRITERIA[np.argmax(scoresA)]
    else:
        choice = optionB
        winning_criteria = CRITERIA[np.argmax(scoresB)]
    
    explanation = f"I recommend {choice} because it scores higher in {winning_criteria}"
    
    return {
        "decision": choice,
        "explanation": explanation,
        "scores": {
            optionA: float(scoreA),
            optionB: float(scoreB)
        }
    }

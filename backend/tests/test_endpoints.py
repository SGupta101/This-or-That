import pytest
from fastapi.testclient import TestClient
from main import app
from models.decision import DecisionRequest
from fastapi import HTTPException

# Create a test client
client = TestClient(app)

# Test data
TEST_OPTIONS = {
    "option_a": "Option A",
    "option_b": "Option B"
}

@pytest.fixture
def decision_request():
    """Fixture to create a valid decision request"""
    return DecisionRequest(
        option_a=TEST_OPTIONS["option_a"],
        option_b=TEST_OPTIONS["option_b"],
        user_reasoning=False
    )

def test_make_random_decision(decision_request):
    """Test making a random decision"""
    response = client.post("/api/decide", json=decision_request.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert "choice" in data
    assert data["choice"] in [TEST_OPTIONS["option_a"], TEST_OPTIONS["option_b"]]
    assert "decision_id" in data
    assert "session_id" in data
    assert data["decision_type"] == "random"
    assert data["reasoning"] == None

def test_make_reasoned_decision(decision_request):
    """Test making a reasoned decision"""
    decision_request.user_reasoning = True
    response = client.post("/api/decide", json=decision_request.model_dump())
    assert response.status_code == 200
    
    data = response.json()
    assert "choice" in data
    assert data["choice"] in [TEST_OPTIONS["option_a"], TEST_OPTIONS["option_b"]]
    assert "decision_id" in data
    assert "session_id" in data
    assert data["decision_type"] == "reasoned"
    assert "reasoning" in data
    assert isinstance(data["reasoning"], str)

def test_openai_failure(decision_request, mocker):
    """Test OpenAI API failure"""
    # Mock the OpenAI function to always return None
    mock = mocker.patch('main.get_reasoned_decision', return_value=None)
    
    print("\nTest setup complete")
    print("Mock function:", mock)
    print("Mock return value:", mock.return_value)
    
    decision_request.user_reasoning = True
    
    response = client.post("/api/decide", json=decision_request.model_dump())
    print("\nResponse status code:", response.status_code)
    print("Response content:", response.json())
    
    assert response.status_code == 500
    assert response.json() == {'detail': 'Failed to get reasoned decision'}

def test_get_history(decision_request):
    """Test getting decision history"""
    # Create a session ID
    session_id = "test-session-123"
    
    # Make a random decision
    decision_request.user_reasoning = False
    response = client.post(f"/api/decide?session_id={session_id}", json=decision_request.model_dump())
    assert response.status_code == 200
    random_decision = response.json()
    
    # Make a reasoned decision
    decision_request.user_reasoning = True
    response = client.post(f"/api/decide?session_id={session_id}", json=decision_request.model_dump())
    assert response.status_code == 200
    reasoned_decision = response.json()
    
    # Get the history
    response = client.get(f"/api/history?session_id={session_id}")
    assert response.status_code == 200
    
    history = response.json()
    print("History:", history)
    assert "decisions" in history
    assert len(history["decisions"]) == 2
    
    # Verify the decisions in history
    decisions = history["decisions"]
    
    # Check random decision
    random_history = next(d for d in decisions if d["decision_id"] == random_decision["decision_id"])
    assert random_history["app_decision"]["choice"] == random_decision["choice"]
    assert random_history["app_decision"]["reasoning"] == random_decision["reasoning"]
    
    # Check reasoned decision
    reasoned_history = next(d for d in decisions if d["decision_id"] == reasoned_decision["decision_id"])
    assert reasoned_history["app_decision"]["choice"] == reasoned_decision["choice"]
    assert reasoned_history["app_decision"]["reasoning"] == reasoned_decision["reasoning"]

def test_record_final_choice(decision_request):
    """Test recording a user's final choice for a decision"""
    # Create a session ID
    session_id = "test-session-123"
    
    # Make a decision first
    decision_request.user_reasoning = False
    response = client.post(f"/api/decide?session_id={session_id}", json=decision_request.model_dump())
    assert response.status_code == 200
    decision = response.json()
    
    # Record a final choice
    decision_id = decision["decision_id"]
    choice = decision["choice"]  # Record the same choice for testing
    
    response = client.post(
        f"/api/history/{decision_id}/final-choice?choice={choice}&session_id={session_id}"
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    
    # Verify the choice was recorded
    response = client.get(f"/api/history?session_id={session_id}")
    assert response.status_code == 200
    
    history = response.json()
    assert "decisions" in history
    decisions = history["decisions"]
    
    # Find our decision in the history
    recorded_decision = next(d for d in decisions if d["decision_id"] == decision_id)
    assert recorded_decision["user_decision"]["choice"] == choice
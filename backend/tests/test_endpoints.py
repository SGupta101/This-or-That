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
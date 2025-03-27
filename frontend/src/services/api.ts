import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface DecisionRequest {
  option_a: string;
  option_b: string;
  user_reasoning: boolean;
}

export interface DecisionResponse {
  choice: string;
  reasoning?: string;
  decision_type: string;
}

export const makeDecision = async (data: DecisionRequest): Promise<DecisionResponse> => {
  try {
    const response = await api.post('/api/decide', data);
    return response.data;
  } catch (error) {
    console.error('Error making decision:', error);
    throw error;
  }
};

export const getHistory = async (): Promise<DecisionResponse[]> => {
  try {
    const response = await api.get('/history');
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export const recordFinalChoice = async (decisionId: string, finalChoice: string, sessionId: string) => {
  try {
    await api.post(`/api/history/${decisionId}/final-choice/${finalChoice}`, {
      session_id: sessionId
    });
  } catch (error) {
    console.error('Error recording final choice:', error);
    throw error;
  }
};
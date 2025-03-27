import { useState } from "react";
import ChoiceInput from "./components/ChoiceInput";
import { DecisionTypeToggle } from "./components/DecisionTypeToggle";
import DecisionButton from "./components/DecisionButton";
import FinalChoiceInput from "./components/FinalChoiceInput";
import { makeDecision } from "./services/api";

function App() {
  const [choices, setChoices] = useState({ option_a: "", option_b: "" });
  const [decisionType, setDecisionType] = useState<boolean>(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [decision, setDecision] = useState<string | null>(null);
  const [reasoning, setReasoning] = useState<string | null>(null);
  const [showFinalChoiceInput] = useState(false);

  const handleDecide = async () => {
    if (!choices.option_a || !choices.option_b) {
      setError("Please enter both choices");
      return;
    }

    setLoading(true);
    setError(null);
    setDecision(null);
    setReasoning(null);

    try {
      const result = await makeDecision({
        option_a: choices.option_a,
        option_b: choices.option_b,
        user_reasoning: decisionType,
      });
      setDecision(result.choice);
      setReasoning(result.reasoning ?? null); // Use null if reasoning is undefined
    } catch (err) {
      setError("Failed to make decision. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-8">This or That</h1>

      <ChoiceInput
        onChoicesChange={(option_a, option_b) =>
          setChoices({ option_a, option_b })
        }
        className="mb-6"
      />
      <DecisionTypeToggle
        decisionType={decisionType}
        onToggle={setDecisionType}
        className="mb-6"
      />

      <DecisionButton
        onDecide={handleDecide}
        loading={loading}
        className="mb-6"
      />

      {error && <div className="text-red-500 mb-4">{error}</div>}
      {decision && (
        <div className="bg-white rounded-lg shadow-md w-full max-w-md p-6">
          <div className="flex justify-between items-center mb-4">
            <p className="text-gray-600">Options:</p>
            <div className="flex space-x-2">
              <span className="px-2 py-1 bg-gray-100 rounded text-sm">
                {choices.option_a}
              </span>
              <span className="px-2 py-1 bg-gray-100 rounded text-sm">
                {choices.option_b}
              </span>
            </div>
          </div>
          <div className="flex justify-between items-center mb-4">
            <p className="text-gray-600">Chosen:</p>
            <span className="px-2 py-1 bg-green-100 rounded text-green-700 font-semibold">
              {decision}
            </span>
          </div>
          {reasoning && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Reasoning:</p>
              <p className="mt-2 text-sm text-gray-700">{reasoning}</p>
            </div>
          )}
        </div>
      )}
      {showFinalChoiceInput && (
        <FinalChoiceInput 
          options={choices} 
          decisionId={null} 
          onChoiceRecorded={() => console.log('Choice recorded')} 
          className="mb-6"
        />
      )}
    </div>
  );
}

export default App;

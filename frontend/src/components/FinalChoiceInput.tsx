import { useState } from "react";
import { recordFinalChoice } from "../services/api";
import { useSessionId } from "../contexts/SessionContext";

interface Props {
  options: {
    option_a: string;
    option_b: string;
  };
  decisionId: string | null;
  onChoiceRecorded: () => void;
  className?: string;
}

const FinalChoiceInput = ({
  options,
  decisionId,
  onChoiceRecorded,
  className,
}: Props) => {
  const sessionId = useSessionId();
  const [finalChoice, setFinalChoice] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFinalChoice = async () => {
    if (!finalChoice) {
      setError("Please select your final choice");
      return;
    }

    if (!sessionId) {
      setError("Session ID not found. Please try making a new decision.");
      return;
    }

    if (!decisionId) {
      setError("Decision ID not found. Please try making a new decision.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await recordFinalChoice(decisionId, finalChoice, sessionId);
      onChoiceRecorded();
    } catch (err) {
      setError("Failed to record your choice. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`${className} mt-4 p-4 bg-gray-50 rounded-lg`}>
      <p className="text-sm text-gray-600 mb-2">What was your final choice?</p>
      <select
        value={finalChoice}
        onChange={(e) => setFinalChoice(e.target.value)}
        className="w-full p-2 border rounded"
      >
        <option value="">Select your choice</option>
        <option value={options.option_a}>{options.option_a}</option>
        <option value={options.option_b}>{options.option_b}</option>
      </select>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      <button
        onClick={handleFinalChoice}
        disabled={isLoading || !finalChoice}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {isLoading ? "Recording..." : "Record Choice"}
      </button>
    </div>
  );
};

export default FinalChoiceInput;

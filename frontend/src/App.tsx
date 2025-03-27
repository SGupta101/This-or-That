import { useState } from "react";
import ChoiceInput from "./components/ChoiceInput";
import DecisionTypeToggle from "./components/DecisionTypeToggle";
import DecisionButton from "./components/DecisionButton";
import History from "./components/History";

function App() {
  const [choices, setChoices] = useState({ choiceA: "", choiceB: "" });
  const [decisionType, setDecisionType] = useState<"reasoned" | "random">(
    "reasoned"
  );

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">This or That</h1>
      <ChoiceInput
        onChoicesChange={(choiceA, choiceB) => setChoices({ choiceA, choiceB })}
      />
      <DecisionTypeToggle
        decisionType={decisionType}
        onToggle={setDecisionType}
      />
      <DecisionButton
        onDecide={() =>
          alert(`Choosing between ${choices.choiceA} and ${choices.choiceB}...`)
        }
      />
      <History />
    </div>
  );
}

export default App;

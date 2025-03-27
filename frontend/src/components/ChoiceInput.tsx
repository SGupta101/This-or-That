import { useState } from "react";

interface Props {
  onChoicesChange: (choiceA: string, choiceB: string) => void;
  className?: string;
}

const ChoiceInput = ({ onChoicesChange, className }: Props) => {
  const [choiceA, setChoiceA] = useState("");
  const [choiceB, setChoiceB] = useState("");

  return (
    <div className={`${className} flex flex-col gap-2`}>
      <input
        type="text"
        className="p-2 border rounded"
        placeholder="First choice"
        value={choiceA}
        onChange={(e) => {
          setChoiceA(e.target.value);
          onChoicesChange(e.target.value, choiceB);
        }}
      />
      <input
        type="text"
        className="p-2 border rounded"
        placeholder="Second choice"
        value={choiceB}
        onChange={(e) => {
          setChoiceB(e.target.value);
          onChoicesChange(choiceA, e.target.value);
        }}
      />
    </div>
  );
};

export default ChoiceInput;

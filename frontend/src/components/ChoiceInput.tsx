import { useState } from "react";

interface Props {
  onChoicesChange: (option_a: string, option_b: string) => void;
  className?: string;
}

const ChoiceInput = ({ onChoicesChange, className = "" }: Props) => {
  const [optionA, setOptionA] = useState("");
  const [optionB, setOptionB] = useState("");

  const handleOptionAChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setOptionA(value);
    onChoicesChange(value, optionB);
  };

  const handleOptionBChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setOptionB(value);
    onChoicesChange(optionA, value);
  };

  return (
    <div className={`flex flex-col space-y-4 ${className}`}>
      <div>
        <label
          htmlFor="optionA"
          className="block text-sm font-medium text-gray-700 mb-1"
        ></label>
        <input
          type="text"
          id="optionA"
          value={optionA}
          onChange={handleOptionAChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Enter option A"
        />
      </div>
      <div>
        <label
          htmlFor="optionB"
          className="block text-sm font-medium text-gray-700 mb-1"
        ></label>
        <input
          type="text"
          id="optionB"
          value={optionB}
          onChange={handleOptionBChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Enter option B"
        />
      </div>
    </div>
  );
};

export default ChoiceInput;

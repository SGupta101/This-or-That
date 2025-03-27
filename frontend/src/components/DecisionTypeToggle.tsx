interface Props {
  decisionType: "reasoned" | "random";
  onToggle: (type: "reasoned" | "random") => void;
}

const DecisionTypeToggle = ({ decisionType, onToggle }: Props) => {
  return (
    <div className="flex items-center gap-4">
      <span className="text-sm">Decision Type:</span>
      <button
        className={`px-4 py-2 rounded ${
          decisionType === "reasoned" ? "bg-blue-500 text-white" : "bg-gray-200"
        }`}
        onClick={() => onToggle("reasoned")}
      >
        Reasoned
      </button>
      <button
        className={`px-4 py-2 rounded ${
          decisionType === "random" ? "bg-blue-500 text-white" : "bg-gray-200"
        }`}
        onClick={() => onToggle("random")}
      >
        Random
      </button>
    </div>
  );
};

export default DecisionTypeToggle;

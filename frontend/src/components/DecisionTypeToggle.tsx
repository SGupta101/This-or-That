interface Props {
  decisionType: "reasoned" | "random";
  onToggle: (type: "reasoned" | "random") => void;
  className?: string;
}

export function DecisionTypeToggle({ decisionType, onToggle, className }: Props) {
  return (
    <div className={`flex items-center gap-4 ${className}`}>
      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
        Decision Type:
      </span>

      {/* Toggle Switch */}
      <label className="relative inline-flex items-center cursor-pointer">
        {/* Hidden Checkbox (Controls Toggle State) */}
        <input
          type="checkbox"
          className="sr-only peer"
          checked={decisionType === "random"}
          onChange={() =>
            onToggle(decisionType === "reasoned" ? "random" : "reasoned")
          }
        />

        {/* Toggle Track (Background) */}
        <div className="w-14 h-8 bg-gray-300 rounded-full peer-checked:bg-green-500 transition-all duration-300 ease-in-out"></div>

        {/* Toggle Knob */}
        <div className="absolute w-6 h-6 bg-white border border-gray-300 rounded-full shadow-md left-1 top-1 transition-all duration-300 ease-in-out peer-checked:translate-x-6 peer-checked:border-white"></div>

        {/* Label Text (Dynamic) */}
        <span className="ml-3 text-sm font-medium text-gray-900 dark:text-gray-100">
          {decisionType === "random" ? "Random" : "Reasoned"}
        </span>
      </label>
    </div>
  );
};

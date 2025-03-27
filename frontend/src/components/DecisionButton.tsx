interface Props {
  onDecide: () => void;
}

const DecisionButton = ({ onDecide }: Props) => {
  return (
    <button
      className="bg-green-500 text-white px-4 py-2 rounded w-full mt-4"
      onClick={onDecide}
    >
      Get a Decision
    </button>
  );
};

export default DecisionButton;

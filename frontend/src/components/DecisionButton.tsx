interface Props {
  onDecide: () => Promise<void>;
  loading: boolean;
  className?: string;
}

const DecisionButton = ({ onDecide, loading, className = '' }: Props) => {
  return (
    <button
      className={`bg-green-500 text-white px-4 py-2 rounded w-full mt-4 ${className} ${
        loading ? 'opacity-50 cursor-not-allowed' : ''
      }`}
      onClick={onDecide}
      disabled={loading}
    >
      {loading ? 'Making Decision...' : 'Get a Decision'}
    </button>
  );
};

export default DecisionButton;

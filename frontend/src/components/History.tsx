const mockHistory = [
  { choiceA: "Pizza", choiceB: "Burger", decision: "Pizza" },
  { choiceA: "Morning run", choiceB: "Evening run", decision: "Evening run" },
];

const History = () => {
  return (
    <div className="mt-6">
      <h2 className="text-lg font-bold">Past Decisions</h2>
      <ul className="mt-2 space-y-2">
        {mockHistory.map((entry, index) => (
          <li key={index} className="p-2 bg-white shadow rounded">
            {entry.choiceA} vs {entry.choiceB} →{" "}
            <strong>{entry.decision}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default History;

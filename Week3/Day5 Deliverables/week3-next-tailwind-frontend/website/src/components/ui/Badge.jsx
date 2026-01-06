export default function Badge({ text, status }) {
  const color =
    status === "online"
      ? "bg-green-100 text-green-600"
      : "bg-gray-200 text-gray-500";

  return (
    <span className={`px-2 py-1 rounded text-xs ${color}`}>{text}</span>
  );
}

export default function Card({ title, value, percentage }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-card">
      <p className="text-sm text-gray-500">{title}</p>
      <h2 className="text-2xl font-bold mt-1">{value}</h2>
      <p className="text-green-500 text-sm mt-2">{percentage}</p>
    </div>
  );
}

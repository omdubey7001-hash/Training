export default function Input({ placeholder, type = "text" }) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className="w-full border px-3 py-2 rounded focus:outline-none focus:ring"
    />
  );
}

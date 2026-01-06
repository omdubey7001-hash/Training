export default function Badge({ children, variant = "teal" }) {
  const variants = {
    teal: "bg-teal-400 text-white",
    gray: "bg-gray-100 text-gray-600",
    red: "bg-red-400 text-white",
    green: "bg-green-400 text-white"
  };

  return (
    <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wide ${variants[variant]}`}>
      {children}
    </span>
  );
}
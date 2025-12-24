export default function Button({ children, variant = "primary" }) {
  const styles = {
    primary: "bg-teal-500 text-white",
    secondary: "bg-gray-200 text-black",
  };

  return (
    <button className={`px-4 py-2 rounded ${styles[variant]}`}>
      {children}
    </button>
  );
}

export default function Button({ 
  children, 
  variant = "primary", 
  className = "", 
  ...props 
}) {
  const baseStyles = "px-4 py-2 rounded-xl font-bold text-xs transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer";
  
  const variants = {
    primary: "bg-teal-400 text-white hover:bg-teal-500 shadow-md",
    secondary: "bg-white text-gray-700 hover:bg-gray-50 border border-gray-100 shadow-sm",
    ghost: "bg-transparent text-gray-500 hover:text-gray-800",
    outline: "border-2 border-teal-400 text-teal-400 hover:bg-teal-50"
  };

  return (
    <button 
      className={`${baseStyles} ${variants[variant]} ${className}`} 
      {...props}
    >
      {children}
    </button>
  );
}
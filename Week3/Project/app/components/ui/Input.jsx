import React from "react";

export default function Input(props) {
  // We extract the values inside the function.
  // This tricks TypeScript into treating them as optional.
  const { 
    label, 
    icon, 
    placeholder, 
    type = "text", 
    className = "",
    ...otherProps // This captures all other props like onChange, value, etc.
  } = props;

  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      {/* Only render label if it exists */}
      {label && <label className="text-xs font-bold text-gray-500 ml-1">{label}</label>}
      
      <div className="relative flex items-center group">
        {/* Only render icon if it exists */}
        {icon && (
          <div className="absolute left-3 text-gray-400 group-focus-within:text-teal-400 transition-colors">
            {icon}
          </div>
        )}
        
        <input
          type={type}
          placeholder={placeholder}
          className={`w-full bg-white border border-gray-200 rounded-xl py-2.5 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition-all shadow-sm ${icon ? "pl-10" : "pl-4"}`}
          {...otherProps} 
        />
      </div>
    </div>
  );
}
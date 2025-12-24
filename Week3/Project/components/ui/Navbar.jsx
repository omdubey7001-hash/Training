import { Search, User, Settings, Bell } from "lucide-react";

export default function Navbar({ pageTitle = "Dashboard" }) {
  return (
    <nav className="flex flex-col md:flex-row md:items-center justify-between gap-4 px-2 py-4 mb-4 sticky top-4 z-40">
      
      {/* Left: Breadcrumbs (Transparent) */}
      <div className="flex flex-col text-gray-800">
        <div className="flex items-center gap-1 text-sm text-gray-500 font-medium">
          <span className="opacity-70 hover:opacity-100 cursor-pointer">Pages</span>
          <span>/</span>
          <span>{pageTitle}</span>
        </div>
        <h1 className="text-sm font-bold mt-1 text-gray-800">{pageTitle}</h1>
      </div>

      {/* Right: Actions (White Pill Shape) */}
      <div className="flex items-center gap-2 sm:gap-4 bg-white px-4 py-2 rounded-2xl shadow-sm border border-gray-100">
        
        {/* Search Input */}
        <div className="relative flex items-center border border-gray-200 rounded-lg px-2 py-1 focus-within:ring-2 focus-within:ring-teal-400 transition-all bg-gray-50/50">
          <div className="text-gray-500 mr-2">
            <Search size={14} />
          </div>
          <input
            type="text"
            placeholder="Type here..."
            className="bg-transparent border-none outline-none text-xs text-gray-600 placeholder-gray-400 w-24 sm:w-32 font-medium"
          />
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3 text-gray-500">
          <button className="flex items-center gap-1 hover:text-teal-500 transition font-bold text-gray-500 text-xs">
            <User size={14} />
            <span className="hidden md:block">Sign In</span>
          </button>
          
          <button className="hover:text-teal-500 transition">
            <Settings size={14} />
          </button>
          
          <button className="hover:text-teal-500 transition">
            <Bell size={14} />
          </button>
        </div>
      </div>
    </nav>
  );
}
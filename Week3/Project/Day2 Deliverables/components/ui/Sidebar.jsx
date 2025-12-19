import Link from "next/link";
import { 
  Home, 
  BarChart2, 
  CreditCard, 
  Wrench, 
  User, 
  FileText, 
  Rocket, 
  HelpCircle 
} from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="h-[calc(100vh-32px)] w-64 m-4 bg-white rounded-xl flex flex-col transition-transform duration-300 shadow-xl border border-gray-100/50 relative z-50">
      
      {/* Logo Area */}
      <div className="flex items-center justify-center h-20 border-b border-gray-100 mb-4 mx-4">
        <div className="flex items-center gap-3 text-gray-800 font-bold tracking-wide text-sm">
          <div className="p-1.5 bg-teal-400 text-white rounded-lg shadow-md">
             <Rocket size={14} fill="currentColor" />
          </div>
          PURITY UI DASHBOARD
        </div>
      </div>

      {/* Navigation Links */}
      <div className="px-4 flex-1 overflow-y-auto">
        <ul className="flex flex-col gap-1 space-y-1">
          
          {/* Active Item (Dashboard) */}
          <li>
            <Link
              href="/"
              className="flex items-center gap-3 px-3 py-2.5 bg-white shadow-md rounded-xl text-gray-800 font-bold text-xs"
            >
              <div className="p-1.5 bg-teal-400 rounded-lg text-white shadow-sm">
                <Home size={14} />
              </div>
              Dashboard
            </Link>
          </li>

          {/* Inactive Items */}
          <NavItem icon={<BarChart2 size={16} />} label="Tables" />
          <NavItem icon={<CreditCard size={16} />} label="Billing" />
          <NavItem icon={<Wrench size={16} />} label="RTL" />

          {/* Section Header */}
          <li className="mt-6 mb-2 px-3 text-[10px] font-bold text-gray-400 uppercase tracking-wider">
            Account Pages
          </li>
          
          <NavItem icon={<User size={16} />} label="Profile" />
          <NavItem icon={<FileText size={16} />} label="Sign In" />
          <NavItem icon={<Rocket size={16} />} label="Sign Up" />
        </ul>
      </div>

      {/* Help Card */}
      <div className="p-4">
        <div className="relative overflow-hidden rounded-2xl bg-teal-400 p-4 text-white shadow-lg">
          <div className="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-white/20" />
          
          <div className="relative z-10 flex h-8 w-8 items-center justify-center rounded-lg bg-white text-teal-500 mb-3 shadow-sm">
            <HelpCircle size={18} />
          </div>
          
          <h4 className="mb-1 text-sm font-bold">Need help?</h4>
          <p className="mb-3 text-[10px] opacity-90">Please check our docs</p>
          
          <button className="w-full rounded-lg bg-white py-2 text-[10px] font-bold text-gray-800 shadow-md hover:bg-gray-50 transition uppercase tracking-wide">
            Documentation
          </button>
        </div>
      </div>
    </aside>
  );
}

// Helper component
function NavItem({ icon, label }) {
  return (
    <li>
      <Link
        href="#"
        className="flex items-center gap-3 px-3 py-2.5 text-gray-500 hover:bg-gray-50 hover:text-gray-800 rounded-xl transition-all text-xs font-semibold group"
      >
        <div className="p-1.5 bg-white rounded-lg text-teal-400 shadow-sm border border-gray-100 group-hover:border-teal-200 transition-colors">
            {icon}
        </div>
        {label}
      </Link>
    </li>
  );
}
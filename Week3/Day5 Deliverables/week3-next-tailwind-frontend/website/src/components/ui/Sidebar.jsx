"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const menuMain = [
  { label: "Dashboard", href: "/dashboard", icon: "🏠" },
  { label: "Tables", href: "/dashboard/users", icon: "📊" },
  { label: "Billing", href: "/dashboard/billing", icon: "💳" },
  { label: "RTL", href: "/dashboard/rtl", icon: "🔧" },
];

const menuAccount = [
  { label: "Profile", href: "/dashboard/profile", icon: "👤" },
  { label: "Sign In", href: "/login", icon: "📄" },
  { label: "Sign Up", href: "/signup", icon: "🚀" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-white px-6 py-8 shadow-card flex flex-col">

      {/* LOGO */}
      <div className="flex items-center gap-2 mb-10">
        <div className="w-6 h-6 border rounded flex items-center justify-center">
          ⧉
        </div>
        <Link
  href="/"
  className="text-xs font-bold tracking-widest text-gray-800 hover:opacity-80"
>
  PURITY UI DASHBOARD
</Link>

      </div>

      {/* MAIN MENU */}
      <nav className="space-y-2">
        {menuMain.map((item) => {
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition
                ${
                  isActive
                    ? "bg-gray-100 text-gray-800"
                    : "text-gray-400 hover:bg-gray-100"
                }`}
            >
              <span
                className={`w-8 h-8 rounded-lg flex items-center justify-center
                  ${
                    isActive
                      ? "bg-[#4FD1C5] text-white"
                      : "bg-gray-100"
                  }`}
              >
                {item.icon}
              </span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* ACCOUNT PAGES */}
      <p className="text-xs font-bold text-gray-500 tracking-wider mt-8 mb-3">
        ACCOUNT PAGES
      </p>

      <nav className="space-y-2">
        {menuAccount.map((item) => {
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition
                ${
                  isActive
                    ? "bg-gray-100 text-gray-800 font-medium"
                    : "text-gray-400 hover:bg-gray-100"
                }`}
            >
              <span
                className={`w-8 h-8 rounded-lg flex items-center justify-center
                  ${
                    isActive
                      ? "bg-[#4FD1C5] text-white"
                      : "bg-gray-100"
                  }`}
              >
                {item.icon}
              </span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* HELP CARD */}
      <div className="mt-6 bg-[#4FD1C5] rounded-2xl p-5 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_top,_white,_transparent)]" />

        <div className="relative">
          <div className="w-8 h-8 bg-white text-[#4FD1C5] rounded-lg flex items-center justify-center mb-3 font-bold">
            ?
          </div>

          <p className="text-sm font-semibold">Need help?</p>
          <p className="text-xs opacity-90 mb-4">
            Please check our docs
          </p>

          <button className="w-full bg-white text-xs font-semibold text-[#4FD1C5] py-2 rounded-lg">
            DOCUMENTATION
          </button>
        </div>
      </div>

    </aside>
  );
}

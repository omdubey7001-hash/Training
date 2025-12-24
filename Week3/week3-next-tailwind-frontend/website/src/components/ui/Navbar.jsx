"use client";

import { usePathname, useRouter } from "next/navigation";

const routeTitleMap = {
  "/dashboard": "Dashboard",
  "/dashboard/users": "Tables",
  "/dashboard/billing": "Billing",
  "/dashboard/profile": "Profile",
  "/dashboard/rtl": "RTL"
};

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter(); 

  const pageTitle = routeTitleMap[pathname] || "Dashboard";

  return (
    <header className="h-20 bg-white px-8 flex items-center justify-between border-b">

      {/* LEFT SECTION */}
      <div className="flex flex-col">
        <p className="text-xs text-gray-400 mb-1">
          Pages / {pageTitle}
        </p>

        <h1 className="text-xs font-bold tracking-widest text-gray-800">
          {pageTitle}
        </h1>
      </div>

      {/* RIGHT SECTION */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <input
            type="text"
            placeholder="Type here..."
            className="pl-10 pr-4 py-2 rounded-xl border text-sm text-gray-500 focus:outline-none"
          />
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
            🔍
          </span>
        </div>
        <button
          onClick={() => router.push("/login")}
          className="text-sm text-gray-500 hover:text-gray-800"
        >
          Sign In
        </button>
      </div>

    </header>
  );
}

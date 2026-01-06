import Link from "next/link";

export default function PublicNavbar({ variant = "default" }) {
    // ================= HERO (SIGNUP / LOGIN) =================
    if (variant === "hero") {
        return (
            <header className="w-full pt-6">
                <div className="max-w-7xl mx-auto px-8 flex justify-between items-center text-white">

                    {/* LOGO */}
                    <div className="flex items-center gap-2 text-xs font-bold tracking-widest">
                        ⧉ PURITY UI DASHBOARD
                    </div>

                    {/* NAV */}
                    <nav className="flex items-center gap-6 text-sm">
                        <Link href="/dashboard">Dashboard</Link>
                        <Link href="/dashboard/profile">Profile</Link>
                        <Link href="/signup">Sign Up</Link>
                        <Link href="/login">Sign In</Link>

                        <button className="ml-4 bg-white text-gray-800 px-5 py-2 rounded-full text-sm font-medium">
                            Free Download
                        </button>
                    </nav>

                </div>
            </header>
        );
    }

    // ================= DEFAULT (WHITE CARD NAVBAR) =================
    return (
        <header className="w-full py-6">
            <div
                className="
          max-w-7xl mx-auto px-8 py-4
          flex justify-between items-center
          bg-white rounded-2xl
          shadow-[0_20px_27px_0_rgba(0,0,0,0.05)]
        "
            >
                {/* LEFT LOGO */}
                <Link
                    href="/"
                    className="text-xs font-bold tracking-widest text-gray-800 hover:opacity-80"
                >
                    PURITY UI DASHBOARD
                </Link>

                {/* RIGHT NAV */}
                <nav className="flex items-center gap-6 text-sm text-gray-600">
                    <Link href="/dashboard">Dashboard</Link>
                    <Link href="/dashboard/profile">Profile</Link>
                    <Link href="/signup">Sign Up</Link>
                    <Link href="/login">Sign In</Link>

                    <button className="ml-4 bg-gray-900 text-white px-4 py-2 rounded-lg text-sm">
                        Free Download
                    </button>
                </nav>
            </div>
        </header>
    );
}

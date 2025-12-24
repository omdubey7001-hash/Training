"use client";

import { useRouter } from "next/navigation";
import PublicNavbar from "@/components/ui/PublicNavbar";

export default function LoginPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-white">
      {/* PUBLIC NAVBAR */}
      <PublicNavbar />

      {/* MAIN CONTENT */}
      <div className="grid grid-cols-1 lg:grid-cols-2 min-h-[calc(100vh-96px)]">
        
        {/* LEFT LOGIN FORM */}
        <div className="flex items-center justify-center px-8">
          <div className="w-full max-w-md">
            <h1 className="text-3xl font-bold text-[#4FD1C5] mb-2">
              Welcome Back
            </h1>
            <p className="text-sm text-gray-400 mb-8">
              Enter your email and password to sign in
            </p>

            <div className="space-y-5">
              <div>
                <label className="text-sm font-medium">Email</label>
                <input
                  type="email"
                  placeholder="Your email address"
                  className="w-full mt-2 px-4 py-3 rounded-xl border focus:outline-none"
                />
              </div>

              <div>
                <label className="text-sm font-medium">Password</label>
                <input
                  type="password"
                  placeholder="Your password"
                  className="w-full mt-2 px-4 py-3 rounded-xl border focus:outline-none"
                />
              </div>

              <div className="flex items-center gap-2">
                <input type="checkbox" defaultChecked />
                <span className="text-sm text-gray-600">
                  Remember me
                </span>
              </div>

              <button
                onClick={() => router.push("/dashboard")}
                className="w-full bg-[#4FD1C5] text-white py-3 rounded-xl font-semibold"
              >
                SIGN IN
              </button>

              <p className="text-sm text-center text-gray-500">
                Don&apos;t have an account?{" "}
                <span className="text-[#4FD1C5] cursor-pointer">
                  Sign up
                </span>
              </p>
            </div>
          </div>
        </div>

        {/* RIGHT TEAL PANEL */}
        <div className="hidden lg:flex items-center justify-center bg-[#4FD1C5] rounded-bl-[80px]">
          <div className="text-white text-4xl font-bold flex items-center gap-4">
            ⚡ chakra
          </div>
        </div>

      </div>
    </div>
  );
}

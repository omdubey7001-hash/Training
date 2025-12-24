"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import PublicNavbar from "@/components/ui/PublicNavbar";

export default function SignupPage() {
  const router = useRouter();

  const handleSignup = () => {
    // simulate successful signup
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen bg-white relative overflow-hidden">

      {/* TOP TEAL SECTION */}
      <div className="relative bg-[#4FD1C5] h-[420px] rounded-b-[20px]">

        <PublicNavbar variant="hero" />

        <div className="text-center text-white mt-12">
          <h1 className="text-3xl font-bold">Welcome!</h1>
          <p className="text-sm opacity-90 mt-2">
            Use these awesome forms to login or create new account in your project for free.
          </p>
        </div>
      </div>

      {/* SIGNUP CARD */}
      <div className="relative -mt-40 flex justify-center">
        <div className="bg-white w-[420px] rounded-2xl shadow-[0_20px_27px_rgba(0,0,0,0.05)] p-8">

          <h2 className="text-center font-semibold mb-6">Register with</h2>

          {/* SOCIAL BUTTONS (UI ONLY) */}
          <div className="flex justify-center gap-4 mb-4">
            <SocialButton label="f" />
            <SocialButton label="" />
            <SocialButton label="G" />
          </div>

          <p className="text-center text-gray-400 text-sm mb-6">or</p>

          {/* FORM */}
          <div className="space-y-4 text-sm">
            <Input label="Name" placeholder="Your full name" />
            <Input label="Email" placeholder="Your email address" />
            <Input label="Password" placeholder="Your password" type="password" />
          </div>

          {/* REMEMBER ME */}
          <div className="flex items-center gap-2 mt-4 text-sm">
            <input type="checkbox" className="accent-[#4FD1C5]" />
            Remember me
          </div>

          {/* SIGN UP BUTTON */}
          <button
            onClick={handleSignup}
            className="w-full mt-6 bg-[#4FD1C5] text-white py-3 rounded-xl font-semibold hover:opacity-90"
          >
            SIGN UP
          </button>

          {/* FOOTER LINK */}
          <p className="text-center text-sm text-gray-400 mt-6">
            Already have an account?{" "}
            <Link href="/login" className="text-[#4FD1C5] font-semibold">
              Sign in
            </Link>
          </p>
        </div>
      </div>

      {/* FOOTER */}
      <footer className="text-xs text-gray-400 text-center mt-16">
        © 2021, Made with ❤️ by Creative Tim & Simmmple for a better web
      </footer>
    </div>
  );
}

/* ================= HELPER COMPONENTS ================= */

function SocialButton({ label }) {
  return (
    <button className="w-12 h-12 border rounded-xl flex items-center justify-center font-bold text-gray-700">
      {label}
    </button>
  );
}

function Input({ label, ...props }) {
  return (
    <div>
      <label className="block mb-1 text-gray-600">{label}</label>
      <input
        {...props}
        className="w-full px-4 py-3 border rounded-xl focus:outline-none"
      />
    </div>
  );
}

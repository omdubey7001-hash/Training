import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="bg-white text-gray-800">

      {/* ================= HERO SECTION ================= */}
      <section className="bg-gradient-to-br from-teal-500 to-cyan-400 text-white">
        <div className="max-w-7xl mx-auto px-6 py-28 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-6">
            Build Faster with a Modern SaaS Dashboard
          </h1>

          <p className="max-w-2xl mx-auto text-lg opacity-90 mb-10">
            A clean, responsive, and scalable dashboard solution built with
            Next.js and Tailwind CSS — perfect for real-world applications.
          </p>

          <div className="flex justify-center gap-4">
            <Link
              href="/dashboard"
              className="bg-white text-teal-600 px-6 py-3 rounded-xl font-semibold shadow hover:scale-105 transition"
            >
              Get Started
            </Link>

            <Link
              href="/signup"
              className="border border-white px-6 py-3 rounded-xl font-semibold hover:bg-white hover:text-teal-600 transition"
            >
              Create Account
            </Link>
          </div>
        </div>
      </section>

      {/* ================= FEATURES GRID ================= */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-14">
            Powerful Features
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Feature
              title="Modern Tech Stack"
              desc="Built using Next.js App Router and Tailwind CSS for speed and scalability."
            />
            <Feature
              title="Clean UI Design"
              desc="Minimal and professional design inspired by modern SaaS products."
            />
            <Feature
              title="Fully Responsive"
              desc="Looks great on desktops, tablets, and mobile devices."
            />
          </div>
        </div>
      </section>

      {/* ================= TESTIMONIALS ================= */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-14">
            What Our Users Say
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Testimonial
              name="Ankan Sharma"
              role="Frontend Developer"
              text="This dashboard saved me weeks of development time. Clean, fast, and easy to use."
            />
            <Testimonial
              name="Priyanshu Verma"
              role="Product Manager"
              text="The UI looks professional and works perfectly across all devices."
            />
            <Testimonial
              name="Mahak Singh"
              role="Startup Founder"
              text="A solid foundation for building SaaS products quickly."
            />
          </div>
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer className="bg-gray-900 text-gray-300 py-10">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <span>© 2025 SaaS Dashboard. All rights reserved.</span>

          <div className="flex gap-6 text-sm">
            <Link href="#">About</Link>
            <Link href="#">Docs</Link>
            <Link href="#">Privacy</Link>
            <Link href="#">Contact</Link>
          </div>
        </div>
      </footer>

    </div>
  );
}

/* ================= COMPONENTS ================= */

function Feature({ title, desc }) {
  return (
    <div className="bg-white rounded-2xl p-8 shadow hover:shadow-lg transition">
      <h3 className="text-xl font-semibold mb-3">{title}</h3>
      <p className="text-gray-600">{desc}</p>
    </div>
  );
}

function Testimonial({ name, role, text }) {
  return (
    <div className="bg-white rounded-2xl p-8 shadow hover:shadow-lg transition">
      <p className="text-gray-600 mb-6">“{text}”</p>
      <div className="font-semibold">{name}</div>
      <div className="text-sm text-gray-400">{role}</div>
    </div>
  );
}

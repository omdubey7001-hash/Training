export default function DashboardPage() {
  return (
    <div className="space-y-6">

      {/* ================= SMALL STAT CARDS (DO NOT TOUCH) ================= */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <SmallStat title="Today's Money" value="$53,000" change="+55%" />
        <SmallStat title="Today's Users" value="2,300" change="+5%" />
        <SmallStat title="New Clients" value="+3,052" change="-14%" />
        <SmallStat title="Total Sales" value="$173,000" change="+8%" />
      </div>

      {/* ================= LARGE CARDS SECTION (FIXED) ================= */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        {/* LEFT – INFO CARD */}
        <div className="bg-white rounded-2xl p-6 shadow-card h-[260px] flex flex-col justify-between">
          <div>
            <p className="text-sm text-gray-400">Built by developers</p>
            <h3 className="text-lg font-semibold mt-1">
              Purity UI Dashboard
            </h3>
            <p className="text-sm text-gray-500 mt-2 max-w-sm">
              From colors, cards, typography to complex elements,
              you will find the full documentation.
            </p>
          </div>

          <button className="text-sm font-medium text-gray-700 w-fit">
            Read more →
          </button>
        </div>

        {/* RIGHT – CHAKRA CARD */}
        <div className="bg-[#4FD1C5] rounded-2xl shadow-card h-[260px] flex items-center justify-center">
          <div className="text-white text-3xl font-bold flex items-center gap-3">
            ⚡ chakra
          </div>
        </div>
      </div>

      {/* ================= SECOND LARGE ROW ================= */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        {/* BAR CHART PLACEHOLDER */}
        <div className="bg-gradient-to-r from-gray-900 to-gray-700 rounded-2xl shadow-card h-[280px]" />

        {/* SALES OVERVIEW */}
        <div className="bg-white rounded-2xl shadow-card h-[280px] p-6">
          <h3 className="font-semibold">Sales overview</h3>
          <p className="text-sm text-green-500 mb-4">
            (+5) more in 2021
          </p>

          <div className="w-full h-full bg-gray-100 rounded-xl" />
        </div>
      </div>

    </div>
  );
}

/* ================= COMPONENTS ================= */

function SmallStat({ title, value, change }) {
  const isPositive = change.startsWith("+");

  return (
    <div className="bg-white rounded-2xl shadow-card p-5 flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-400">{title}</p>
        <h3 className="text-xl font-bold">{value}</h3>
        <span
          className={`text-sm font-semibold ${
            isPositive ? "text-green-500" : "text-red-500"
          }`}
        >
          {change}
        </span>
      </div>

      <div className="w-12 h-12 bg-[#4FD1C5] rounded-xl" />
    </div>
  );
}

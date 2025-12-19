export default function Navbar() {
  return (
    <header className="h-16 bg-white border-b flex items-center px-6">
      
      {/* Left: Logo */}
      <div className="text-sm font-semibold text-gray-800 w-56">
        Purity UI Dashboard
      </div>

      {/* Middle: Page Title (aligned with content, NOT center) */}
      <div className="flex-1 pl-6">
        <p className="text-xs text-gray-400">Pages / Tables</p>
        <h2 className="text-lg font-semibold text-gray-900">Tables</h2>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Type here..."
          className="px-4 py-2 text-sm border rounded-lg focus:outline-none"
        />
        <span className="text-sm text-gray-600 cursor-pointer">
          Sign In
        </span>
      </div>
    </header>
  );
}

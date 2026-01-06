import Sidebar from "@/components/ui/Sidebar";
import Navbar from "@/components/ui/Navbar";

export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar is fixed */}
      <Sidebar />

      {/* Content wrapper accounts for sidebar ONCE */}
      <div className="ml-64">
        <Navbar />

        {/* CONTAIN PAGE WIDTH */}
        <main className="p-6 max-w-[calc(100vw-16rem)]">
          {children}
        </main>
      </div>
    </div>
  );
}

import PublicNavbar from "@/components/ui/PublicNavbar";

export default function PublicLayout({ children }) {
  return (
    <div className="min-h-screen bg-white">
      <PublicNavbar />
      {children}
    </div>
  );
}

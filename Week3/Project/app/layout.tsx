import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "./components/ui/Sidebar";
import Navbar from "./components/ui/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Purity UI Dashboard",
  description: "Dashboard Skeleton",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 text-slate-800`}>
        <div className="flex min-h-screen relative">
          
          {/* Sidebar: Fixed position on left */}
          <div className="fixed inset-y-0 left-0 z-50 w-64">
             <Sidebar />
          </div>

          {/* Main Content: 
              Added 'ml-72' (margin-left) to push everything to the right. 
              The value 72 is slightly larger than the sidebar width (64) for spacing.
          */}
          <main className="flex-1 ml-72 p-4 transition-all duration-300">
            <Navbar pageTitle="Tables" />
            
            <div className="px-2">
              {children}
            </div>
          </main>
        
        </div>
      </body>
    </html>
  );
}
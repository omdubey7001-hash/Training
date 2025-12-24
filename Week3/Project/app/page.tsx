"use client";

import { useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import Badge from "../components/ui/Badge";
import Modal from "../components/ui/Modal";
import { Search, Plus, Filter } from "lucide-react";

export default function Home() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="flex flex-col gap-6">
      
      {/* 1. Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
           <h2 className="text-2xl font-bold text-gray-800">Dashboard Overview</h2>
           <p className="text-gray-500 text-sm">Check your daily stats and tasks.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => alert("Filter clicked")}>
            <Filter size={16} /> Filter
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            <Plus size={16} /> New Project
          </Button>
        </div>
      </div>

      {/* 2. Simple Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="flex flex-col gap-2">
          <p className="text-gray-400 text-xs font-bold uppercase">Server Status</p>
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-teal-400 animate-pulse" />
            <h3 className="text-lg font-bold text-gray-700">Online</h3>
            <Badge variant="teal">98% Uptime</Badge>
          </div>
        </Card>

        <Card className="flex flex-col gap-2">
          <p className="text-gray-400 text-xs font-bold uppercase">Pending Tasks</p>
          <div className="flex items-center gap-2">
             <h3 className="text-lg font-bold text-gray-700">12 Items</h3>
             <Badge variant="gray">To Do</Badge>
          </div>
        </Card>

        <Card className="flex flex-col gap-2">
          <p className="text-gray-400 text-xs font-bold uppercase">System Alerts</p>
          <div className="flex items-center gap-2">
             <h3 className="text-lg font-bold text-gray-700">1 Error</h3>
             <Badge variant="red">Attention</Badge>
          </div>
        </Card>
      </div>

      {/* 3. Main Content Area (Ready for Table) */}
      <Card className=  "flex-1 flex flex-col gap-6 min-h-[400px]">
        
        {/* Card Header */}
        <div className="flex justify-between items-center border-b border-gray-100 pb-4">
          <h3 className="font-bold text-gray-800 text-lg">Authors Table</h3>
          <div className="w-64">
            <Input placeholder="Search authors..." icon={<Search size={16} />} />
          </div>
        </div>

        {/* Empty State Placeholder */}
        <div className="flex-1 flex flex-col items-center justify-center text-gray-400 bg-gray-50/50 rounded-xl border border-dashed border-gray-200 m-2">
           <div className="p-4 bg-white rounded-full shadow-sm mb-3">
             <Filter size={24} className="text-teal-400" />
           </div>
           <p className="font-medium">No data available yet</p>
           <p className="text-sm">We will build the table rows in the next step.</p>
        </div>

      </Card>

      {/* Modal Component */}
      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title="Add New Project"
      >
        <div className="flex flex-col gap-4">
          <Input label="Project Name" placeholder="e.g. Dashboard Redesign" />
          <Input label="Budget" placeholder="$0.00" type="number" />
          
          <div className="flex justify-end gap-2 mt-4 pt-4 border-t border-gray-100">
             <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
             <Button onClick={() => setIsModalOpen(false)}>Create Project</Button>
          </div>
        </div>
      </Modal>

    </div>
  );
}
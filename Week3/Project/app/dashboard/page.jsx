import Card from "@/components/ui/Card";

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card title="Users" value="120" />
      <Card title="Revenue" value="$3,200" />
      <Card title="Growth" value="+18%" />
    </div>
  );
}

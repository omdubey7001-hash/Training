import Card from "@/components/ui/Card";

export default function ProfilePage() {
  return (
    <div className="max-w-xl">
      <Card>
        <h2 className="text-xl font-semibold">User Profile</h2>
        <p className="text-gray-600 mt-2">
          Static profile page using nested routing.
        </p>
      </Card>
    </div>
  );
}

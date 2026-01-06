import Badge from "@/components/ui/Badge";

const users = [
  {
    name: "Esthera Jackson",
    email: "esthera@mail.com",
    role: "Manager",
    status: "online",
    date: "14/06/21",
  },
  {
    name: "Alexa Liras",
    email: "alexa@mail.com",
    role: "Developer",
    status: "offline",
    date: "14/06/21",
  },
];

export default function UsersPage() {
  return (
    <div className="bg-white rounded-2xl shadow-card p-6">
      <h2 className="text-lg font-semibold mb-4">Authors Table</h2>

      <table className="w-full border-collapse">
        <thead className="text-xs text-gray-400 uppercase bg-gray-50">
          <tr>
            <th className="px-6 py-4 text-left">Author</th>
            <th className="text-left">Function</th>
            <th>Status</th>
            <th>Employed</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u, i) => (
            <tr key={i} className="border-b last:border-none">
              <td className="px-6 py-4">
                <p className="font-medium">{u.name}</p>
                <p className="text-sm text-gray-400">{u.email}</p>
              </td>
              <td>
                <p className="text-sm">{u.role}</p>
              </td>
              <td>
                <Badge text={u.status} status={u.status} />
              </td>
              <td className="text-sm text-gray-500">{u.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

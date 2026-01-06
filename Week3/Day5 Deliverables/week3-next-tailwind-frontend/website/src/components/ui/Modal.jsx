export default function Modal({ title, children }) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
      <div className="bg-white p-6 rounded w-96">
        <h3 className="font-semibold mb-4">{title}</h3>
        {children}
      </div>
    </div>
  );
}

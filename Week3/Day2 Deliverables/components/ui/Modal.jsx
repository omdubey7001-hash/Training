export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[999] flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="bg-white w-full max-w-md rounded-2xl shadow-2xl p-6 relative animate-in fade-in zoom-in duration-200">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-gray-800">{title}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="text-gray-600 text-sm">
          {children}
        </div>

        {/* Footer Buttons Example */}
        <div className="mt-6 flex justify-end gap-2">
           <button onClick={onClose} className="px-4 py-2 text-sm font-bold text-gray-500 hover:bg-gray-100 rounded-xl">Close</button>
        </div>
      </div>
    </div>
  );
}
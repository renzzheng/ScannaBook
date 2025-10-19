export default function History() {
  return (
    <div className="relative min-h-screen font-sans">
      {/* Gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-800 to-blue-700"></div>
      <div className="absolute inset-0 bg-[url('/trans-papers.png')] bg-cover bg-center blur-[0px]"></div>

      {/* Optional overlay for readability */}
      <div className="absolute inset-0 bg-black/30"></div>

      {/* Page content */}
      <div className="relative z-10 flex items-center justify-center min-h-screen text-white">
        <h1 className="text-3xl font-bold">📚 Your Saved Books</h1>
      </div>
    </div>
  );
}

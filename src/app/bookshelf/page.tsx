export default function Bookshelf() {
  return (
    <div className="relative min-h-screen font-sans">
      {/* Background image with blur */}
      {/* <div className="absolute inset-0 bg-[url('/librarybackground.png')] bg-cover bg-center blur-[4px]"></div> */}
      <div className="absolute inset-0 bg-[url('/librarybackground.png')] bg-cover bg-center blur-[4px]"></div>


      {/* Optional overlay for readability */}
      <div className="absolute inset-0 bg-black/30"></div>

      {/* Page content */}
      <div className="relative z-10 flex items-center justify-center min-h-screen text-white">
        <h1 className="text-3xl font-bold">📚 Your Saved Books</h1>
      </div>
    </div>
  );
}
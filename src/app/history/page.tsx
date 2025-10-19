export default function History() {
  return (
    <div className="relative min-h-screen font-sans">
      {/* Background */}
      <div className="absolute inset-0 bg-[url('/setting.png')] bg-cover bg-center blur-[6px]"></div>

      {/* Overlay */}
      <div className="absolute inset-0 bg-black/30"></div>

      {/* Centered content */}
      <div className="relative z-10 flex items-center justify-center min-h-screen w-full text-white">
        <h1 className="text-3xl font-Roboto text-center">
          Your most recent searches will appear here
        </h1>
      </div>
    </div>
  );
}

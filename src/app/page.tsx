import Image from "next/image";
import HeroSection from "../components/HeroSection";
import BookCard from "../components/card"

export default function Home() {
  // Example array of book cover image URLs
  const bookCovers = [
    "/covers/book1.jpg",
    "/covers/book2.jpg",
    "/covers/book3.jpg",
    "/covers/book4.jpg",
  ];

  return (
    <div className="relative min-h-screen font-sans">
      {/* Background image */}
      <div className="blur-[2px] absolute inset-0 bg-[url('/bookshelf-bg.png')] bg-cover bg-center"></div>

      {/* Dark overlay for readability */}
      <div className="absolute inset-0 bg-black/60"></div>

      {/* Page content */}
      <div className="relative z-10 grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 text-white">

        {/* Main section */}
        <main className="flex flex-col gap-[32px] row-start-2 items-center text-center">
          <Image
            src="/ascii-art-text.png"
            alt="BookScanner logo"
            width={1000}
            height={1}
            className="h-20 w-auto"
            priority
          />
          <HeroSection />
          <p className="font-Roboto text-xl text-center">
            Welcome to your personal digital librarian.
          </p>
        </main>

        <BookCard thumbnail="/yes.png"></BookCard>
        
        {/* Footer */}
        <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
          <a
            className="flex items-center gap-2 hover:underline hover:underline-offset-4"
            href="https://nextjs.org/learn"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image aria-hidden src="/file.svg" alt="File icon" width={16} height={16} />
            Presentation
          </a>
          <a
            className="flex items-center gap-2 hover:underline hover:underline-offset-4"
            href="https://vercel.com/templates?framework=next.js"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image aria-hidden src="/window.svg" alt="Window icon" width={16} height={16} />
            Demo Video
          </a>
          <a
            className="flex items-center gap-2 hover:underline hover:underline-offset-4"
            href="https://nextjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image aria-hidden src="/globe.svg" alt="Globe icon" width={16} height={16} />
            Credits
          </a>
        </footer>
      </div>
    </div>
  );
}
'use client';
import React, { useEffect, useState } from "react";
import Image from "next/image";
import HeroSection from "../components/HeroSection";
import ResultBox from "../components/result";
import ImageUpload from "../components/ImageUpload";

interface BookData {
  title?: string;
  rating?: number;
  author?: string;
  description?: string;
  thumbnail?: string;
}

export default function Home() {
  const [offsetY, setOffsetY] = useState(0);
  const [books, setBooks] = useState<BookData[]>([]);

  useEffect(() => {
    const handleScroll = () => {
      // Smooth performance using requestAnimationFrame
      requestAnimationFrame(() => setOffsetY(window.scrollY));
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="relative min-h-screen font-sans overflow-x-hidden">
      {/* 🌄 Background with smooth parallax */}
      <div
        className="absolute inset-0 blur-[2.5px] bg-[url('/bookshelf-bg.png')] bg-cover bg-center will-change-transform"
        style={{
          transform: `translateY(${offsetY * 0.3}px)`, // 0.3 = subtle parallax speed
        }}
      ></div>

      {/* Dark overlay for readability */}
      <div className="fixed inset-0 bg-black/30"></div>

      {/* Page content */}
      <div className="relative z-10 grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 text-white">
        <main className="flex flex-col gap-[32px] row-start-2 items-center text-center">
          <HeroSection>
            <ImageUpload onUploadSuccess={setBooks} />
          </HeroSection>

          <ResultBox
            books={books}
          />

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
        </main>
      </div>
    </div>
  );
}

'use client';
import React from "react";

const navItems = [
  { name: "BookScanner", href: "/" }, // main page for uploads and search
  { name: "Bookshelf", href: "/bookshelf" },
  { name: "History", href: "/history" }
];

export default function Navbar() {
  return (
    <nav
      className="
        absolute top-0 left-0 z-20 w-full
        flex justify-center gap-x-6 p-6
        bg-transparent text-white
      "
    >
      {navItems.map((item) => (
        <div
          key={item.name}
          className="
            relative rounded-full p-[1.5px]
            bg-gradient-to-br from-gray-100/80 via-gray-400/50 to-gray-700/70
            hover:from-gray-200/90 hover:via-gray-500/60 hover:to-gray-800/80
            transition-all duration-200
          "
        >
          <div
            className="
              rounded-full bg-white/10 backdrop-blur-md
              px-5 py-2 text-base font-sans
              hover:bg-white/20 transition-colors duration-200
            "
          >
            <a href={item.href}>{item.name}</a>
          </div>
        </div>
      ))}
    </nav>
  );
}

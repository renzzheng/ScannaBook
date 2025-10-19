'use client';
import React from "react";

const navItems = [
  { name: "BookScanner", href: "/" },
  { name: "Bookshelf", href: "/bookshelf" },
  { name: "History", href: "/history" },
];

export default function Navbar() {
  return (
    <nav className="absolute top-0 left-0 z-20 w-full flex justify-center gap-4 p-6">
      {navItems.map((item) => (
        <a
          key={item.name}
          href={item.href}
          className="
            relative rounded-full
            border border-white/20
            bg-white/10 backdrop-blur-md
            shadow-md
            px-5 py-2
            hover:bg-white/15
            transition
            flex justify-center items-center
            text-base font-sans text-center text-white
          "
        >
          {item.name}
        </a>
      ))}
    </nav>
  );
}

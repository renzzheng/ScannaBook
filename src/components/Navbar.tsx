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
        <a
          key={item.name}
          href={item.href}
          className="
            px-5 py-2 rounded-full
            bg-white/10 hover:bg-white/20
            backdrop-blur-md
            text-sm font-medium
            transition-colors duration-200
          "
        >
          {item.name}
        </a>
      ))}
    </nav>
  );
}

'use client';
import React from "react";

// EXAMPLE NAV BAR 

const navItems = [
  { name: "BookScanner", href: "/" }, //main page for uploads and search
  { name: "Bookshelf", href: "/bookshelf" },
  { name: "History" , href: "/History"}
];

export default function Navbar() {
  return (
    <nav className="
      sticky top-0 z-5 flex w-full items-center 
      justify-start gap-x-8 p-4 bg-transparent
      backdrop-blur-sm rounded-2xl">

      {navItems.map((item) => (
        <a
          key={item.name}
          href={item.href}
          className="text-white hover:text-red-400 px-3 py-2 max-w-sm bg-slate-900 rounded-md text-sm font-medium transition-colors"
        >
          {item.name}
        </a>
      ))}

    </nav>
  );
}

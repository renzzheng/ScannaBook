import React, { useState, useEffect } from 'react';

// Define the structure of a single book object
interface BookData {
  title: string;
  authors: string[];
  rating: number;
  description: string;
  thumbnail: string;
}

// Define the props for our filter component
// It now includes an onSort callback function
interface BookFilterProps {
  activeMethod: SortMethod;
  onSort: (method: SortMethod) => void;
}

export type SortMethod = 'title' | 'author' | 'rating';

export default function BookFilter({ activeMethod, onSort }: BookFilterProps) {

  const SortButton = ({ method, children }: { method: 'title' | 'author' | 'rating', children: React.ReactNode }) => (
    <button
      onClick={() => onSort(method)}
      className={`bg-transparent px-4 py-1.5 text-black text-sm font-medium rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-gray-500 ${activeMethod === method
        ? 'bg-white/25 text-gray'
        : 'text-gray hover:bg-gray-100 hover:text-black'
        }`}
    >
      {children}
    </button>
  );

  return (
    // This is the standalone filter component UI
    <div className="bg-white/20 backdrop-blur-md flex items-center justify-center space-x-2 my-8 p-1 rounded-full border border-gray-200 shadow-sm max-w-md mx-auto">
      <SortButton method="title">Sort by Title</SortButton>
      <div className="w-px h-5 bg-gray-300"></div>
      <SortButton method="author">Sort by Author</SortButton>
      <div className="w-px h-5 bg-gray-300"></div>
      <SortButton method="rating">Sort by Rating</SortButton>
    </div>
  );
};

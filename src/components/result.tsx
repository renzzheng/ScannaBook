'use client';
import { useState, useEffect } from "react";
import React from "react";
import BookCard from "./card";

type SortMethod = 'rating' | 'author' | 'title';

export interface BookData {
  title?: string;
  rating?: number;
  author?: string;
  description?: string;
  thumbnail?: string;
}

interface ResultBoxProps {
  books: BookData[];
}

export default function ResultBox({ books }: ResultBoxProps) {
  const [displayedBooks, setDisplayedBooks] = useState<BookData[]>([]);
  const [sortMethod, setSortMethod] = useState<SortMethod>('rating');

  // This useEffect hook handles all the sorting logic
  useEffect(() => {
    const booksToSort = [...(books || [])];
    booksToSort.sort((a, b) => {
      switch (sortMethod) {
        case 'title':
          return (a.title || '').localeCompare(b.title || '');
        case 'author':
          return (a.author || '').localeCompare(b.author || '');
        case 'rating':
          return (b.rating || 0) - (a.rating || 0);
        default:
          return 0;
      }
    });
    setDisplayedBooks(booksToSort);
  }, [books, sortMethod]); // It re-runs whenever 'books' or 'sortMethod' changes

  // Define the SortButton sub-component directly inside ResultBox
  // It now uses 'sortMethod' and 'setSortMethod' from ResultBox's state
  const SortButton = ({ method, children }: { method: SortMethod, children: React.ReactNode }) => (
    <button
      onClick={() => setSortMethod(method)} // Use setSortMethod directly
      className={`bg-transparent px-4 py-1 text-black text-sm font-medium rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-gray-500 ${
        sortMethod === method // Use sortMethod directly
          ? 'bg-white/25 text-black' // Active button colors
          : 'text-gray-300 hover:bg-white/10 hover:text-black' // Inactive button colors
      }`}
    >
      {children}
    </button>
  );

  return (
    <div className="relative mt-8 w-full max-w-5xl rounded-2xl p-6 bg-transparent ">
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 text-white shadow-md border border-white/20">
        
        {/* This is the filter UI, now inlined from BookFilter.tsx */}
        <div className="bg-white/20 backdrop-blur-md flex items-center justify-center space-x-2 my-8 p-1 rounded-full border border-gray-200/50 shadow-sm max-w-sm mx-auto">
          <SortButton method="title">Sort by Title</SortButton>
          <div className="w-px h-5 bg-gray-400"></div>
          <SortButton method="author">Sort by Author</SortButton>
          <div className="w-px h-5 bg-gray-400"></div>
          <SortButton method="rating">Sort by Rating</SortButton>
        </div>
        {/* End of inlined filter UI */}

        <h2 className="text-2xl font-semibold mb-4 text-center">Search Results</h2>

        {displayedBooks.length === 0 ? (
          <p className="text-center text-gray-400">No books to display.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 place-items-start"> {/* Changed to place-items-start */}
            {displayedBooks.map((book, index) => (
              <BookCard
                key={index}
                title={book.title}
                author={book.author}
                rating={book.rating}
                description={book.description}
                thumbnail={book.thumbnail}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

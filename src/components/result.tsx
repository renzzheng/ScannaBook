'use client';
import { useState, useEffect } from "react";
import React from "react";
import BookCard from "./card";
import { SortMethod } from "./Filter";
import BookFilter from "./Filter";

interface BookData {
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
  }, [books, sortMethod]);

  return (
    <div className="relative mt-8 w-full max-w-5xl rounded-2xl p-6 bg-transparent">
      <div
        className="
          bg-white/10 backdrop-blur-md rounded-2xl p-6 text-white shadow-md
          border border-white/20
        "
      >
        {/* Book filter */}
        <BookFilter activeMethod={sortMethod} onSort={setSortMethod} />
        <h2 className="text-2xl font-semibold mb-4">Search Results</h2>

        {displayedBooks.length === 0 ? (
          <p className="text-center text-gray-400">No books to display.</p>
        ) : (
          <div className="flex justify-center gap-8">
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

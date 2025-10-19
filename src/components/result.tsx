'use client';
import React from "react";
import BookCard from "./card";

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
  return (
    <div className="relative mt-8 w-full max-w-5xl rounded-2xl p-6 bg-transparent ">
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 text-white shadow-md hover:bg-white/15 transition">
        <h2 className="text-2xl font-semibold mb-4">Search Results</h2>
        <div className="flex justify-center gap-8">
          {books.map((book, index) => (
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
      </div>
    </div>
  );
}

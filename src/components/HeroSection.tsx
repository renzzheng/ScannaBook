import React from 'react';
import ImageUpload from './ImageUpload';

export default function HeroSection() {
  return (
    <section className="bg-transparent text-gray-200 w-full rounded-2xl">
      <div className="container mx-auto flex flex-col items-center justify-center py-15 px-4 text-center">

        {/* Main Headline */}
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-gray-200 to-blue-400 mb-4">
          Welcome to Scannabook
        </h1>

        {/* Subheading */}
        <p className="max-w-2xl text-lg md:text-xl text-gray-200 mb-8 font-Roboto">
          The simplest way to digitize your physical library. Scan your books to unlock a world of digital notes, search, and accessibility.
        </p>
 
        {/* Call to Action Button */}
        <div className="
        w-full flex justify-center mt-6 relative rounded-full
        rounded-base px-6 py-2 text-white
        ">
          <ImageUpload />
        </div>

      </div>
    </section>
  );
};

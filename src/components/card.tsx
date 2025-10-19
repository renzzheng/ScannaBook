import React from "react";
import Image from "next/image";

interface BookCardProps {
  title?: string;
  rating?: number;
  author?: string;
  description?: string;
  thumbnail?: string; // Book cover image
}

export default function BookCard({
  title,
  rating,
  author,
  description,
  thumbnail,
}: BookCardProps) {
  return (
    <div className="relative mt-8 w-full max-w-xl rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md p-6 text-white shadow-md hover:bg-white/15 transition flex gap-4">
  {/* Thumbnail on the left */}
  {thumbnail && (
    <div className="flex-shrink-0 overflow-hidden rounded-xl">
      <Image
        src={thumbnail}
        alt={title || "Book cover"}
        width={100}   // fixed width
        height={150}  // fixed height
        className="object-cover w-[100px] h-[150px]"
      />
    </div>
  )}

     {/* Text content wraps on the right */}
  <div className="flex-1">
    <h2 className="text-xl font-semibold mb-1">{title || "Untitled Book"}</h2>
    <p className="text-sm text-gray-200 mb-1">{author || "Unknown Author"}</p>
    {rating && (
      <p className="text-yellow-400 text-sm mb-1">⭐ {rating.toFixed(1)}</p>
    )}
    <p className="text-sm text-gray-300">{description || "No description available."}</p>
  </div>
</div>
  );
}

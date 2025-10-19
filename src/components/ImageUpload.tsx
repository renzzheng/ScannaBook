'use client';
import React, { useRef, useState, useEffect } from "react";
import { Camera } from "lucide-react";

interface ImageUploadProps {
  className?: string;
}

export default function ImageUpload({ className }: ImageUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Trigger hidden file input
  const handleChooseFile = () => fileInputRef.current?.click();

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
  };

  // Generate preview when file changes
  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const handleConfirm = () => {
    if (!file) return;
    console.log("Uploading file:", file);
    alert(`Uploading ${file.name}`);
    setFile(null);
  };

  const handleCancel = () => setFile(null);

  return (
    <div
      className={`
        flex flex-col items-center justify-center gap-4 mt-6 
        p-[10px] border border-white/20 backdrop-blur-md shadow-md 
        bg-white/10 text-white transition-all duration-300 ease-in-out
        ${file ? "rounded-2xl py-6 px-8" : "rounded-full px-4 py-3"}
        ${className || ""}
      `}
    >
      {/* Hidden file input */}
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Upload button */}
      {!file ? (
        <button
          onClick={handleChooseFile}
          className="
            flex items-center gap-2
            relative rounded-full px-6 py-2 text-white font-sans text-base
            border bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/30
            backdrop-blur-md shadow-md hover:bg-white/20 
            transition-colors duration-200
          "
        >
          <Camera size={22} strokeWidth={1.25} className="text-white/70" />
          Upload Image
        </button>
      ) : (
        <div className="flex flex-col items-center gap-4">
          {/* Thumbnail preview */}
          {previewUrl && (
            <img
              src={previewUrl}
              alt="Preview"
              className="w-48 h-auto rounded-xl border border-white/20 object-cover"
            />
          )}

          {/* File name */}
          <p className="text-gray-200 text-sm text-center break-words max-w-[12rem]">
            {file.name}
          </p>

          {/* Confirm / Cancel buttons */}
          <div className="flex gap-4">
  <button
    onClick={handleConfirm}
    className="
      rounded-full px-6 py-2 text-white font-sans text-base
      border bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/30
      backdrop-blur-md shadow-md
      hover:bg-white/20 transition-colors duration-200
    "
  >
    Confirm Upload
  </button>

{/* cancel button */}
  <button
    onClick={handleCancel}
    className="
      rounded-full px-6 py-2 text-white font-sans text-base
      border bg-red-500/20 hover:bg-red-500/30 border border-red-400/30
      backdrop-blur-md shadow-md
      hover:bg-white/20 transition-colors duration-200
    "
  >
    Cancel
  </button>
  </div>
        </div>
      )}
    </div>
  );
}

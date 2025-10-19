'use client';
import React, { useRef, useState, useEffect } from "react";

interface ImageUploadProps {
  className?: string;
}

export default function ImageUpload({ className }: ImageUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Trigger hidden file input
  const handleChooseFile = () => {
    fileInputRef.current?.click();
  };

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

    return () => URL.revokeObjectURL(url); // Cleanup
  }, [file]);

  // Confirm upload
  const handleConfirm = () => {
    if (!file) return;
    console.log("Uploading file:", file);
    alert(`Uploading ${file.name}`);
    // TODO: replace with backend upload
    setFile(null);
  };

  // Cancel upload
  const handleCancel = () => {
    setFile(null);
  };

  return (
    <div className={`flex flex-col items-center gap-4 mt-6 p-2 bg-slate-900 rounded-xl shadow-lg ${className}`}>
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
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md transition-colors font-medium"
        >
          Upload Image
        </button>
      ) : (
        <div className="flex flex-col items-center gap-4">
          {/* Thumbnail preview */}
          {previewUrl && (
            <img
              src={previewUrl}
              alt="Preview"
              className="w-48 h-auto rounded-md border border-gray-400"
            />
          )}

          {/* File name */}
          <p className="text-gray-200 text-sm">Selected file: {file.name}</p>

          {/* Confirm / Cancel buttons */}
          <div className="flex gap-4">
            <button
              onClick={handleConfirm}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-md transition-colors font-medium"
            >
              Upload
            </button>
            <button
              onClick={handleCancel}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-md transition-colors font-medium"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

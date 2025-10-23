
'use client';
import React, { useRef, useState, useEffect } from "react";
import myData from "../../Backend/bookshelf_response.json";
import { Camera, RefreshCw } from "lucide-react"; // Added RefreshCw for loading spinner

// Define the book data structure so this component knows what to expect
interface BookData {
  title?: string;
  rating?: number;
  author?: string;
  description?: string;
  thumbnail?: string;
}

interface ImageUploadProps {
  className?: string;
  // This is the key change: a function passed from the parent
  onUploadSuccess: (books: BookData[]) => void;
  isLive?: boolean;
}

export default function ImageUpload({ className, onUploadSuccess, isLive=false }: ImageUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  // Add loading and error states for better UX
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleChooseFile = () => fileInputRef.current?.click();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
    setError(null); // Clear previous errors
  };

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const handleConfirm = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const data = myData;
      if (isLive){
        const response = await fetch('http://127.0.0.1:5000/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          // Handle server errors (like 500, 404 etc.)
          throw new Error(`Upload failed with status: ${response.status}`);
        }

        const data = await response.json();
      }
      console.log('Upload response:', data);

      // APPLY FIX HERE 
      if (onUploadSuccess) {
        onUploadSuccess(data.books || []);
      }

      setFile(null); // Clear the file after successful upload
    } catch (e: any) {
      console.error("Upload failed:", e);
      setError(e.message || "An unknown error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFile(null);
    setError(null);
  }

  return (
    <div className={`flex flex-col items-center justify-center gap-4 mt-6 p-[10px] border border-white/20 backdrop-blur-md shadow-md bg-white/10 text-white transition-all duration-300 ease-in-out ${file ? "rounded-2xl py-6 px-8" : "rounded-full px-4 py-3"} ${className || ""}`}>
      <input type="file" accept="image/*" ref={fileInputRef} className="hidden" onChange={handleFileChange} />

      {!file ? (
        <button onClick={handleChooseFile} className="flex items-center gap-2 relative rounded-full px-6 py-2 text-white font-sans text-base bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/30 backdrop-blur-md shadow-md transition-colors duration-200">
          <Camera size={22} strokeWidth={1.25} className="text-white/70" />
          Upload Image
        </button>
      ) : (
        <div className="flex flex-col items-center gap-4">
          {previewUrl && <img src={previewUrl} alt="Preview" className="w-48 h-auto rounded-xl border border-white/20 object-cover" />}
          <p className="text-gray-200 text-sm text-center break-words max-w-[12rem]">{file.name}</p>

          <div className="flex gap-4">
            <button onClick={handleConfirm} disabled={isLoading} className="flex items-center justify-center rounded-full px-6 py-2 text-white font-sans text-base bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/30 backdrop-blur-md shadow-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              {isLoading ? (
                <>
                  <RefreshCw className="animate-spin mr-2" size={18} />
                  Uploading...
                </>
              ) : (
                "Confirm Upload"
              )}
            </button>
            <button onClick={handleCancel} disabled={isLoading} className="rounded-full px-6 py-2 text-white font-sans text-base bg-red-500/20 hover:bg-red-500/30 border border-red-400/30 backdrop-blur-md shadow-md transition-colors duration-200 disabled:opacity-50">
              Cancel
            </button>
          </div>
          {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
        </div>
      )}
    </div>
  );
}



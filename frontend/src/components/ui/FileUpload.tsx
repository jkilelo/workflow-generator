import React, { useRef } from 'react';

interface FileUploadProps {
  onFileSelect: (file: File) -> void;
  accept?: string;
  required?: boolean;
  label?: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  accept = "*/*",
  required = false,
  label = "Choose File"
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };
  
  return (
    <div className="mb-4">
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        required={required}
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        type="button"
        onClick={() => fileInputRef.current?.click()}
        className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {label}
      </button>
    </div>
  );
};
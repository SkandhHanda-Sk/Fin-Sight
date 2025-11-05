// src/components/UploadSection.jsx
import React, { useRef } from 'react';

function UploadSection({ onFileSelected }) {
  const fileInputRef = useRef(null); // Create a ref to access the file input

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.style.background = 'linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(59, 130, 214, 0.2) 100%)';
  };

  const handleDragLeave = (e) => {
    e.currentTarget.style.background = 'var(--neutral-50)';
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.style.background = 'var(--neutral-50)';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileSelected(files[0]); // Pass the file up to the parent component
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files.length > 0) {
      onFileSelected(e.target.files[0]); // Pass the file up to the parent component
    }
  };

  // Function to programmatically click the hidden file input
  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <section className="upload-section">
      <div
        className="upload-area"
        onClick={triggerFileInput} // Trigger file input on click
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <h3>📤 Upload Your Income Statement</h3>
        <p>Drag and drop or click to select your file</p>
        <div className="file-formats">
          <span className="format-badge">PDF</span>
          <span className="format-badge">CSV</span>
          <span className="format-badge">Excel</span>
          <span className="format-badge">Image</span>
        </div>
        <input
          type="file"
          id="fileInput" // Keep ID for potential direct access, though ref is preferred in React
          ref={fileInputRef} // Attach the ref
          accept=".pdf,.csv,.xlsx,.xls,.jpg,.png"
          onChange={handleFileInputChange}
          style={{ display: 'none' }} // Hide the input
        />
      </div>
    </section>
  );
}

export default UploadSection;
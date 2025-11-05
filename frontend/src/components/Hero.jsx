// src/components/Hero.jsx
import React from 'react';

function Hero({ onUploadClick }) { // Receive onUploadClick as a prop
  return (
    <section className="hero">
      <h1>AI-Powered Financial Analysis</h1>
      <p>Upload your income statements and get instant financial insights. Analyze profitability, stability, and efficiency with our intelligent AI engine.</p>
      <div className="hero-buttons">
        {/* Call the passed-in function */}
        <button className="btn-primary" onClick={onUploadClick}>Upload Document</button>
        <button className="btn-secondary">View Demo</button>
      </div>
    </section>
  );
}

export default Hero;
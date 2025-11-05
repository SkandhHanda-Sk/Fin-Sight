// src/App.jsx
import React, { useRef, useState, useEffect } from 'react';
import './App.css';

// Import all your components
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import UploadSection from './components/UploadSection';
import ChartComponent from './components/chart';
import ProcessingSection from './components/ProcessingSection';
import RatiosSection from './components/RatiosSection';
import InsightsSection from './components/InsightsSection';
import Footer from './components/Footer';
import SplashScreen from './components/SplashScreen';

function App() {
  const uploadSectionRef = useRef(null);
  const [showSplash, setShowSplash] = useState(true);
  const [isFading, setIsFading] = useState(false);
  const [showContent, setShowContent] = useState(false);

  // --- NEW STATE FOR API DATA ---
  const [financialData, setFinancialData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  // -----------------------------

  useEffect(() => {
    if (!showSplash) {
      const timer = setTimeout(() => setShowContent(true), 50);
      return () => clearTimeout(timer);
    }
  }, [showSplash]);

  // --- UPDATED FILE HANDLING LOGIC ---
  const handleFileSelected = async (file) => {
    console.log('File selected:', file.name);
    setIsLoading(true);
    setError(null);
    setFinancialData(null); // Clear previous data

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Make the API call to your backend
      const response = await fetch('http://localhost:5001/api/process-document', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setFinancialData(data); // Store the entire JSON response in state
      console.log('API Response:', data);

    } catch (e) {
      console.error('Error uploading or processing file:', e);
      setError('Failed to process the document. Please try again.');
    } finally {
      setIsLoading(false); // Stop loading indicator
    }
  };
  // ------------------------------------

  const smoothScrollTo = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSplashFinish = () => {
    setIsFading(true);
    setTimeout(() => setShowSplash(false), 500);
  };

  return (
    <>
      {showSplash ? (
        <div style={{ opacity: isFading ? 0 : 1, transition: 'opacity 0.5s ease-out' }}>
          <SplashScreen onFinish={handleSplashFinish} />
        </div>
      ) : (
        <div style={{ opacity: showContent ? 1 : 0, transition: 'opacity 0.8s ease-in' }}>
          <Navbar />
          <main>
            <Hero onUploadClick={() => smoothScrollTo('upload-section-id')} />

            <section id="upload-section-id" ref={uploadSectionRef} className="dashboard-layout">
              <UploadSection onFileSelected={handleFileSelected} />
              {/* Pass raw data to chart, only if it exists */}
              <ChartComponent chartData={financialData ? financialData.raw_parsed_data : null} />
            </section>

            {/* --- DYNAMICALLY RENDER SECTIONS BASED ON API RESPONSE --- */}
            {isLoading && <ProcessingSection />}
            
            {error && <div className="error-message">{error}</div>}

            {financialData && (
              <>
                {/* Pass the ratios array as a prop */}
                <RatiosSection ratios={financialData.profitability_ratios} />
                {/* Pass the AI analysis object as a prop */}
                <InsightsSection analysis={financialData.ai_analysis} />
              </>
            )}
            {/* -------------------------------------------------------- */}
          </main>
          <Footer />
        </div>
      )}
    </>
  );
}

export default App;
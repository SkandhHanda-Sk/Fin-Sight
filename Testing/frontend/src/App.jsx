// src/App.jsx
import React, { useRef, useState, useEffect } from 'react';
import './App.css'; // Your main CSS file

// Import all your components
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import UploadSection from './components/UploadSection';
import ChartComponent from './components/chart'; // Import the chart
import ProcessingSection from './components/ProcessingSection';
import RatiosSection from './components/RatiosSection';
import InsightsSection from './components/InsightsSection';
import Footer from './components/Footer';
import SplashScreen from './components/SplashScreen'; // <--- NEW IMPORT


function App() {
  // We need a ref to trigger the file input from the Hero section button
  const uploadSectionRef = useRef(null);
  const [showSplash, setShowSplash] = useState(true); // <--- NEW STATE
  const [isFading, setIsFading] = useState(false); // State to control the fade-out
  const [showContent, setShowContent] = useState(false); // State to control content fade-in

  // Effect to trigger the content fade-in after the splash screen is hidden
  useEffect(() => {
    if (!showSplash) {
      // A small delay ensures the content is in the DOM before we start the transition.
      const timer = setTimeout(() => {
        setShowContent(true);
      }, 50); // 50ms is enough
      return () => clearTimeout(timer);
    }
  }, [showSplash]);

  const handleUploadClick = () => {
    // Scroll to the upload section smoothly
    if (uploadSectionRef.current) {
      uploadSectionRef.current.scrollIntoView({ behavior: 'smooth' });
      // Optionally, you might want to directly trigger the file input within UploadSection
      // For now, let's just scroll there. The UploadSection itself handles its own file input trigger.
    }
  };

  const handleFileSelected = (file) => {
    console.log('File uploaded in App.jsx:', file.name);
    alert('File received: ' + file.name + '\n\nIn production, this would be sent to your backend for analysis.');
    // Here you would typically handle the file, e.g., send it to an API
    // setUploadedFile(file); // If you wanted to store the file in state
  };

  // Function for smooth scrolling to anchor links
  const smoothScrollTo = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSplashFinish = () => {
    setIsFading(true); // Start the fade-out animation
    // Wait for the animation to finish before unmounting the component
    setTimeout(() => {
      setShowSplash(false);
    }, 500); // This duration must match the transition duration in SplashScreen's CSS
  };

  return (
    <>
      {showSplash ? ( // <--- CONDITIONAL RENDERING
        // Add a style to control opacity for the fade-out effect
        <div style={{ opacity: isFading ? 0 : 1, transition: 'opacity 0.5s ease-out' }}>
          <SplashScreen onFinish={handleSplashFinish} />
        </div>
      ) : (
      // This div will handle the fade-in effect for the main content
      <div style={{ opacity: showContent ? 1 : 0, transition: 'opacity 0.8s ease-in' }}>
        <> 
          <Navbar /> 

          <main>
            {/* Pass the handleUploadClick function as a prop */}
            <Hero onUploadClick={() => smoothScrollTo('upload-section-id')} />

            {/* New layout for Upload and Chart */}
            <section id="upload-section-id" ref={uploadSectionRef} className="dashboard-layout">
              {/* The upload section is now the left column */}
              <UploadSection onFileSelected={handleFileSelected} />
              {/* The chart is the right column */}
              <ChartComponent />
            </section>

            <ProcessingSection />
            <RatiosSection />
            <InsightsSection />
          </main>

          <Footer />
        </>
      </div>
      )}
    </>
  );
}

export default App;
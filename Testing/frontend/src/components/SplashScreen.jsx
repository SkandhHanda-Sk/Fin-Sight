// src/components/SplashScreen.jsx
import React, { useState, useEffect } from 'react';

function SplashScreen({ onFinish }) {
  // State to control the 'growth' of our simulated graph bars
  const [progress, setProgress] = useState(0);

  // Use useEffect to simulate the graph growing over time
  useEffect(() => {
    // Simulate graph loading over 3 seconds
    const interval = setInterval(() => {
      setProgress(prevProgress => {
        const newProgress = prevProgress + 10; // Increase progress
        if (newProgress >= 100) {
          clearInterval(interval);
          // Call onFinish when animation is complete
          setTimeout(onFinish, 500); // Give a little extra time before fading out/unmounting
          return 100;
        }
        return newProgress;
      });
    }, 300); // Update every 300ms

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, [onFinish]); // Dependency array includes onFinish to prevent lint warnings, though it's stable

  return (
    <div style={splashScreenStyles.container}>
      <h1 style={splashScreenStyles.title}>Finsight</h1>
      <p style={splashScreenStyles.subtitle}>AI-Powered Market Analysis</p>

      <div style={splashScreenStyles.graphContainer}>
        {/* Simulated Graph Bars */}
        <div style={{ ...splashScreenStyles.bar, ...splashScreenStyles.bar1, height: `${progress * 0.8}%` }}></div>
        <div style={{ ...splashScreenStyles.bar, ...splashScreenStyles.bar2, height: `${progress * 1.0}%` }}></div>
        <div style={{ ...splashScreenStyles.bar, ...splashScreenStyles.bar3, height: `${progress * 0.7}%` }}></div>
        <div style={{ ...splashScreenStyles.bar, ...splashScreenStyles.bar4, height: `${progress * 0.9}%` }}></div>
        <div style={{ ...splashScreenStyles.bar, ...splashScreenStyles.bar5, height: `${progress * 0.6}%` }}></div>
        <div style={{ ...splashScreenStyles.bar, ...splashScreenStyles.bar5, height: `${progress * 0.8}%` }}></div>
      </div>

      <p style={splashScreenStyles.loadingText}>Analyzing market data... {progress}%</p>
    </div>
  );
}

// Inline styles for simplicity. You could move these to App.css or a dedicated CSS file.
const splashScreenStyles = {
  container: {
    position: 'fixed', // Covers the entire viewport
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    background: 'linear-gradient(135deg, #0F172A 0%, #1a1f3a 100%)', // Your primary gradient
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'white',
    zIndex: 9999, // Ensure it's on top of everything
    transition: 'opacity 0.5s ease-out', // For fading out
  },
  title: {
    fontSize: '3.5rem',
    fontWeight: '800',
    color: 'white',
    marginBottom: '1rem',
  },
  subtitle: {
    fontSize: '1.5rem',
    color: '#D1D5DB', // neutral-300
    marginBottom: '2rem',
  },
  graphContainer: {
    display: 'flex',
    alignItems: 'flex-end',
    gap: '10px',
    height: '150px', // Fixed height for the graph area
    width: '300px',
    marginBottom: '2rem',
    borderBottom: '2px solid rgba(255,255,255,0.3)',
    paddingBottom: '5px',
  },
  bar: {
    width: '40px',
    backgroundColor: '#06B6D4', // Your accent color
    borderRadius: '5px 5px 0 0',
    transition: 'height 0.3s ease-out', // Smooth growth animation for bars
  },
  bar1: { backgroundColor: '#3B82D6' }, // accent-light
  bar2: { backgroundColor: '#06B6D4' }, // accent
  bar3: { backgroundColor: '#3B82D6' },
  bar4: { backgroundColor: '#06B6D4' },
  bar5: { backgroundColor: '#3B82D6' },
  bar6: { backgroundColor: '#6fc6f2ff' },
  loadingText: {
    fontSize: '1.2rem',
    color: '#F3F4F6', // neutral-100
  },
};

export default SplashScreen;
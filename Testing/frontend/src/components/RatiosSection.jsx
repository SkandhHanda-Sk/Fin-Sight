// src/components/RatiosSection.jsx
import React from 'react';

// A helper function to determine the status class based on insight text
const getStatusClass = (insight) => {
  if (!insight) return 'status-neutral';
  const lowerInsight = insight.toLowerCase();
  if (lowerInsight.includes('healthy') || lowerInsight.includes('strong') || lowerInsight.includes('good')) {
    return 'status-good';
  }
  if (lowerInsight.includes('weak') || lowerInsight.includes('poor') || lowerInsight.includes('concern')) {
    return 'status-bad';
  }
  return 'status-neutral';
};

// The component now accepts 'ratios' as a prop
function RatiosSection({ ratios }) {
  // If no ratios are provided, don't render anything or show a message
  if (!ratios || ratios.length === 0) {
    return null; // Or a placeholder: <section><h2>Financial Ratios will appear here.</h2></section>
  }

  return (
    <section className="ratios-section" id="features">
      <h2 className="section-title">Financial Ratios Analysis</h2>
      <div className="ratios-grid">
        {/* Map over the 'ratios' prop instead of the hardcoded array */}
        {ratios.map((ratio, index) => (
          <div className="ratio-card" key={index}>
            {/* You might need to add a 'category' to your backend response, or remove this div */}
            <div className="ratio-category">{ratio.category || 'Ratio'}</div>
            <div className="ratio-name">{ratio.metric}</div>
            <div className="ratio-value">{ratio.value}</div>
            <div className="ratio-status">
              <span className={`status-dot ${getStatusClass(ratio.insight)}`}></span>
              <span>{ratio.insight}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default RatiosSection;
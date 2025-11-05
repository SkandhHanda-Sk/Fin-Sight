// src/components/InsightsSection.jsx
import React from 'react';

// The component now accepts 'analysis' as a prop
function InsightsSection({ analysis }) {
  // If no analysis data is provided, render nothing
  if (!analysis) {
    return null;
  }

  // Destructure the properties from the analysis object for easier access
  const { strengths, weaknesses, recommendations } = analysis;

  return (
    <section className="insights-section">
      <h2 className="section-title">AI Analysis Report</h2>
      <div className="insights-grid">
        {/* Strengths - check if the array exists and is not empty */}
        {strengths && strengths.length > 0 && (
          <div className="insight-card">
            <h4>💪 Strengths</h4>
            {strengths.map((item, index) => (
              <div className="insight-item" key={index}>
                <div className="insight-title">{item.title}</div>
                <div className="insight-desc">{item.description}</div>
              </div>
            ))}
          </div>
        )}

        {/* Weaknesses */}
        {weaknesses && weaknesses.length > 0 && (
          <div className="insight-card">
            <h4>⚠️ Weaknesses</h4>
            {weaknesses.map((item, index) => (
              <div className="insight-item" key={index}>
                <div className="insight-title">{item.title}</div>
                <div className="insight-desc">{item.description}</div>
              </div>
            ))}
          </div>
        )}

        {/* Recommendations */}
        {recommendations && recommendations.length > 0 && (
          <div className="insight-card">
            <h4>💡 Recommendations</h4>
            {recommendations.map((item, index) => (
              <div className="insight-item" key={index}>
                <div className="insight-title">{item.title}</div>
                <div className="insight-desc">{item.description}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

export default InsightsSection;
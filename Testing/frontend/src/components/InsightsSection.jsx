// src/components/InsightsSection.jsx
import React from 'react';

function InsightsSection() {
  const insights = {
    strengths: [
      { title: 'Strong Profitability', description: 'Net margins of 18.5% indicate healthy profit generation above industry average.' },
      { title: 'Good Liquidity Position', description: 'Current ratio of 1.8 shows strong ability to meet short-term obligations.' },
      { title: 'Manageable Debt', description: 'D/E ratio of 0.65 indicates conservative leverage and financial stability.' },
    ],
    weaknesses: [
      { title: 'Asset Turnover', description: 'Lower asset utilization suggests opportunity to optimize operational efficiency.' },
      { title: 'Operating Expenses', description: 'Operating costs are 35% of revenue, indicating room for cost optimization.' },
      { title: 'ROE Potential', description: 'Return on equity at 12.3% could be improved with better capital allocation.' },
    ],
    recommendations: [
      { title: 'Cost Optimization', description: 'Review operating expenses to match industry benchmarks and improve margins.' },
      { title: 'Asset Efficiency', description: 'Implement measures to increase asset turnover and operational capacity utilization.' },
      { title: 'Strategic Growth', description: 'Strong financial position allows for strategic investments in growth initiatives.' },
    ],
  };

  return (
    <section className="insights-section">
      <h2 className="section-title">AI Analysis Report</h2>
      <div className="insights-grid">
        {/* Strengths */}
        <div className="insight-card">
          <h4>💪 Strengths</h4>
          {insights.strengths.map((item, index) => (
            <div className="insight-item" key={index}>
              <div className="insight-title">{item.title}</div>
              <div className="insight-desc">{item.description}</div>
            </div>
          ))}
        </div>

        {/* Weaknesses */}
        <div className="insight-card">
          <h4>⚠️ Weaknesses</h4>
          {insights.weaknesses.map((item, index) => (
            <div className="insight-item" key={index}>
              <div className="insight-title">{item.title}</div>
              <div className="insight-desc">{item.description}</div>
            </div>
          ))}
        </div>

        {/* Recommendations */}
        <div className="insight-card">
          <h4>💡 Recommendations</h4>
          {insights.recommendations.map((item, index) => (
            <div className="insight-item" key={index}>
              <div className="insight-title">{item.title}</div>
              <div className="insight-desc">{item.description}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default InsightsSection;
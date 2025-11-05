// src/components/RatiosSection.jsx
import React from 'react';

function RatiosSection() {
  const ratioCards = [
    { category: 'Profitability', name: 'Net Profit Margin', value: '18.5%', status: 'Healthy', statusClass: 'status-good' },
    { category: 'Profitability', name: 'Gross Margin', value: '42.3%', status: 'Good', statusClass: 'status-good' },
    { category: 'Stability', name: 'Debt-to-Equity', value: '0.65', status: 'Manageable', statusClass: 'status-good' },
    { category: 'Stability', name: 'Interest Coverage', value: '5.2x', status: 'Strong', statusClass: 'status-good' },
    { category: 'Liquidity', name: 'Current Ratio', value: '1.8', status: 'Healthy', statusClass: 'status-good' },
    { category: 'Liquidity', name: 'Quick Ratio', value: '1.2', status: 'Good', statusClass: 'status-good' },
  ];

  return (
    <section className="ratios-section" id="features">
      <h2 className="section-title">Financial Ratios Analysis</h2>
      <div className="ratios-grid">
        {ratioCards.map((ratio, index) => (
          <div className="ratio-card" key={index}>
            <div className="ratio-category">{ratio.category}</div>
            <div className="ratio-name">{ratio.name}</div>
            <div className="ratio-value">{ratio.value}</div>
            <div className="ratio-status">
              <span className={`status-dot ${ratio.statusClass}`}></span>
              <span>{ratio.status}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default RatiosSection;
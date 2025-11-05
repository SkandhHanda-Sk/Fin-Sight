// src/components/ProcessingSection.jsx
import React from 'react';

function ProcessingSection() {
  const workflowSteps = [
    { number: 1, title: 'File Detection', description: 'Automatically detect file type and validate format' },
    { number: 2, title: 'Data Extraction', description: 'Extract financial data using OCR and parsing' },
    { number: 3, title: 'Analysis', description: 'Calculate 12+ financial ratios automatically' },
    { number: 4, title: 'AI Insights', description: 'Get AI-powered strengths and weakness analysis' },
  ];

  return (
    <section className="processing-section" id="how-it-works">
      <h2 className="section-title">How Finsight Works</h2>
      <div className="workflow-steps">
        {workflowSteps.map((step, index) => (
          <div className="step" key={step.number}>
            <div className="step-number">{step.number}</div>
            <h4>{step.title}</h4>
            <p>{step.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ProcessingSection;
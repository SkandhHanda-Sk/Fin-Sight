// src/components/Navbar.jsx
import React from 'react';

function Navbar() {
  const smoothScrollTo = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav>
      <a href="#" className="logo" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>Fin<span>sight</span></a>
      <ul className="nav-links">
        <li><a href="#features" onClick={(e) => { e.preventDefault(); smoothScrollTo('features'); }}>Features</a></li>
        <li><a href="#how-it-works" onClick={(e) => { e.preventDefault(); smoothScrollTo('how-it-works'); }}>How It Works</a></li>
        {/* No #pricing section in your current HTML, keeping for example */}
        <li><a href="#pricing" onClick={(e) => { e.preventDefault(); smoothScrollTo('features'); }}>Pricing</a></li>
      </ul>
      <button className="nav-btn" onClick={(e) => { e.preventDefault(); smoothScrollTo('upload-section-id'); }}>Get Started</button>
    </nav>
  );
}

export default Navbar;
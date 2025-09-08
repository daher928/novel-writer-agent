import React, { useState } from 'react';
import './Navigation.css';

const Navigation = ({ activeView, onViewChange }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleNavClick = (view) => {
    onViewChange(view);
    setIsMobileMenuOpen(false); // Close mobile menu when item is selected
  };

  const navItems = [
    { key: 'home', label: 'Home' },
    { key: 'history', label: 'History' }
  ];

  return (
    <nav className="navigation">
      <div className="nav-container">
        {/* Mobile menu button */}
        <button 
          className="mobile-menu-toggle"
          onClick={toggleMobileMenu}
          aria-label="Toggle navigation menu"
        >
          <span className={`hamburger ${isMobileMenuOpen ? 'open' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        {/* Navigation menu */}
        <ul className={`nav-menu ${isMobileMenuOpen ? 'mobile-open' : ''}`}>
          {navItems.map((item) => (
            <li key={item.key} className="nav-item">
              <button
                className={`nav-link ${activeView === item.key ? 'active' : ''}`}
                onClick={() => handleNavClick(item.key)}
                aria-current={activeView === item.key ? 'page' : undefined}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import Home from './components/Home';
import History from './components/History';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="app-title">
            <h1>Novel Writer Agent</h1>
            <p>AI-Powered Daily Novel Writing</p>
          </div>
        </header>
        
        <Navigation />
        
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Navigate to="/" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/history" element={<History />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        
        <footer className="app-footer">
          <p>© 2025 Novel Writer Agent. Built with React & Vite.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;

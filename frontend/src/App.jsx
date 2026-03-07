// frontend/src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Home from './components/Home';
import ResumeUpload from './components/ResumeUpload';
import SkillRecommendations from './components/SkillRecommendations';
import JobListings from './components/JobListings';
import Footer from './components/Footer';
import { JobProvider } from './context/JobContext';

function App() {
  return (
    <JobProvider>
      <Router>
        <div className="app">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/upload" element={<ResumeUpload />} />
              <Route path="/recommendations" element={<SkillRecommendations />} />
              <Route path="/jobs" element={<JobListings />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </JobProvider>
  );
}

export default App;
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="fade-in">
      <div className="card" style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem', color: '#333' }}>
          AI-Powered Skill Recommendation
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '2rem' }}>
          Upload your resume and let our AI analyze your skills to find the perfect job matches
        </p>
        <Link to="/upload">
          <button className="btn btn-primary" style={{ fontSize: '1.2rem', padding: '1rem 3rem' }}>
            Get Started
          </button>
        </Link>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
        <div className="card">
          <h2 style={{ color: '#667eea', marginBottom: '1rem' }}>📄 Smart Resume Parsing</h2>
          <p style={{ color: '#666', lineHeight: '1.6' }}>
            Our AI automatically extracts your skills, experience, and education from your resume with high accuracy
          </p>
        </div>

        <div className="card">
          <h2 style={{ color: '#667eea', marginBottom: '1rem' }}>🎯 Intelligent Matching</h2>
          <p style={{ color: '#666', lineHeight: '1.6' }}>
            Get personalized job recommendations based on your skills and experience using machine learning
          </p>
        </div>

        <div className="card">
          <h2 style={{ color: '#667eea', marginBottom: '1rem' }}>📊 Skill Gap Analysis</h2>
          <p style={{ color: '#666', lineHeight: '1.6' }}>
            Identify missing skills and get recommendations for courses to improve your employability
          </p>
        </div>
      </div>
    </div>
  );
}

export default Home;
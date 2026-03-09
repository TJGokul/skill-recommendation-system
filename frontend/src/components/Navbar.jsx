// frontend/src/components/Navbar.jsx

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthModal from './AuthModal';
import { useAuth } from '../context/AuthContext';
import { getCSRFToken } from '../utils/csrf';
import axios from 'axios';

function Navbar() {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    setShowAuthModal(false);
    navigate('/upload');
  };

  const handleUploadClick = (e) => {
    e.preventDefault();
    if (!user) {
      setShowAuthModal(true);
    } else {
      navigate('/upload');
    }
  };

  const handleLogout = async () => {
    try {
      const csrfToken = getCSRFToken();
      console.log('Logout CSRF Token:', csrfToken);
      
      await axios.post('http://localhost:8000/api/logout/', {}, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        }
      });
      
      logout();
      navigate('/');
    } catch (error) {
      console.error('Error logging out:', error.response?.data || error.message);
    }
  };

  return (
    <>
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            SkillMatch AI
          </Link>
          <div className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/upload" onClick={handleUploadClick}>Upload Resume</Link>
            <Link to="/recommendations">Recommendations</Link>
            <Link to="/jobs">Jobs</Link>
            
            {user ? (
              <div className="user-menu">
                <span className="user-name">Hi, {user.first_name || user.username}</span>
                <button className="btn btn-secondary" onClick={handleLogout}>
                  Sign Out
                </button>
              </div>
            ) : (
              <button 
                className="btn btn-primary" 
                onClick={() => setShowAuthModal(true)}
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </nav>

      <AuthModal 
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </>
  );
}

export default Navbar;
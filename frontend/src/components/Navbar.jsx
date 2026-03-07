import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthModal from './AuthModal';
import axios from 'axios';

// Helper function to get CSRF token
function getCSRFToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

function Navbar() {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    checkUserStatus();
  }, []);

  const checkUserStatus = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/user/', {
        withCredentials: true
      });
      if (response.data.user) {
        setUser(response.data.user);
      }
    } catch (error) {
      console.error('Error checking user status:', error);
    }
  };

  const handleLoginSuccess = (data) => {
    setUser(data.user);
  };

  const handleLogout = async () => {
    try {
      const csrfToken = getCSRFToken();
      
      await axios.post('http://localhost:8000/api/logout/', {}, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrfToken
        }
      });
      
      setUser(null);
      navigate('/'); // Redirect to home after logout
    } catch (error) {
      console.error('Error logging out:', error);
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
            <Link to="/upload">Upload Resume</Link>
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
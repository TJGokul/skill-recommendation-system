import React from 'react';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>SkillMatch AI</h3>
          <p style={{ color: '#cbd5e0', lineHeight: '1.6' }}>
            Empowering job seekers with AI-driven skill recommendations and career guidance.
          </p>
        </div>

        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/upload">Upload Resume</a></li>
            <li><a href="/recommendations">Recommendations</a></li>
            <li><a href="/jobs">Jobs</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Resources</h3>
          <ul>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Career Tips</a></li>
            <li><a href="#">Skill Development</a></li>
            <li><a href="#">FAQ</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Contact</h3>
          <ul>
            <li>📧 support@skillmatch.ai</li>
            <li>📞 +91 93845 19520</li>
            <li>📍 Paramakudi, Ramanthapuram</li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; 2024 SkillMatch AI. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
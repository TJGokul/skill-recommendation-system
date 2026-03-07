import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CourseRecommendations.css';

function CourseRecommendations({ skills, onClose }) {
  const [recommendations, setRecommendations] = useState([]);
  const [analysis, setAnalysis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRole, setSelectedRole] = useState('');

  useEffect(() => {
    if (skills && skills.length > 0) {
      fetchRecommendations();
      fetchSkillGapAnalysis();
    }
  }, [skills]);

  const fetchRecommendations = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/course-recommendations/', {
        skills: skills
      });
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const fetchSkillGapAnalysis = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/skill-gap-analysis/', {
        skills: skills
      });
      setAnalysis(response.data.analysis);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analysis:', error);
      setLoading(false);
    }
  };

  const getRecommendationsForRole = async (role) => {
    setSelectedRole(role);
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/course-recommendations/', {
        skills: skills,
        target_role: role.toLowerCase()
      });
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error fetching role recommendations:', error);
    }
    setLoading(false);
  };

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h2>Your Skill Analysis</h2>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>

      {loading ? (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Analyzing your skills...</p>
        </div>
      ) : (
        <>
          {/* Skill Gap Analysis */}
          <div className="analysis-section">
            <h3>Job Role Match Analysis</h3>
            <div className="analysis-grid">
              {analysis.map((item, index) => (
                <div key={index} className="analysis-card">
                  <div className="role-header">
                    <h4>{item.role}</h4>
                    <span className="match-percentage">{item.match_percentage}% Match</span>
                  </div>
                  <div className="progress-bar-container">
                    <div 
                      className="progress-bar" 
                      style={{ width: `${item.match_percentage}%` }}
                    ></div>
                  </div>
                  <div className="skills-section">
                    <div className="current-skills">
                      <p><strong>Your Skills:</strong></p>
                      <div className="skill-tags">
                        {item.current_skills.map((skill, i) => (
                          <span key={i} className="skill-tag success">{skill}</span>
                        ))}
                      </div>
                    </div>
                    {item.missing_skills.length > 0 && (
                      <div className="missing-skills">
                        <p><strong>Skills to Learn:</strong></p>
                        <div className="skill-tags">
                          {item.missing_skills.map((skill, i) => (
                            <span 
                              key={i} 
                              className="skill-tag warning"
                              onClick={() => getRecommendationsForRole(item.role)}
                            >
                              {skill} +
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  <button 
                    className="btn btn-secondary"
                    onClick={() => getRecommendationsForRole(item.role)}
                  >
                    Get Courses for {item.role}
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Course Recommendations */}
          {recommendations.length > 0 && (
            <div className="recommendations-section">
              <h3>
                {selectedRole 
                  ? `Recommended Courses for ${selectedRole}` 
                  : 'Recommended Courses for You'}
              </h3>
              <div className="courses-grid">
                {recommendations.map((course, index) => (
                  <div key={index} className="course-card">
                    <div className="course-header">
                      <h4>{course.name}</h4>
                      <span className="course-level">{course.level}</span>
                    </div>
                    <div className="course-details">
                      <p><strong>Platform:</strong> {course.platform}</p>
                      <p><strong>Duration:</strong> {course.duration}</p>
                    </div>
                    <a 
                      href={course.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="btn btn-primary"
                    >
                      View Course
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default CourseRecommendations;
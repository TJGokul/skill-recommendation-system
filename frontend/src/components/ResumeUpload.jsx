// frontend/src/components/ResumeUpload.jsx

import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useJobs } from '../context/JobContext';
import { useAuth } from '../context/AuthContext';
import JobMatches from './JobMatches';
import SkillGapAnalysis from './SkillGapAnalysis';
import AICareerAssistant from './AICareerAssistant';
import AuthModal from './AuthModal';

// Helper function to get CSRF token from cookies
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

function ResumeUpload() {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [parsedData, setParsedData] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('parsed');
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const { updateJobs, setLoading: setContextLoading, setError: setContextError, parsedResumeData } = useJobs();

  // Load previously parsed data from context
  useEffect(() => {
    if (parsedResumeData && !parsedData) {
      setParsedData(parsedResumeData);
      setUploadSuccess(true);
    }
  }, [parsedResumeData]);

  // Show auth modal if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      setShowAuthModal(true);
    }
  }, [user, authLoading]);

  const handleLoginSuccess = () => {
    setShowAuthModal(false);
  };

  const extractSkillsList = (data) => {
    if (!data) return [];
    
    if (data.skills) {
      if (Array.isArray(data.skills)) {
        return data.skills;
      }
      if (data.skills.flat_list && Array.isArray(data.skills.flat_list)) {
        return data.skills.flat_list;
      }
      if (data.skills.by_category) {
        const flatSkills = [];
        Object.values(data.skills.by_category).forEach(categorySkills => {
          if (Array.isArray(categorySkills)) {
            flatSkills.push(...categorySkills);
          }
        });
        return flatSkills;
      }
    }
    return [];
  };

  const fetchJobsAfterUpload = async (data) => {
    const skillsList = extractSkillsList(data);
    if (skillsList.length === 0) return;
    
    const csrfToken = getCSRFToken(); // ADDED: CSRF token for job fetch
    
    setContextLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/search-live-jobs/', {
        skills: skillsList.map(s => s.name || s).slice(0, 3)
      }, {
        withCredentials: true,
        headers: { // ADDED: Headers with CSRF token
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        }
      });
      
      if (response.data && response.data.jobs) {
        updateJobs(response.data.jobs, skillsList, data);
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
      setContextError(err.message);
    } finally {
      setContextLoading(false);
    }
  };

  const onDrop = useCallback(async (acceptedFiles) => {
    if (!user) {
      setShowAuthModal(true);
      return;
    }

    const file = acceptedFiles[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('resume', file);

    // Get CSRF token for file upload
    const csrfToken = getCSRFToken();
    console.log('CSRF Token for upload:', csrfToken);

    setUploading(true);
    setError(null);
    setUploadSuccess(false);
    setParsedData(null);

    try {
      console.log('Uploading file as user:', user.username);
      
      const response = await axios.post('http://localhost:8000/api/upload-resume/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        },
      });

      console.log('Upload response:', response.data);
      const newParsedData = response.data.parsed_data;
      setParsedData(newParsedData);
      setUploadSuccess(true);
      setActiveTab('parsed');
      setUploading(false);
      
      await fetchJobsAfterUpload(newParsedData);
      
    } catch (err) {
      console.error('Upload error:', err.response?.data || err.message);
      console.error('Status:', err.response?.status);
      
      if (err.response?.status === 401 || err.response?.status === 403) {
        setShowAuthModal(true);
        setError('Your session has expired. Please sign in again.');
      } else {
        setError(err.response?.data?.error || 'Upload failed. Please try again.');
      }
      setUploading(false);
      setUploadSuccess(false);
    }
  }, [user]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  });

  const getRawText = () => {
    if (!parsedData) return '';
    return parsedData.raw_text_preview || parsedData.raw_text || '';
  };

  const getExperienceYears = () => {
    if (!parsedData) return 0;
    return parsedData.experience_years || 0;
  };

  const skillsList = extractSkillsList(parsedData);
  const rawText = getRawText();
  const experienceYears = getExperienceYears();

  if (authLoading) {
    return (
      <div className="fade-in">
        <h1 style={{ color: 'white', marginBottom: '2rem' }}>Upload Your Resume</h1>
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fade-in">
      <h1 style={{ color: 'white', marginBottom: '2rem' }}>Upload Your Resume</h1>
      
      <div className="card">
        {user ? (
          <>
            <div style={{ 
              marginBottom: '1rem', 
              padding: '0.5rem',
              background: '#e8f5e9', 
              borderRadius: '8px',
              textAlign: 'center',
              color: '#2e7d32'
            }}>
              ✅ Logged in as: <strong>{user.username}</strong>
            </div>

            <div {...getRootProps()} className="upload-area">
              <input {...getInputProps()} />
              <i style={{ fontSize: '3rem' }}>📄</i>
              {isDragActive ? (
                <p>Drop your resume here...</p>
              ) : (
                <>
                  <p>Drag & drop your resume here, or click to select</p>
                  <p style={{ fontSize: '0.9rem', color: '#999', marginTop: '0.5rem' }}>
                    Supports PDF and DOCX files
                  </p>
                </>
              )}
            </div>

            {uploading && (
              <div style={{ marginTop: '2rem' }}>
                <p>Uploading... {uploadProgress}%</p>
                <div className="progress-container">
                  <div className="progress-bar" style={{ width: `${uploadProgress}%` }}></div>
                </div>
              </div>
            )}

            {error && (
              <div className="alert alert-error" style={{ marginTop: '1rem' }}>
                <strong>Error:</strong> {error}
              </div>
            )}

            {(uploadSuccess && parsedData) || parsedResumeData ? (
              <div style={{ marginTop: '2rem' }}>
                {/* Tab Navigation */}
                <div className="recommendation-tabs">
                  <button 
                    className={`tab-btn ${activeTab === 'parsed' ? 'active' : ''}`}
                    onClick={() => setActiveTab('parsed')}
                  >
                    📄 Parsed Info
                  </button>
                  <button 
                    className={`tab-btn ${activeTab === 'jobs' ? 'active' : ''}`}
                    onClick={() => setActiveTab('jobs')}
                  >
                    💼 Job Matches
                  </button>
                  <button 
                    className={`tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
                    onClick={() => setActiveTab('skills')}
                  >
                    📊 Skill Gap Analysis
                  </button>
                  <button 
                    className={`tab-btn ${activeTab === 'ai' ? 'active' : ''}`}
                    onClick={() => setActiveTab('ai')}
                  >
                    🤖 AI Assistant
                  </button>
                </div>

                {/* Tab Content */}
                <div className="tab-content">
                  {activeTab === 'parsed' && (
                    <div className="parsed-info">
                      <h2 style={{ color: '#333', marginBottom: '1rem' }}>Parsed Information</h2>
                      
                      {/* Personal Info */}
                      {parsedData?.personal_info && Object.keys(parsedData.personal_info).length > 0 && (
                        <div style={{ marginBottom: '1.5rem' }}>
                          <h3 style={{ color: '#667eea', marginBottom: '0.5rem' }}>Contact Info:</h3>
                          <div style={{ background: '#f8f9ff', padding: '1rem', borderRadius: '8px' }}>
                            {parsedData.personal_info.name && <p><strong>Name:</strong> {parsedData.personal_info.name}</p>}
                            {parsedData.personal_info.email && <p><strong>Email:</strong> {parsedData.personal_info.email}</p>}
                            {parsedData.personal_info.phone && <p><strong>Phone:</strong> {parsedData.personal_info.phone}</p>}
                          </div>
                        </div>
                      )}
                      
                      {/* Skills Section */}
                      <div style={{ marginBottom: '1.5rem' }}>
                        <h3 style={{ color: '#667eea', marginBottom: '0.5rem' }}>Skills Found:</h3>
                        <div className="skills-container">
                          {skillsList.length > 0 ? (
                            skillsList.map((skill, index) => (
                              <span key={index} className="skill-tag">
                                {typeof skill === 'string' ? skill : skill.name || 'Unknown'}
                                {skill.proficiency && ` (${skill.proficiency})`}
                              </span>
                            ))
                          ) : (
                            <p>No skills detected. Try uploading a more detailed resume.</p>
                          )}
                        </div>
                      </div>

                      {/* Experience */}
                      <div style={{ marginBottom: '1.5rem' }}>
                        <h3 style={{ color: '#667eea', marginBottom: '0.5rem' }}>Experience:</h3>
                        <p><strong>{experienceYears} years</strong> total experience</p>
                        
                        {parsedData?.experience && parsedData.experience.length > 0 && (
                          <div style={{ marginTop: '1rem' }}>
                            {parsedData.experience.slice(0, 2).map((exp, idx) => (
                              <div key={idx} style={{ 
                                background: '#f8f9ff', 
                                padding: '0.8rem', 
                                borderRadius: '8px',
                                marginBottom: '0.5rem'
                              }}>
                                <strong>{exp.title}</strong> at {exp.company}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Education */}
                      <div style={{ marginBottom: '1rem' }}>
                        <h3 style={{ color: '#667eea', marginBottom: '0.5rem' }}>Education:</h3>
                        <div className="skills-container">
                          {parsedData?.education && parsedData.education.length > 0 ? (
                            parsedData.education.map((edu, index) => (
                              <span key={index} className="skill-tag">
                                {edu.degree || edu}
                              </span>
                            ))
                          ) : (
                            <p>No education details detected</p>
                          )}
                        </div>
                      </div>

                      {/* Certifications */}
                      {parsedData?.certifications && parsedData.certifications.length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h3 style={{ color: '#667eea', marginBottom: '0.5rem' }}>Certifications:</h3>
                          <div className="skills-container">
                            {parsedData.certifications.map((cert, index) => (
                              <span key={index} className="skill-tag" style={{ background: '#ff9800' }}>
                                {cert}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {activeTab === 'jobs' && <JobMatches />}
                  {activeTab === 'skills' && (
                    <SkillGapAnalysis 
                      skills={skillsList}
                      experience={experienceYears}
                    />
                  )}
                  {activeTab === 'ai' && (
                    <AICareerAssistant 
                      skills={skillsList}
                      experience={experienceYears}
                    />
                  )}
                </div>
              </div>
            ) : (
              <div style={{ marginTop: '2rem', textAlign: 'center', color: '#666' }}>
                <p>Upload your resume to get personalized job recommendations and skill analysis</p>
              </div>
            )}
          </>
        ) : (
          <div className="auth-required-banner" style={{
            background: 'linear-gradient(135deg, #667eea, #764ba2)',
            padding: '3rem',
            borderRadius: '10px',
            textAlign: 'center',
            color: 'white'
          }}>
            <i style={{ fontSize: '4rem', marginBottom: '1rem' }}>🔒</i>
            <h2>Sign In Required</h2>
            <p style={{ margin: '1rem 0 2rem', fontSize: '1.1rem' }}>
              Please sign in to upload your resume and get personalized job recommendations.
            </p>
            <button 
              className="btn btn-primary" 
              onClick={() => setShowAuthModal(true)}
              style={{ background: 'white', color: '#667eea', padding: '0.8rem 2rem', fontSize: '1.1rem' }}
            >
              Sign In
            </button>
          </div>
        )}
      </div>

      {/* Auth Modal */}
      <AuthModal 
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
}

export default ResumeUpload;
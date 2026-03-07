// frontend/src/components/ResumeUpload.jsx

import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { useJobs } from '../context/JobContext';
import JobMatches from './JobMatches';
import SkillGapAnalysis from './SkillGapAnalysis';
import AICareerAssistant from './AICareerAssistant';

function ResumeUpload() {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [parsedData, setParsedData] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('parsed');
  const [uploadSuccess, setUploadSuccess] = useState(false);
  
  const { updateJobs, setLoading, setError: setContextError, parsedResumeData } = useJobs();

  // Load previously parsed data from context
  useEffect(() => {
    if (parsedResumeData && !parsedData) {
      setParsedData(parsedResumeData);
      setUploadSuccess(true);
    }
  }, [parsedResumeData]);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('resume', file);

    setUploading(true);
    setError(null);
    setUploadSuccess(false);
    setParsedData(null);

    try {
      const response = await axios.post('http://localhost:8000/api/upload-resume/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
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
      
      // Fetch jobs immediately after upload
      await fetchJobsAfterUpload(newParsedData);
      
    } catch (err) {
      console.error('Upload error:', err);
      console.error('Error response:', err.response?.data);
      const errorMsg = err.response?.data?.error || 'Error uploading resume. Please try again.';
      setError(errorMsg);
      setUploading(false);
      setUploadSuccess(false);
    }
  }, []);

  const fetchJobsAfterUpload = async (data) => {
    const skillsList = extractSkillsList(data);
    if (skillsList.length === 0) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/search-live-jobs/', {
        skills: skillsList.map(s => s.name || s).slice(0, 3)
      });
      
      if (response.data && response.data.jobs) {
        // Save jobs to global context
        updateJobs(response.data.jobs, skillsList, data);
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
      setContextError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  });

  // Helper function to extract skills in various formats
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

  return (
    <div className="fade-in">
      <h1 style={{ color: 'white', marginBottom: '2rem' }}>Upload Your Resume</h1>
      
      <div className="card">
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

              {activeTab === 'jobs' && (
                <JobMatches />
              )}

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
          !uploading && !uploadSuccess && !error && (
            <div style={{ marginTop: '2rem', textAlign: 'center', color: '#666' }}>
              <p>Upload your resume to get personalized job recommendations and skill analysis</p>
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default ResumeUpload;
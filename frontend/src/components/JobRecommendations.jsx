import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './JobRecommendations.css';

function JobRecommendations({ jobSeekerId, skills, experience }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetchJobs();
    if (jobSeekerId) {
      fetchRecommendations();
    }
  }, [jobSeekerId]);

  const fetchJobs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/jobs/');
      setJobs(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching jobs:', error);
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/recommendations/${jobSeekerId}/`);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const calculateMatchScore = (job) => {
    if (!skills || skills.length === 0) return 0;
    
    const jobSkills = job.skills_required || [];
    const userSkills = skills.map(s => s.name.toLowerCase());
    
    if (jobSkills.length === 0) return 50;
    
    const matchedSkills = jobSkills.filter(skill => 
      userSkills.includes(skill.name.toLowerCase())
    );
    
    return Math.round((matchedSkills.length / jobSkills.length) * 100);
  };

  if (loading) {
    return <div className="loading-spinner">Loading jobs...</div>;
  }

  return (
    <div className="job-recommendations">
      <h2>Recommended Jobs for You</h2>
      
      <div className="jobs-grid">
        {jobs.length > 0 ? (
          jobs.map((job) => {
            const matchScore = calculateMatchScore(job);
            return (
              <div key={job.id} className="job-card">
                <div className="match-score-badge" style={{
                  background: matchScore > 70 ? '#4caf50' : matchScore > 40 ? '#ff9800' : '#f44336'
                }}>
                  {matchScore}% Match
                </div>
                <h3>{job.title}</h3>
                <p className="company">{job.company}</p>
                <p className="location">📍 {job.location}</p>
                <p className="description">{job.description?.substring(0, 100)}...</p>
                
                <div className="job-skills">
                  {job.skills_required?.slice(0, 3).map((skill, i) => (
                    <span key={i} className="skill-badge">{skill.name}</span>
                  ))}
                  {job.skills_required?.length > 3 && (
                    <span className="skill-badge more">+{job.skills_required.length - 3}</span>
                  )}
                </div>
                
                <button className="btn btn-primary">Apply Now</button>
              </div>
            );
          })
        ) : (
          <p>No jobs available at the moment.</p>
        )}
      </div>
    </div>
  );
}

export default JobRecommendations;
// frontend/src/components/JobListings.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './JobListings.css';

function JobListings() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [userSkills, setUserSkills] = useState([]);

  useEffect(() => {
    fetchUserSkills();
    fetchJobs();
  }, []);

  const fetchUserSkills = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/latest-resume/', {
        withCredentials: true
      });
      if (response.data && response.data.skills) {
        const skills = response.data.skills.flat_list || response.data.skills || [];
        setUserSkills(skills.map(s => s.name || s));
      }
    } catch (error) {
      console.error('Error fetching skills:', error);
    }
  };

  const fetchJobs = async () => {
    setLoading(true);
    try {
      // Try to get live jobs first
      const response = await axios.post('http://localhost:8000/api/search-live-jobs/', {
        skills: userSkills.length > 0 ? userSkills : ['developer']
      });
      
      if (response.data && response.data.jobs && response.data.jobs.length > 0) {
        setJobs(response.data.jobs);
      } else {
        // Fallback to mock jobs
        setJobs(getMockJobs());
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
      setJobs(getMockJobs());
    } finally {
      setLoading(false);
    }
  };

  const getMockJobs = () => {
    return [
      {
        id: 1,
        title: 'Frontend Developer',
        company: 'Tech Solutions Inc',
        description: 'Looking for a React developer with 2+ years experience...',
        location: 'Bangalore, India',
        salary: '₹8L - ₹12L',
        employment_type: 'full-time',
        skills_required: ['React', 'JavaScript', 'CSS']
      },
      {
        id: 2,
        title: 'Backend Engineer',
        company: 'Innovation Labs',
        description: 'Python/Django developer needed for core product team...',
        location: 'Remote',
        salary: '₹10L - ₹15L',
        employment_type: 'full-time',
        skills_required: ['Python', 'Django', 'PostgreSQL']
      },
      {
        id: 3,
        title: 'Full Stack Developer',
        company: 'Startup India',
        description: 'Join our fast-growing startup as a full stack developer...',
        location: 'Mumbai, India',
        salary: '₹9L - ₹14L',
        employment_type: 'full-time',
        skills_required: ['React', 'Node.js', 'MongoDB']
      }
    ];
  };

  const filteredJobs = jobs.filter(job => {
    if (filter === 'all') return true;
    return job.employment_type === filter;
  }).filter(job => 
    job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.company.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="job-listings">
      <h1>Job Opportunities</h1>
      
      <div className="filters-section">
        <input
          type="text"
          placeholder="Search jobs..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All Jobs</option>
          <option value="full-time">Full Time</option>
          <option value="part-time">Part Time</option>
          <option value="contract">Contract</option>
          <option value="remote">Remote</option>
        </select>
      </div>

      {userSkills.length > 0 && (
        <div className="skills-banner">
          <span>Jobs matching your skills: </span>
          {userSkills.slice(0, 5).map((skill, i) => (
            <span key={i} className="skill-pill">{skill}</span>
          ))}
        </div>
      )}

      {loading ? (
        <div className="loading">Loading jobs...</div>
      ) : filteredJobs.length > 0 ? (
        <div className="jobs-grid">
          {filteredJobs.map(job => (
            <div key={job.id} className="job-card">
              <h3>{job.title}</h3>
              <p className="company">{job.company}</p>
              <p className="location">📍 {job.location}</p>
              <p className="description">{job.description}</p>
              
              {job.skills_required && (
                <div className="job-skills">
                  {job.skills_required.slice(0, 4).map((skill, i) => (
                    <span key={i} className="skill-tag">{skill.name || skill}</span>
                  ))}
                </div>
              )}
              
              {job.salary && (
                <p className="salary">💰 {job.salary}</p>
              )}
              
              <button className="apply-btn">Apply Now</button>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-jobs">
          <p>No jobs found matching your criteria.</p>
          <button onClick={fetchJobs} className="retry-btn">
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}

export default JobListings;
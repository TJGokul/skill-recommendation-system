// frontend/src/context/JobContext.jsx

import React, { createContext, useState, useContext, useEffect } from 'react';

const JobContext = createContext();

export const useJobs = () => {
  const context = useContext(JobContext);
  if (!context) {
    throw new Error('useJobs must be used within JobProvider');
  }
  return context;
};

export const JobProvider = ({ children }) => {
  const [jobs, setJobs] = useState([]);
  const [skills, setSkills] = useState([]);
  const [parsedResumeData, setParsedResumeData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('jobData');
    if (saved) {
      try {
        const data = JSON.parse(saved);
        const age = Date.now() - new Date(data.timestamp).getTime();
        if (age < 24 * 60 * 60 * 1000) { // 24 hours
          setJobs(data.jobs || []);
          setSkills(data.skills || []);
          setParsedResumeData(data.parsedResumeData || null);
          setLastUpdated(data.timestamp);
        }
      } catch (e) {
        console.error('Failed to load saved jobs', e);
      }
    }
  }, []);

  const updateJobs = (newJobs, newSkills, newParsedData = null) => {
    setJobs(newJobs);
    setSkills(newSkills);
    if (newParsedData) {
      setParsedResumeData(newParsedData);
    }
    const timestamp = new Date().toISOString();
    setLastUpdated(timestamp);
    
    // Save to localStorage
    localStorage.setItem('jobData', JSON.stringify({
      jobs: newJobs,
      skills: newSkills,
      parsedResumeData: newParsedData || parsedResumeData,
      timestamp
    }));
  };

  const clearJobs = () => {
    setJobs([]);
    setSkills([]);
    setParsedResumeData(null);
    setLastUpdated(null);
    localStorage.removeItem('jobData');
  };

  return (
    <JobContext.Provider value={{
      jobs,
      skills,
      parsedResumeData,
      lastUpdated,
      loading,
      error,
      setLoading,
      setError,
      updateJobs,
      clearJobs
    }}>
      {children}
    </JobContext.Provider>
  );
};
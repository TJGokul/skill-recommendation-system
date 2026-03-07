// frontend/src/components/JobMatches.jsx

import React, { useState, useEffect, useMemo, useRef } from 'react';
import axios from 'axios';
import { useJobs } from '../context/JobContext';
import './JobMatches.css';

function JobMatches() {
  const { jobs, skills, loading: contextLoading, error: contextError, updateJobs } = useJobs();
  
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [searchFilters, setSearchFilters] = useState({
    location: '',
    jobType: 'all',
    remote: false,
    experience: 'all',
    sortBy: 'match'
  });
  const [stats, setStats] = useState({ total: 0, time: 0, source: '' });
  const [activeTab, setActiveTab] = useState('grid');
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const jobsPerPage = 6;

  // Update filtered jobs when jobs or filters change
  useEffect(() => {
    if (!jobs || jobs.length === 0) {
      setFilteredJobs([]);
      return;
    }

    let filtered = jobs.filter(job => {
      if (searchFilters.location && 
          !job.location?.toLowerCase().includes(searchFilters.location.toLowerCase())) {
        return false;
      }
      if (searchFilters.jobType !== 'all' && 
          job.job_type !== searchFilters.jobType) {
        return false;
      }
      if (searchFilters.remote && !job.is_remote) {
        return false;
      }
      if (searchFilters.experience !== 'all') {
        const title = job.title?.toLowerCase() || '';
        if (searchFilters.experience === 'entry' && 
            !title.includes('fresher') && !title.includes('trainee') && !title.includes('junior')) {
          return false;
        }
        if (searchFilters.experience === 'senior' && 
            !title.includes('senior') && !title.includes('lead') && !title.includes('principal')) {
          return false;
        }
      }
      return true;
    });

    // Sort jobs
    switch (searchFilters.sortBy) {
      case 'match':
        filtered.sort((a, b) => (b.match_score || 0) - (a.match_score || 0));
        break;
      case 'date':
        filtered.sort((a, b) => (b.posted_date || '').localeCompare(a.posted_date || ''));
        break;
      default:
        break;
    }

    setFilteredJobs(filtered);
    setStats({
      total: jobs.length,
      time: 'N/A',
      source: 'Saved Jobs'
    });
    setCurrentPage(1);
  }, [jobs, searchFilters]);

  // Pagination
  const paginatedJobs = useMemo(() => {
    const start = (currentPage - 1) * jobsPerPage;
    return filteredJobs.slice(start, start + jobsPerPage);
  }, [filteredJobs, currentPage]);

  const totalPages = Math.ceil(filteredJobs.length / jobsPerPage);

  const handleFilterChange = (key, value) => {
    setSearchFilters(prev => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setSearchFilters({
      location: '',
      jobType: 'all',
      remote: false,
      experience: 'all',
      sortBy: 'match'
    });
  };

  const getPlatformInfo = (source) => {
    if (!source) return { icon: '💼', name: 'Job Portal', color: '#667eea' };
    const s = source.toLowerCase();
    if (s.includes('linkedin')) return { icon: '🔗', name: 'LinkedIn', color: '#0077b5' };
    if (s.includes('indeed')) return { icon: '📋', name: 'Indeed', color: '#003a9b' };
    if (s.includes('glassdoor')) return { icon: '🏢', name: 'Glassdoor', color: '#0caa41' };
    if (s.includes('naukri')) return { icon: '🇮🇳', name: 'Naukri', color: '#ff5353' };
    return { icon: '💼', name: source, color: '#667eea' };
  };

  // Show loading state
  if (contextLoading || loading) {
    return (
      <div className="jm-loading-container">
        <div className="jm-loading-spinner">
          <div className="jm-spinner-ring"></div>
          <div className="jm-spinner-ring"></div>
          <div className="jm-spinner-ring"></div>
        </div>
        <p className="jm-loading-text">Loading your saved jobs...</p>
      </div>
    );
  }

  // Show error state
  if (contextError || error) {
    return (
      <div className="jm-error-glass">
        <div className="jm-error-icon">⚠️</div>
        <h3>Oops! Something went wrong</h3>
        <p>{contextError || error}</p>
      </div>
    );
  }

  // Show empty state
  if (!jobs || jobs.length === 0) {
    return (
      <div className="jm-empty-glass">
        <div className="jm-empty-icon">📭</div>
        <h3>No jobs found</h3>
        <p>Upload a resume to see personalized job matches</p>
        <a href="/upload" className="jm-retry-btn">
          Go to Upload
        </a>
      </div>
    );
  }

  return (
    <div className="jm-wrapper">
      {/* Header Section */}
      <div className="jm-header-glass">
        <div className="jm-header-content">
          <h1 className="jm-title">
            <span className="jm-title-gradient">🎯 Your Job Matches</span>
          </h1>
          <p className="jm-subtitle">
            Based on your skills: {skills.slice(0, 3).map(s => s.name || s).join(' • ')}
          </p>
        </div>
        
        {/* Stats Card */}
        {jobs.length > 0 && (
          <div className="jm-stats-card">
            <div className="jm-stat-item">
              <span className="jm-stat-value">{stats.total}</span>
              <span className="jm-stat-label">Jobs Found</span>
            </div>
            <div className="jm-stat-divider"></div>
            <div className="jm-stat-item">
              <span className="jm-stat-value">{filteredJobs.length}</span>
              <span className="jm-stat-label">After Filters</span>
            </div>
          </div>
        )}
      </div>

      {/* Filters Section */}
      {filteredJobs.length > 0 && (
        <div className="jm-filters-glass">
          <div className="jm-filters-header">
            <h3>🔍 Filter Jobs</h3>
            <button onClick={clearFilters} className="jm-clear-filters">
              Clear All
            </button>
          </div>
          
          <div className="jm-filters-grid">
            <input
              type="text"
              placeholder="📍 Location"
              value={searchFilters.location}
              onChange={(e) => handleFilterChange('location', e.target.value)}
              className="jm-filter-input"
            />
            
            <select 
              value={searchFilters.jobType}
              onChange={(e) => handleFilterChange('jobType', e.target.value)}
              className="jm-filter-select"
            >
              <option value="all">All Job Types</option>
              <option value="fulltime">Full Time</option>
              <option value="parttime">Part Time</option>
              <option value="contract">Contract</option>
              <option value="intern">Internship</option>
            </select>
            
            <label className="jm-filter-checkbox">
              <input
                type="checkbox"
                checked={searchFilters.remote}
                onChange={(e) => handleFilterChange('remote', e.target.checked)}
              />
              <span>🌍 Remote Only</span>
            </label>
            
            <select
              value={searchFilters.experience}
              onChange={(e) => handleFilterChange('experience', e.target.value)}
              className="jm-filter-select"
            >
              <option value="all">All Levels</option>
              <option value="entry">Entry Level / Fresher</option>
              <option value="mid">Mid Level</option>
              <option value="senior">Senior Level</option>
            </select>

            <select
              value={searchFilters.sortBy}
              onChange={(e) => handleFilterChange('sortBy', e.target.value)}
              className="jm-filter-select"
            >
              <option value="match">Sort by Match</option>
              <option value="date">Sort by Date</option>
            </select>
          </div>
        </div>
      )}

      {/* View Toggle */}
      {filteredJobs.length > 0 && (
        <div className="jm-view-toggle">
          <button 
            className={`jm-view-btn ${activeTab === 'grid' ? 'active' : ''}`}
            onClick={() => setActiveTab('grid')}
          >
            📱 Grid View
          </button>
          <button 
            className={`jm-view-btn ${activeTab === 'list' ? 'active' : ''}`}
            onClick={() => setActiveTab('list')}
          >
            📋 List View
          </button>
        </div>
      )}

      {/* Results Count */}
      {filteredJobs.length > 0 && (
        <div className="jm-results-count">
          Showing <strong>{paginatedJobs.length}</strong> of <strong>{filteredJobs.length}</strong> jobs
        </div>
      )}

      {/* Jobs Grid */}
      {paginatedJobs.length > 0 && (
        <>
          <div className={`jm-${activeTab}-view`}>
            {paginatedJobs.map((job, index) => {
              const platform = getPlatformInfo(job.source);
              return (
                <div key={job.id || index} className={`jm-card jm-card-${activeTab}`}>
                  <div className="jm-card-header">
                    <div className="jm-card-title-section">
                      <h3 className="jm-card-title">{job.title}</h3>
                      <span className="jm-card-badge" style={{ 
                        background: `linear-gradient(135deg, ${platform.color}, ${platform.color}dd)` 
                      }}>
                        {job.match_score || 75}% Match
                      </span>
                    </div>
                    
                    <div className="jm-card-company">
                      <span className="jm-card-company-name">{job.company}</span>
                    </div>
                  </div>

                  <div className="jm-card-body">
                    <div className="jm-card-meta">
                      <span className="jm-card-location">📍 {job.location || 'Worldwide'}</span>
                      {job.is_remote && (
                        <span className="jm-card-remote">🌍 Remote</span>
                      )}
                    </div>

                    <p className="jm-card-description">{job.description}</p>

                    {job.salary && (
                      <div className="jm-card-salary">💰 {job.salary}</div>
                    )}

                    <div className="jm-card-footer">
                      <span className="jm-card-source">via {job.source}</span>
                      <a 
                        href={job.apply_url || '#'}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="jm-card-apply"
                      >
                        Apply →
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="jm-pagination">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="jm-page-btn"
              >
                ←
              </button>
              <span className="jm-page-info">
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="jm-page-btn"
              >
                →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default JobMatches;
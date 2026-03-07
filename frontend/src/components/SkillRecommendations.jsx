// frontend/src/components/SkillRecommendations.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SkillRecommendations.css';

function SkillRecommendations({ parsedSkills, resumeText }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userSkills, setUserSkills] = useState([]);
  const [userDomain, setUserDomain] = useState('general');
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [usingAI, setUsingAI] = useState(false);

  // Extract skills from parsed data
  useEffect(() => {
    console.log("📥 Received parsedSkills:", parsedSkills);
    
    if (parsedSkills) {
      const skills = extractSkills(parsedSkills);
      setUserSkills(skills);
      
      // Try to get AI recommendations first
      fetchAIRecommendations(skills, resumeText);
    } else {
      console.log("⚠️ No parsed skills, using fallback");
      generateFallbackRecommendations();
    }
  }, [parsedSkills, resumeText]);

  const extractSkills = (data) => {
    let skills = [];
    
    if (Array.isArray(data)) {
      skills = data.map(s => {
        if (typeof s === 'string') return s.toLowerCase();
        if (s.name) return s.name.toLowerCase();
        return '';
      }).filter(s => s && s.length > 1);
    } 
    else if (data?.flat_list && Array.isArray(data.flat_list)) {
      skills = data.flat_list.map(s => {
        if (typeof s === 'string') return s.toLowerCase();
        return s.name?.toLowerCase() || '';
      }).filter(s => s && s.length > 1);
    } 
    else if (data?.skills && Array.isArray(data.skills)) {
      skills = data.skills.map(s => {
        if (typeof s === 'string') return s.toLowerCase();
        return s.name?.toLowerCase() || '';
      }).filter(s => s && s.length > 1);
    }
    else if (data?.by_category) {
      Object.values(data.by_category).forEach(catSkills => {
        if (Array.isArray(catSkills)) {
          catSkills.forEach(s => {
            if (s.name) skills.push(s.name.toLowerCase());
          });
        }
      });
    }
    
    skills = [...new Set(skills)];
    console.log("📊 Extracted skills:", skills);
    return skills;
  };

  const fetchAIRecommendations = async (skills, resumeText) => {
    setLoading(true);
    setError(null);
    
    try {
      // Try to get AI-powered recommendations from backend
      const response = await axios.post(
        'http://localhost:8000/api/ai-skill-recommendations/',
        {
          skills: skills,
          resume_text: resumeText || '',
          career_goal: ''
        },
        { timeout: 10000 }
      );
      
      if (response.data && response.data.recommendations) {
        console.log("🤖 AI Recommendations received:", response.data);
        
        // Add course URLs to each recommendation
        const enhancedRecs = response.data.recommendations.map(rec => ({
          ...rec,
          courses: generateCourseLinks(rec.name)
        }));
        
        setRecommendations(enhancedRecs);
        setUserDomain(response.data.domain || determineDomain(skills));
        setUsingAI(true);
      } else {
        // Fallback to rule-based recommendations
        console.log("⚠️ AI failed, using rule-based");
        generateRuleBasedRecommendations(skills);
      }
    } catch (error) {
      console.error("❌ AI Error:", error);
      setError("AI service unavailable, using rule-based recommendations");
      generateRuleBasedRecommendations(skills);
    } finally {
      setLoading(false);
    }
  };

  const generateCourseLinks = (skillName) => {
    // Generate course links for any skill
    const encodedSkill = encodeURIComponent(skillName);
    return [
      { platform: 'Coursera', url: `https://www.coursera.org/search?query=${encodedSkill}` },
      { platform: 'Udemy', url: `https://www.udemy.com/courses/search/?q=${encodedSkill}` },
      { platform: 'YouTube', url: `https://www.youtube.com/results?search_query=${encodedSkill}+tutorial` }
    ];
  };

  const determineDomain = (skills) => {
    const skillStr = skills.join(' ').toLowerCase();
    
    if (skillStr.includes('chemical') || skillStr.includes('process') || skillStr.includes('reactor') || 
        skillStr.includes('chemistry') || skillStr.includes('lab') || skillStr.includes('distillation')) {
      return 'chemical';
    }
    if (skillStr.includes('mechanical') || skillStr.includes('cad') || skillStr.includes('solidworks') ||
        skillStr.includes('autocad') || skillStr.includes('thermodynamics')) {
      return 'mechanical';
    }
    if (skillStr.includes('electrical') || skillStr.includes('circuit') || skillStr.includes('plc') ||
        skillStr.includes('electronics') || skillStr.includes('power')) {
      return 'electrical';
    }
    if (skillStr.includes('civil') || skillStr.includes('structural') || skillStr.includes('construction') ||
        skillStr.includes('building')) {
      return 'civil';
    }
    if (skillStr.includes('support') || skillStr.includes('help desk') || skillStr.includes('troubleshoot') || 
        skillStr.includes('windows') || skillStr.includes('active directory') || skillStr.includes('network')) {
      return 'itsupport';
    }
    if (skillStr.includes('python') || skillStr.includes('java') || skillStr.includes('javascript') || 
        skillStr.includes('react') || skillStr.includes('sql') || skillStr.includes('programming')) {
      return 'programming';
    }
    return 'general';
  };

  const generateRuleBasedRecommendations = (currentSkills) => {
    console.log("📚 Generating rule-based recommendations for:", currentSkills);
    
    const domain = determineDomain(currentSkills);
    setUserDomain(domain);
    
    let recommendations = [];
    
    // Domain-specific recommendations
    if (domain === 'chemical') {
      recommendations = [
        { name: 'ASPEN Plus', demand: 85, time: 60, category: 'chemical', matchScore: 95,
          reason: 'Industry standard for process simulation' },
        { name: 'Process Design', demand: 88, time: 70, category: 'chemical', matchScore: 94,
          reason: 'Essential for chemical plant design' },
        { name: 'Heat Transfer', demand: 84, time: 50, category: 'chemical', matchScore: 92,
          reason: 'Core concept in chemical engineering' },
        { name: 'Reaction Engineering', demand: 82, time: 65, category: 'chemical', matchScore: 91,
          reason: 'Critical for reactor design' },
        { name: 'Fluid Mechanics', demand: 83, time: 55, category: 'chemical', matchScore: 90,
          reason: 'Fundamental for process flow' }
      ];
    }
    else if (domain === 'mechanical') {
      recommendations = [
        { name: 'SolidWorks', demand: 88, time: 55, category: 'mechanical', matchScore: 95,
          reason: 'Industry standard 3D CAD software' },
        { name: 'AutoCAD', demand: 89, time: 50, category: 'mechanical', matchScore: 94,
          reason: 'Essential for 2D/3D design' },
        { name: 'ANSYS', demand: 86, time: 60, category: 'mechanical', matchScore: 92,
          reason: 'Powerful simulation tool' },
        { name: 'CATIA', demand: 84, time: 65, category: 'mechanical', matchScore: 90,
          reason: 'Advanced CAD/CAM software' },
        { name: 'FEA', demand: 85, time: 70, category: 'mechanical', matchScore: 89,
          reason: 'Finite Element Analysis' }
      ];
    }
    else if (domain === 'electrical') {
      recommendations = [
        { name: 'MATLAB', demand: 87, time: 50, category: 'electrical', matchScore: 95,
          reason: 'Essential for simulation and analysis' },
        { name: 'PLC Programming', demand: 86, time: 55, category: 'electrical', matchScore: 94,
          reason: 'Industrial automation standard' },
        { name: 'PCB Design', demand: 84, time: 60, category: 'electrical', matchScore: 92,
          reason: 'Circuit board design' },
        { name: 'Arduino', demand: 82, time: 35, category: 'electrical', matchScore: 90,
          reason: 'Embedded systems prototyping' },
        { name: 'AutoCAD Electrical', demand: 83, time: 50, category: 'electrical', matchScore: 89,
          reason: 'Electrical design software' }
      ];
    }
    else if (domain === 'civil') {
      recommendations = [
        { name: 'Revit', demand: 88, time: 55, category: 'civil', matchScore: 95,
          reason: 'BIM software for architecture' },
        { name: 'AutoCAD Civil 3D', demand: 87, time: 50, category: 'civil', matchScore: 94,
          reason: 'Civil engineering design' },
        { name: 'STAAD.Pro', demand: 85, time: 60, category: 'civil', matchScore: 92,
          reason: 'Structural analysis' },
        { name: 'ETABS', demand: 84, time: 65, category: 'civil', matchScore: 91,
          reason: 'Building design software' },
        { name: 'Primavera P6', demand: 82, time: 50, category: 'civil', matchScore: 89,
          reason: 'Project management' }
      ];
    }
    else if (domain === 'itsupport') {
      recommendations = [
        { name: 'Active Directory', demand: 86, time: 35, category: 'itsupport', matchScore: 95,
          reason: 'Windows domain management' },
        { name: 'Linux Administration', demand: 88, time: 60, category: 'itsupport', matchScore: 94,
          reason: 'Server management' },
        { name: 'Networking Basics', demand: 89, time: 40, category: 'itsupport', matchScore: 93,
          reason: 'CCNA, TCP/IP fundamentals' },
        { name: 'CompTIA A+', demand: 87, time: 80, category: 'itsupport', matchScore: 92,
          reason: 'Hardware certification' },
        { name: 'Windows Server', demand: 85, time: 55, category: 'itsupport', matchScore: 91,
          reason: 'Server administration' }
      ];
    }
    else if (domain === 'programming') {
      // Detect specific tech stack
      const skillsStr = currentSkills.join(' ').toLowerCase();
      
      if (skillsStr.includes('python')) {
        recommendations = [
          { name: 'Django', demand: 88, time: 50, category: 'frameworks', matchScore: 95,
            reason: 'Python web framework' },
          { name: 'FastAPI', demand: 87, time: 40, category: 'frameworks', matchScore: 94,
            reason: 'Modern Python API framework' },
          { name: 'Pandas', demand: 86, time: 35, category: 'data', matchScore: 93,
            reason: 'Data analysis library' }
        ];
      }
      else if (skillsStr.includes('java')) {
        recommendations = [
          { name: 'Spring Boot', demand: 89, time: 60, category: 'frameworks', matchScore: 95,
            reason: 'Java enterprise framework' },
          { name: 'Hibernate', demand: 85, time: 45, category: 'frameworks', matchScore: 93,
            reason: 'ORM for Java' },
          { name: 'Maven', demand: 82, time: 30, category: 'tools', matchScore: 90,
            reason: 'Build automation' }
        ];
      }
      else if (skillsStr.includes('javascript') || skillsStr.includes('react')) {
        recommendations = [
          { name: 'TypeScript', demand: 92, time: 45, category: 'programming', matchScore: 95,
            reason: 'Typed JavaScript superset' },
          { name: 'Next.js', demand: 90, time: 50, category: 'frameworks', matchScore: 94,
            reason: 'React framework' },
          { name: 'Node.js', demand: 91, time: 50, category: 'frameworks', matchScore: 93,
            reason: 'Backend JavaScript' }
        ];
      }
      else {
        recommendations = [
          { name: 'Python', demand: 95, time: 60, category: 'programming', matchScore: 90,
            reason: 'Most versatile language' },
          { name: 'JavaScript', demand: 98, time: 50, category: 'programming', matchScore: 95,
            reason: 'Essential for web' },
          { name: 'React', demand: 96, time: 45, category: 'frameworks', matchScore: 92,
            reason: 'Popular frontend library' }
        ];
      }
      
      // Add generic recommendations
      recommendations.push(
        { name: 'Docker', demand: 92, time: 40, category: 'cloud', matchScore: 88,
          reason: 'Containerization' },
        { name: 'AWS', demand: 94, time: 80, category: 'cloud', matchScore: 87,
          reason: 'Cloud computing' }
      );
    }
    else {
      // General recommendations
      recommendations = [
        { name: 'Python', demand: 95, time: 60, category: 'programming', matchScore: 85,
          reason: 'Most in-demand language' },
        { name: 'Communication', demand: 98, time: 30, category: 'soft', matchScore: 90,
          reason: 'Essential for all roles' },
        { name: 'Project Management', demand: 94, time: 60, category: 'soft', matchScore: 85,
          reason: 'Lead projects effectively' },
        { name: 'Data Analysis', demand: 89, time: 50, category: 'data', matchScore: 80,
          reason: 'Make data-driven decisions' }
      ];
    }
    
    // Add course links to all recommendations
    const withCourses = recommendations.map(rec => ({
      ...rec,
      courses: generateCourseLinks(rec.name)
    }));
    
    setRecommendations(withCourses);
  };

  const generateFallbackRecommendations = () => {
    console.log("📚 Generating fallback recommendations");
    const fallback = [
      {
        name: 'Python',
        demand: 95,
        time: 60,
        category: 'programming',
        matchScore: 90,
        reason: 'Most in-demand programming language',
        courses: generateCourseLinks('Python')
      },
      {
        name: 'JavaScript',
        demand: 98,
        time: 50,
        category: 'programming',
        matchScore: 95,
        reason: 'Essential for web development',
        courses: generateCourseLinks('JavaScript')
      },
      {
        name: 'React',
        demand: 96,
        time: 45,
        category: 'frameworks',
        matchScore: 92,
        reason: 'Popular frontend framework',
        courses: generateCourseLinks('React')
      },
      {
        name: 'SQL',
        demand: 94,
        time: 40,
        category: 'databases',
        matchScore: 88,
        reason: 'Database management',
        courses: generateCourseLinks('SQL')
      },
      {
        name: 'AWS',
        demand: 94,
        time: 80,
        category: 'cloud',
        matchScore: 85,
        reason: 'Cloud computing platform',
        courses: generateCourseLinks('AWS')
      },
      {
        name: 'Communication',
        demand: 98,
        time: 30,
        category: 'soft',
        matchScore: 80,
        reason: 'Critical soft skill',
        courses: generateCourseLinks('Communication skills')
      }
    ];
    setRecommendations(fallback);
    setLoading(false);
  };

  const filteredRecommendations = selectedCategory === 'all' 
    ? recommendations 
    : recommendations.filter(s => s.category === selectedCategory);

  const getCategoryIcon = (category) => {
    const icons = {
      'programming': '💻',
      'frameworks': '🛠️',
      'databases': '🗄️',
      'cloud': '☁️',
      'chemical': '🧪',
      'mechanical': '⚙️',
      'electrical': '⚡',
      'civil': '🏗️',
      'itsupport': '🔧',
      'data': '📊',
      'soft': '🤝',
      'general': '📚',
      'tools': '🔨'
    };
    return icons[category] || '📌';
  };

  const handleFindCourses = (skill) => {
    if (skill.courses && skill.courses.length > 0) {
      // Open multiple course platforms in new tabs
      skill.courses.forEach((course, index) => {
        setTimeout(() => {
          window.open(course.url, '_blank');
        }, index * 200); // Open each with slight delay
      });
    } else {
      const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(skill.name + ' online course')}`;
      window.open(searchUrl, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="sr-loading">
        <div className="sr-spinner"></div>
        <h3>Analyzing your skills with AI...</h3>
        {userSkills.length > 0 ? (
          <p className="sr-loading-subtext">
            Detected: {userSkills.slice(0, 5).join(' • ')}
          </p>
        ) : (
          <p className="sr-loading-subtext">Preparing personalized recommendations...</p>
        )}
      </div>
    );
  }

  if (error) {
    return (
      <div className="sr-error">
        <p>{error}</p>
        <button onClick={() => generateRuleBasedRecommendations(userSkills)}>
          Try Again
        </button>
      </div>
    );
  }

  const categories = [...new Set(recommendations.map(r => r.category))];

  return (
    <div className="sr-container">
      {/* Header */}
      <div className="sr-header">
        <h1 className="sr-title">
          <span className="sr-title-gradient">
            {usingAI ? '🤖 AI-Powered' : '🎯'} Personalized Skill Recommendations
          </span>
        </h1>
        {userSkills.length > 0 ? (
          <>
            <p className="sr-subtitle">
              Based on your skills: {userSkills.slice(0, 6).join(' • ')}
              {userSkills.length > 6 && ` +${userSkills.length - 6} more`}
            </p>
            <div className="sr-domain-badge">
              {userDomain === 'programming' && '💻 Software Development'}
              {userDomain === 'chemical' && '🧪 Chemical Engineering'}
              {userDomain === 'mechanical' && '⚙️ Mechanical Engineering'}
              {userDomain === 'electrical' && '⚡ Electrical Engineering'}
              {userDomain === 'civil' && '🏗️ Civil Engineering'}
              {userDomain === 'itsupport' && '🔧 IT Support'}
              {userDomain === 'general' && '📚 General Skills'}
            </div>
            {usingAI && (
              <p className="sr-ai-badge">✨ AI-generated recommendations</p>
            )}
          </>
        ) : (
          <p className="sr-subtitle">
            Upload your resume to get personalized AI recommendations
          </p>
        )}
      </div>

      {/* Category Filter */}
      {categories.length > 1 && (
        <div className="sr-category-filter">
          <button 
            className={`sr-filter-btn ${selectedCategory === 'all' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('all')}
          >
            All
          </button>
          {categories.map(cat => (
            <button
              key={cat}
              className={`sr-filter-btn ${selectedCategory === cat ? 'active' : ''}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {getCategoryIcon(cat)} {cat}
            </button>
          ))}
        </div>
      )}

      {/* Recommendations Grid */}
      {filteredRecommendations.length > 0 ? (
        <div className="sr-grid">
          {filteredRecommendations.map((skill, index) => (
            <div key={index} className="sr-card" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="sr-card-header">
                <span className="sr-card-icon">{getCategoryIcon(skill.category)}</span>
                <h3>{skill.name}</h3>
                <span className="sr-match-badge">{skill.matchScore}% Match</span>
              </div>
              
              <div className="sr-card-body">
                <div className="sr-skill-meta">
                  <span className="sr-demand">
                    Market Demand: <strong>{skill.demand}%</strong>
                  </span>
                  <span className="sr-time">
                    ⏱️ {skill.time}h
                  </span>
                </div>
                
                <div className="sr-progress">
                  <div 
                    className="sr-progress-bar"
                    style={{ width: `${skill.demand}%` }}
                  ></div>
                </div>

                {skill.reason && (
                  <p className="sr-reason">{skill.reason}</p>
                )}

                <div className="sr-skill-category">
                  {skill.category === 'chemical' && '🧪 Chemical Engineering'}
                  {skill.category === 'mechanical' && '⚙️ Mechanical Engineering'}
                  {skill.category === 'electrical' && '⚡ Electrical Engineering'}
                  {skill.category === 'civil' && '🏗️ Civil Engineering'}
                  {skill.category === 'itsupport' && '🔧 IT Support'}
                  {skill.category === 'programming' && '💻 Programming'}
                  {skill.category === 'frameworks' && '🛠️ Framework'}
                  {skill.category === 'databases' && '🗄️ Database'}
                  {skill.category === 'cloud' && '☁️ Cloud'}
                  {skill.category === 'data' && '📊 Data Science'}
                  {skill.category === 'soft' && '🤝 Soft Skill'}
                  {skill.category === 'tools' && '🔨 Development Tools'}
                </div>
                
                <button 
                  onClick={() => handleFindCourses(skill)}
                  className="sr-learn-btn"
                >
                  Find Courses →
                </button>

                {skill.courses && skill.courses.length > 1 && (
                  <p className="sr-course-note">
                    {skill.courses.length} platforms available
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="sr-empty">
          <div className="sr-empty-icon">📚</div>
          <h3>No recommendations available</h3>
          <p>Try uploading a resume with more specific skills</p>
          <button 
            onClick={() => generateFallbackRecommendations()}
            className="sr-fallback-btn"
          >
            Show Popular Skills
          </button>
        </div>
      )}
    </div>
  );
}

export default SkillRecommendations;
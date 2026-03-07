import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SkillGapAnalysis.css';

function SkillGapAnalysis({ skills, experience }) {
  const [targetRole, setTargetRole] = useState('');
  const [customRole, setCustomRole] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [suggestedRoles, setSuggestedRoles] = useState([]);

  // Common roles and their required skills
  const roleDatabase = {
    'Frontend Developer': ['javascript', 'react', 'html', 'css', 'typescript', 'angular', 'vue'],
    'Backend Developer': ['python', 'java', 'sql', 'django', 'node.js', 'spring', 'c#'],
    'Full Stack Developer': ['javascript', 'react', 'python', 'sql', 'node.js', 'django', 'html', 'css'],
    'Data Scientist': ['python', 'sql', 'machine learning', 'statistics', 'pandas', 'r', 'tensorflow'],
    'Data Analyst': ['sql', 'excel', 'tableau', 'python', 'power bi', 'statistics'],
    'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'jenkins', 'linux', 'terraform', 'ci/cd'],
    'Cloud Architect': ['aws', 'azure', 'gcp', 'terraform', 'networking', 'docker'],
    'Mobile Developer': ['swift', 'kotlin', 'react native', 'flutter', 'android', 'ios'],
    'Product Manager': ['agile', 'scrum', 'market research', 'analytics', 'communication', 'leadership'],
    'QA Engineer': ['selenium', 'test automation', 'jira', 'manual testing', 'python', 'cypress'],
    'UX/UI Designer': ['figma', 'sketch', 'adobe xd', 'user research', 'prototyping', 'wireframing']
  };

  useEffect(() => {
    suggestRolesBasedOnSkills();
  }, [skills]);

  const suggestRolesBasedOnSkills = () => {
    const suggestions = [];
    const userSkillNames = skills.map(s => 
      (typeof s === 'string' ? s : s.name || '').toLowerCase()
    ).filter(Boolean);
    
    for (const [role, requiredSkills] of Object.entries(roleDatabase)) {
      const matchedSkills = requiredSkills.filter(skill => 
        userSkillNames.includes(skill.toLowerCase())
      );
      
      const matchPercentage = requiredSkills.length > 0 
        ? (matchedSkills.length / requiredSkills.length) * 100 
        : 0;
      
      if (matchPercentage > 20) {
        suggestions.push({
          role,
          matchPercentage: Math.round(matchPercentage),
          matchedSkills
        });
      }
    }
    
    setSuggestedRoles(suggestions.sort((a, b) => b.matchPercentage - a.matchPercentage));
  };

  const analyzeRole = async () => {
    const role = customRole || targetRole;
    if (!role) return;
    
    setLoading(true);
    
    try {
      // Try API first
      const response = await axios.post('http://localhost:8000/api/analyze-role/', {
        role: role,
        skills: skills
      });
      
      setAnalysis(response.data);
    } catch (error) {
      console.log('Using local analysis fallback');
      // Fallback to local analysis
      localAnalysis(role);
    }
    
    setLoading(false);
  };

  const localAnalysis = (role) => {
    const roleLower = role.toLowerCase();
    let suggestedSkills = [];
    
    // Check against database first
    if (roleDatabase[role]) {
      suggestedSkills = roleDatabase[role];
    } else {
      // Generate based on keywords
      if (roleLower.includes('frontend') || roleLower.includes('ui') || roleLower.includes('web')) {
        suggestedSkills.push('React', 'JavaScript', 'HTML/CSS', 'TypeScript', 'CSS');
      }
      if (roleLower.includes('backend') || roleLower.includes('api')) {
        suggestedSkills.push('Python', 'Java', 'SQL', 'Node.js', 'REST APIs', 'Django');
      }
      if (roleLower.includes('data') || roleLower.includes('analytics') || roleLower.includes('scientist')) {
        suggestedSkills.push('Python', 'SQL', 'Statistics', 'Machine Learning', 'Pandas', 'NumPy');
      }
      if (roleLower.includes('cloud') || roleLower.includes('devops')) {
        suggestedSkills.push('AWS', 'Azure', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform');
      }
      if (roleLower.includes('mobile')) {
        suggestedSkills.push('Swift', 'Kotlin', 'React Native', 'Flutter', 'Mobile UI/UX');
      }
      if (roleLower.includes('product')) {
        suggestedSkills.push('Agile', 'Scrum', 'Market Research', 'Analytics', 'Communication', 'Leadership');
      }
      if (roleLower.includes('qa') || roleLower.includes('test')) {
        suggestedSkills.push('Selenium', 'Test Automation', 'Jira', 'Manual Testing', 'Python', 'Cypress');
      }
    }
    
    // Remove duplicates
    suggestedSkills = [...new Set(suggestedSkills)];
    
    const userSkillNames = skills.map(s => 
      (typeof s === 'string' ? s : s.name || '').toLowerCase()
    );
    
    const matched = suggestedSkills.filter(skill => 
      userSkillNames.includes(skill.toLowerCase())
    );
    
    const missing = suggestedSkills.filter(skill => 
      !userSkillNames.includes(skill.toLowerCase())
    );
    
    const matchScore = suggestedSkills.length > 0 
      ? Math.round((matched.length / suggestedSkills.length) * 100)
      : 0;
    
    setAnalysis({
      role: role,
      requiredSkills: suggestedSkills,
      matchedSkills: matched,
      missingSkills: missing,
      matchScore: matchScore
    });
  };

  return (
    <div className="dynamic-skill-gap">
      <h2>📊 Smart Skill Gap Analysis</h2>
      
      <div className="role-input-section">
        <h3>🎯 What role are you targeting?</h3>
        
        <div className="suggested-roles">
          <p>Suggested based on your skills:</p>
          <div className="role-chips">
            {suggestedRoles.slice(0, 5).map(item => (
              <button
                key={item.role}
                className={`role-chip ${targetRole === item.role ? 'selected' : ''}`}
                onClick={() => {
                  setTargetRole(item.role);
                  setCustomRole('');
                }}
              >
                {item.role} ({item.matchPercentage}% match)
              </button>
            ))}
          </div>
        </div>
        
        <div className="custom-role">
          <p>Or enter your own target role:</p>
          <div className="custom-input">
            <input
              type="text"
              value={customRole}
              onChange={(e) => setCustomRole(e.target.value)}
              placeholder="e.g., AI Engineer, Blockchain Developer"
            />
            <button 
              className="btn btn-primary"
              onClick={analyzeRole}
              disabled={loading || !(customRole || targetRole)}
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>
      </div>
      
      {analysis && (
        <div className="analysis-results">
          <h3>Analysis for: {analysis.role}</h3>
          
          <div className="match-circle">
            <div className="circle" style={{
              background: `conic-gradient(#667eea ${analysis.matchScore * 3.6}deg, #f0f0f0 0deg)`
            }}>
              <span>{analysis.matchScore}%</span>
            </div>
            <p>Match Score</p>
          </div>
          
          <div className="skills-breakdown">
            <div className="required-skills">
              <h4>Required Skills</h4>
              <div className="skill-tags">
                {analysis.requiredSkills.map((skill, i) => (
                  <span key={i} className="skill-tag info">{skill}</span>
                ))}
              </div>
            </div>
            
            <div className="missing-skills">
              <h4>Skills to Learn</h4>
              {analysis.missingSkills.length > 0 ? (
                <>
                  <div className="skill-tags">
                    {analysis.missingSkills.map((skill, i) => (
                      <span key={i} className="skill-tag warning">{skill}</span>
                    ))}
                  </div>
                  
                  <div className="learning-resources">
                    <h5>Recommended Learning Resources:</h5>
                    <ul>
                      {analysis.missingSkills.slice(0, 5).map(skill => (
                        <li key={skill}>
                          <a 
                            href={`https://www.coursera.org/search?query=${encodeURIComponent(skill)}`} 
                            target="_blank" 
                            rel="noopener noreferrer"
                          >
                            {skill} on Coursera
                          </a>
                          {' | '}
                          <a 
                            href={`https://www.udemy.com/courses/search/?q=${encodeURIComponent(skill)}`}
                            target="_blank" 
                            rel="noopener noreferrer"
                          >
                            Udemy
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                </>
              ) : (
                <p className="great-match">You already have all required skills! 🎉</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SkillGapAnalysis;
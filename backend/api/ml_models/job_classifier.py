# backend/api/ml_models/job_classifier.py

import re

class JobQueryClassifier:
    """
    Classifies if a query is job-related and identifies the specific category
    """
    
    # Job-related keywords by category
    JOB_CATEGORIES = {
        'resume': [
            'resume', 'cv', 'curriculum vitae', 'cover letter', 'application',
            'write resume', 'format resume', 'resume tips', 'resume building',
            'resume review', 'resume template', 'ats', 'applicant tracking'
        ],
        
        'interview': [
            'interview', 'interview question', 'interview preparation',
            'interview tips', 'behavioral question', 'technical interview',
            'hr interview', 'mock interview', 'interview feedback',
            'phone screen', 'video interview', 'interview advice'
        ],
        
        'salary': [
            'salary', 'compensation', 'pay', 'negotiation', 'raise',
            'salary expectation', 'salary range', 'benefits', 'package',
            'total compensation', 'equity', 'stock options', 'bonus'
        ],
        
        'career_path': [
            'career path', 'career growth', 'promotion', 'advancement',
            'career change', 'switch career', 'job transition', 'next role',
            'career development', 'professional development', 'upskill',
            'learning path', 'certification', 'career advice'
        ],
        
        'job_search': [
            'job search', 'find job', 'apply job', 'job hunting',
            'job market', 'job board', 'company research', 'target company',
            'remote job', 'hybrid work', 'work from home', 'job offer',
            'accept offer', 'reject offer', 'counter offer'
        ],
        
        'networking': [
            'networking', 'linkedin', 'professional network', 'connection',
            'referral', 'informational interview', 'career fair',
            'industry event', 'conference', 'meetup', 'alumni'
        ],
        
        'workplace': [
            'workplace', 'office culture', 'work environment', 'team dynamics',
            'work-life balance', 'burnout', 'stress management', 'productivity',
            'time management', 'remote work', 'hybrid work', 'manager',
            'colleague', 'conflict resolution', 'feedback'
        ]
    }
    
    # Generic job keywords (if any match, it's job-related)
    GENERIC_JOB_KEYWORDS = [
        'job', 'career', 'work', 'employ', 'hire', 'company', 'profession',
        'occupation', 'vocation', 'position', 'role', 'opportunity',
        'recruiter', 'hiring', 'staff', 'team', 'office', 'workplace'
    ]
    
    def classify(self, query):
        """
        Classify query into job category or return None if not job-related
        """
        query_lower = query.lower()
        
        # Check each category
        matches = []
        for category, keywords in self.JOB_CATEGORIES.items():
            for keyword in keywords:
                if keyword in query_lower:
                    matches.append(category)
                    break
        
        # If no category matches, check generic keywords
        if not matches:
            for keyword in self.GENERIC_JOB_KEYWORDS:
                if keyword in query_lower:
                    matches.append('general')
                    break
        
        # Return classification
        if matches:
            return {
                'is_job_related': True,
                'categories': list(set(matches)),  # Unique categories
                'primary_category': matches[0] if matches else None
            }
        else:
            return {
                'is_job_related': False,
                'categories': [],
                'primary_category': None
            }
    
    def extract_entities(self, query):
        """
        Extract job-related entities like roles, skills, companies
        """
        query_lower = query.lower()
        
        # Common job roles
        job_roles = [
            'software engineer', 'developer', 'data scientist', 'product manager',
            'project manager', 'designer', 'ux designer', 'ui designer',
            'marketing', 'sales', 'hr', 'recruiter', 'accountant',
            'financial analyst', 'consultant', 'architect', 'devops',
            'system administrator', 'network engineer', 'security analyst'
        ]
        
        # Common skills
        skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'django', 'flask', 'spring', 'node.js', 'express', 'sql',
            'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'excel', 'tableau', 'power bi', 'r', 'spss', 'sas',
            'communication', 'leadership', 'teamwork', 'problem solving'
        ]
        
        # Extract roles
        found_roles = []
        for role in job_roles:
            if role in query_lower:
                found_roles.append(role)
        
        # Extract skills
        found_skills = []
        for skill in skills:
            if skill in query_lower:
                found_skills.append(skill)
        
        return {
            'roles': found_roles,
            'skills': found_skills
        }
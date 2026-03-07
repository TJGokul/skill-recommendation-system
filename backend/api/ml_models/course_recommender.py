import json

class CourseRecommender:
    def __init__(self):
        self.course_database = {
            'python': [
                {'name': 'Complete Python Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/complete-python-bootcamp/', 'duration': '20 hours', 'level': 'Beginner'},
                {'name': 'Python for Data Science', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/python-data-science', 'duration': '30 hours', 'level': 'Intermediate'},
                {'name': 'Advanced Python', 'platform': 'Pluralsight', 'url': 'https://www.pluralsight.com/courses/advanced-python', 'duration': '15 hours', 'level': 'Advanced'}
            ],
            'javascript': [
                {'name': 'JavaScript: The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/javascript-the-complete-guide/', 'duration': '25 hours', 'level': 'Beginner'},
                {'name': 'Advanced JavaScript', 'platform': 'Frontend Masters', 'url': 'https://frontendmasters.com/courses/advanced-javascript/', 'duration': '20 hours', 'level': 'Advanced'}
            ],
            'react': [
                {'name': 'React - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/react-the-complete-guide/', 'duration': '40 hours', 'level': 'Beginner'},
                {'name': 'Modern React with Redux', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/react-redux/', 'duration': '35 hours', 'level': 'Intermediate'}
            ],
            'django': [
                {'name': 'Django for Beginners', 'platform': 'Django for Beginners', 'url': 'https://djangoforbeginners.com/', 'duration': '15 hours', 'level': 'Beginner'},
                {'name': 'Django REST Framework', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/django-python-rest-framework/', 'duration': '20 hours', 'level': 'Intermediate'}
            ],
            'java': [
                {'name': 'Java Programming Masterclass', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/java-the-complete-java-developer-course/', 'duration': '50 hours', 'level': 'Beginner'},
                {'name': 'Spring Framework', 'platform': 'Pluralsight', 'url': 'https://www.pluralsight.com/courses/spring-framework', 'duration': '25 hours', 'level': 'Intermediate'}
            ],
            'sql': [
                {'name': 'SQL for Data Science', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/sql-for-data-science', 'duration': '15 hours', 'level': 'Beginner'},
                {'name': 'Advanced SQL', 'platform': 'Pluralsight', 'url': 'https://www.pluralsight.com/courses/advanced-sql', 'duration': '10 hours', 'level': 'Advanced'}
            ],
            'aws': [
                {'name': 'AWS Certified Solutions Architect', 'platform': 'A Cloud Guru', 'url': 'https://acloudguru.com/course/aws-certified-solutions-architect', 'duration': '40 hours', 'level': 'Intermediate'},
                {'name': 'AWS for Beginners', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/aws-certified/', 'duration': '30 hours', 'level': 'Beginner'}
            ],
            'docker': [
                {'name': 'Docker Mastery', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/docker-mastery/', 'duration': '20 hours', 'level': 'Beginner'},
                {'name': 'Kubernetes for Developers', 'platform': 'Pluralsight', 'url': 'https://www.pluralsight.com/courses/kubernetes-developers', 'duration': '15 hours', 'level': 'Intermediate'}
            ],
            'communication': [
                {'name': 'Effective Communication Skills', 'platform': 'LinkedIn Learning', 'url': 'https://www.linkedin.com/learning/effective-communication', 'duration': '5 hours', 'level': 'Beginner'},
                {'name': 'Public Speaking', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/public-speaking', 'duration': '10 hours', 'level': 'Intermediate'}
            ],
            'leadership': [
                {'name': 'Leadership Principles', 'platform': 'Harvard Online', 'url': 'https://online.hbs.edu/courses/leadership-principles/', 'duration': '15 hours', 'level': 'Intermediate'},
                {'name': 'Team Management', 'platform': 'LinkedIn Learning', 'url': 'https://www.linkedin.com/learning/team-management', 'duration': '8 hours', 'level': 'Beginner'}
            ]
        }
        
        # Popular job roles and their required skills
        self.job_role_skills = {
            'Frontend Developer': ['javascript', 'react', 'css', 'html'],
            'Backend Developer': ['python', 'java', 'django', 'sql'],
            'Full Stack Developer': ['javascript', 'react', 'python', 'django', 'sql'],
            'Data Scientist': ['python', 'sql', 'machine learning', 'statistics'],
            'DevOps Engineer': ['aws', 'docker', 'kubernetes', 'jenkins'],
            'Cloud Architect': ['aws', 'azure', 'gcp', 'docker'],
            'Project Manager': ['leadership', 'communication', 'management', 'agile']
        }
    
    def get_course_recommendations(self, skills_list, target_role=None):
        """Get course recommendations based on current skills"""
        
        # Extract skill names from skills list
        current_skills = [skill['name'].lower() if isinstance(skill, dict) else skill.lower() 
                         for skill in skills_list]
        
        recommendations = []
        
        # If target role is specified, recommend missing skills for that role
        if target_role and target_role in self.job_role_skills:
            required_skills = self.job_role_skills[target_role]
            missing_skills = [skill for skill in required_skills if skill not in current_skills]
            
            for skill in missing_skills:
                if skill in self.course_database:
                    recommendations.extend(self.course_database[skill])
        
        # Also recommend advanced courses for current skills
        for skill in current_skills:
            if skill in self.course_database:
                # Get intermediate/advanced courses for existing skills
                advanced_courses = [course for course in self.course_database[skill] 
                                  if course['level'] in ['Intermediate', 'Advanced']]
                recommendations.extend(advanced_courses[:2])  # Limit to 2 per skill
        
        # Remove duplicates (by course name)
        unique_recommendations = []
        seen = set()
        for course in recommendations:
            if course['name'] not in seen:
                seen.add(course['name'])
                unique_recommendations.append(course)
        
        return unique_recommendations[:10]  # Return top 10 recommendations
    
    def get_skill_gap_analysis(self, skills_list, target_jobs=None):
        """Analyze skill gaps for target jobs"""
        
        current_skills = [skill['name'].lower() if isinstance(skill, dict) else skill.lower() 
                         for skill in skills_list]
        
        if not target_jobs:
            # If no target jobs specified, use all common roles
            target_jobs = list(self.job_role_skills.keys())[:5]  # Top 5 roles
        
        analysis = []
        
        for job_role in target_jobs[:5]:  # Limit to 5 roles
            if job_role in self.job_role_skills:
                required = self.job_role_skills[job_role]
                current = [skill for skill in required if skill in current_skills]
                missing = [skill for skill in required if skill not in current_skills]
                
                match_percentage = (len(current) / len(required)) * 100 if required else 0
                
                analysis.append({
                    'role': job_role,
                    'match_percentage': round(match_percentage, 1),
                    'current_skills': current,
                    'missing_skills': missing,
                    'required_skills': required
                })
        
        # Sort by match percentage (highest first)
        analysis.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return analysis
import os
import google.generativeai as genai
from django.conf import settings
import json

class AISkillRecommender:
    """
    AI-Powered Skill Recommendation using Gemini/OpenAI
    Provides personalized recommendations based on resume content and market trends
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        print(f"🤖 AI Recommender initialized: {bool(self.api_key)}")
    
    def get_recommendations(self, resume_text, current_skills, career_goal=None):
        """
        Get AI-powered skill recommendations based on resume analysis
        """
        if not self.api_key:
            print("⚠️ No API key, using fallback recommendations")
            return self._get_fallback_recommendations(current_skills)
        
        try:
            # Build prompt for AI
            prompt = self._build_prompt(resume_text, current_skills, career_goal)
            
            # Get AI response
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            recommendations = self._parse_ai_response(response.text)
            
            return recommendations
            
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return self._get_fallback_recommendations(current_skills)
    
    def _build_prompt(self, resume_text, current_skills, career_goal):
        """Build prompt for AI"""
        skills_str = ', '.join(current_skills[:10])
        
        prompt = f"""
        You are an expert career counselor and skill advisor. Analyze this resume and provide personalized skill recommendations.

        RESUME CONTENT:
        {resume_text[:2000]}

        CURRENT SKILLS DETECTED:
        {skills_str}

        CAREER GOAL: {career_goal if career_goal else 'Not specified'}

        Based on the resume, identify:
        1. The user's current profession/domain (e.g., Software Developer, Chemical Engineer, IT Support)
        2. 8-10 skills they should learn next to advance their career
        3. Market demand score for each skill (0-100)
        4. Estimated learning time in hours
        5. Category (programming, framework, database, cloud, chemical, mechanical, soft_skill, etc.)

        Return ONLY a JSON object with this exact structure:
        {{
            "detected_domain": "string",
            "recommendations": [
                {{
                    "name": "Skill Name",
                    "demand": 95,
                    "time": 60,
                    "category": "category_name",
                    "matchScore": 85,
                    "reason": "Why this skill is recommended"
                }}
            ]
        }}

        Make recommendations relevant to their current domain. For example:
        - Chemical Engineer: Process simulation, ASPEN Plus, Heat Transfer, Reaction Engineering
        - IT Support: Active Directory, Linux, Networking, CompTIA A+
        - Software Developer: Specific frameworks, cloud, databases based on their stack
        """
        
        return prompt
    
    def _parse_ai_response(self, response_text):
        """Parse AI response into structured recommendations"""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                # Format recommendations
                recommendations = []
                for rec in data.get('recommendations', []):
                    recommendations.append({
                        'name': rec.get('name', 'Unknown'),
                        'demand': rec.get('demand', 85),
                        'time': rec.get('time', 50),
                        'category': rec.get('category', 'general'),
                        'matchScore': rec.get('matchScore', 80),
                        'reason': rec.get('reason', '')
                    })
                
                return {
                    'domain': data.get('detected_domain', 'General'),
                    'recommendations': recommendations
                }
        except Exception as e:
            print(f"❌ Parse error: {e}")
        
        return self._get_fallback_recommendations([])
    
    def _get_fallback_recommendations(self, current_skills):
        """Fallback recommendations if AI fails"""
        # Domain detection from current skills
        skill_str = ' '.join(current_skills).lower()
        
        if any(s in skill_str for s in ['chemical', 'process', 'reactor', 'chemistry']):
            domain = 'Chemical Engineering'
            recommendations = [
                {'name': 'ASPEN Plus', 'demand': 85, 'time': 60, 'category': 'chemical', 'matchScore': 90},
                {'name': 'Process Design', 'demand': 88, 'time': 70, 'category': 'chemical', 'matchScore': 92},
                {'name': 'Heat Transfer', 'demand': 84, 'time': 50, 'category': 'chemical', 'matchScore': 88},
                {'name': 'Reaction Engineering', 'demand': 82, 'time': 65, 'category': 'chemical', 'matchScore': 86},
                {'name': 'Fluid Mechanics', 'demand': 83, 'time': 55, 'category': 'chemical', 'matchScore': 85}
            ]
        elif any(s in skill_str for s in ['support', 'help desk', 'troubleshoot', 'windows']):
            domain = 'IT Support'
            recommendations = [
                {'name': 'Active Directory', 'demand': 86, 'time': 35, 'category': 'itsupport', 'matchScore': 92},
                {'name': 'Linux Administration', 'demand': 88, 'time': 60, 'category': 'itsupport', 'matchScore': 90},
                {'name': 'Networking Basics', 'demand': 89, 'time': 40, 'category': 'itsupport', 'matchScore': 91},
                {'name': 'CompTIA A+', 'demand': 87, 'time': 80, 'category': 'itsupport', 'matchScore': 89},
                {'name': 'Windows Server', 'demand': 85, 'time': 55, 'category': 'itsupport', 'matchScore': 88}
            ]
        else:
            domain = 'Software Development'
            recommendations = [
                {'name': 'Python', 'demand': 95, 'time': 60, 'category': 'programming', 'matchScore': 90},
                {'name': 'JavaScript', 'demand': 98, 'time': 50, 'category': 'programming', 'matchScore': 95},
                {'name': 'React', 'demand': 96, 'time': 45, 'category': 'frameworks', 'matchScore': 92},
                {'name': 'SQL', 'demand': 94, 'time': 40, 'category': 'databases', 'matchScore': 88},
                {'name': 'AWS', 'demand': 94, 'time': 80, 'category': 'cloud', 'matchScore': 85}
            ]
        
        return {
            'domain': domain,
            'recommendations': recommendations[:8]
        }
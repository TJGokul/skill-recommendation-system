import os
from freeflow_llm import FreeFlowClient, NoProvidersAvailableError
import google.generativeai as genai

class FreeAICareerService:
    def __init__(self):
        # You can get these keys for free from the links above
        self.groq_key = os.getenv('GROQ_API_KEY', '')
        self.gemini_key = os.getenv('GEMINI_API_KEY', '')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
        
        # Initialize FreeFlow client (auto-falls back between providers)
        self.client = FreeFlowClient()
        
        # Also setup Gemini directly as backup
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_career_advice(self, question, user_skills=None, experience=None):
        """Get AI-powered career advice for any question"""
        
        # Build context about the user
        context = ""
        if user_skills:
            skills_list = [s['name'] if isinstance(s, dict) else s for s in user_skills]
            context += f"User has skills in: {', '.join(skills_list)}. "
        if experience:
            context += f"Experience: {experience} years. "
        
        # Create prompt with context
        prompt = f"""You are a helpful career advisor. {context}
        
User question: {question}

Provide practical, actionable advice. Be encouraging but realistic. 
If they ask about specific jobs, suggest roles that match their skills.
If they ask about learning, recommend specific courses or skills.
Keep response to 3-4 sentences maximum.
"""
        
        # Try multiple providers automatically
        try:
            # Try FreeFlow first (chains multiple providers)
            response = self.client.chat(
                messages=[
                    {"role": "system", "content": "You are a career counselor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response.content
            
        except NoProvidersAvailableError:
            # Fallback to direct Gemini if FreeFlow fails
            if hasattr(self, 'gemini_model'):
                gemini_response = self.gemini_model.generate_content(prompt)
                return gemini_response.text
            
            # Last resort fallback
            return self._get_fallback_response(question)
    
    def _get_fallback_response(self, question):
        """Friendly fallback when AI is unavailable"""
        responses = {
            "mnc": "To join an MNC, focus on building strong technical skills, create a portfolio, practice interview questions, and network on LinkedIn. Many MNCs also value freshers with internship experience.",
            "salary": "Entry-level salaries in tech vary by location and role. In India, freshers can expect ₹3-8 LPA. In the US, $60-85k. Research on Glassdoor for specific companies.",
            "skills": "Based on your profile, consider learning in-demand skills like React, Python, Cloud (AWS), or Data Science. Check Coursera for structured learning paths."
        }
        
        # Simple keyword matching
        for key, answer in responses.items():
            if key in question.lower():
                return answer
        
        return "I'd be happy to help with your career question! Please try again or ask something specific about jobs, skills, or companies."
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class JobRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def create_job_profile(self, job):
        profile = f"{job.title} {job.description} {job.requirements}"
        return profile.lower()
    
    def create_seeker_profile(self, job_seeker):
        profile = f"{job_seeker.education}"
        return profile.lower()
    
    def calculate_match_score(self, seeker_profile, job_profile):
        try:
            documents = [seeker_profile, job_profile]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0] * 100)
        except Exception as e:
            print(f"Error calculating match score: {e}")
            return 0
    
    def recommend_jobs(self, job_seeker_id, top_n=10):
        try:
            from ..models import JobSeeker, Job
            
            job_seeker = JobSeeker.objects.get(id=job_seeker_id)
            jobs = Job.objects.all()
        except Exception as e:
            print(f"Error in recommend_jobs: {e}")
            return []
            
        seeker_profile = self.create_seeker_profile(job_seeker)
        
        recommendations = []
        
        for job in jobs:
            job_profile = self.create_job_profile(job)
            match_score = self.calculate_match_score(seeker_profile, job_profile)
            
            # Simple skill match calculation
            skill_match = 50  # Default value
            
            if match_score > 10:
                recommendations.append({
                    'job_id': job.id,
                    'job_title': job.title,
                    'company': job.company,
                    'match_score': round(match_score, 2),
                    'skill_match_percentage': round(skill_match, 2),
                    'location': job.location
                })
        
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]
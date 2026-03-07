from django.db import models
from django.contrib.auth.models import User
import json

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    education = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Resume(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_data = models.JSONField(default=dict)
    
    def __str__(self):
        return f"Resume {self.id}"

class JobSeekerSkill(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.IntegerField(default=3)  # 1-5 scale
    years_experience = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['job_seeker', 'skill']

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    employment_type = models.CharField(max_length=50)
    posted_date = models.DateTimeField(auto_now_add=True)
    skills_required = models.ManyToManyField(Skill, through='JobSkill')
    
    def __str__(self):
        return f"{self.title} at {self.company}"

class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.IntegerField(default=3)  # 1-5 scale
    
    class Meta:
        unique_together = ['job', 'skill']

class JobRecommendation(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    match_score = models.FloatField()
    skill_match_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['job_seeker', 'job']
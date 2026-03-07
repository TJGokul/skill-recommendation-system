from django.contrib import admin
from .models import JobSeeker, Skill, Resume, JobSeekerSkill, Job, JobSkill, JobRecommendation

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'location', 'experience_years', 'created_at')
    search_fields = ('user__username', 'phone', 'location')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_seeker', 'uploaded_at')
    search_fields = ('job_seeker__user__username',)

@admin.register(JobSeekerSkill)
class JobSeekerSkillAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'skill', 'proficiency', 'years_experience')
    search_fields = ('job_seeker__user__username', 'skill__name')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location', 'employment_type', 'posted_date')
    search_fields = ('title', 'company', 'location')
    list_filter = ('employment_type', 'location')

@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('job', 'skill', 'importance')
    search_fields = ('job__title', 'skill__name')

@admin.register(JobRecommendation)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job', 'match_score', 'skill_match_percentage', 'created_at')
    search_fields = ('job_seeker__user__username', 'job__title')
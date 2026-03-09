from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('test/', views.test_api, name='test-api'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.get_current_user, name='current-user'),
    path('upload-resume/', views.upload_resume, name='upload-resume'),
    path('recommendations/<int:job_seeker_id>/', views.get_job_recommendations, name='job-recommendations'),
    path('jobs/', views.get_jobs, name='jobs'),
    path('skills/', views.get_skills, name='skills'),
    path('job-seeker/', views.create_job_seeker, name='create-job-seeker'),
    path('course-recommendations/', views.get_course_recommendations, name='course-recommendations'),
    path('skill-gap-analysis/', views.get_skill_gap_analysis, name='skill-gap-analysis'),
    path('analyze-role/', views.analyze_role, name='analyze-role'),
    path('free-ai-advice/', views.free_ai_advice, name='free-ai-advice'),
    path('search-live-jobs/', views.search_live_jobs, name='search-live-jobs'),
    path('get-live-jobs/', views.get_live_jobs, name='get-live-jobs'),
    path('latest-resume/', views.latest_resume, name='latest-resume'),
    path('skill-recommendations/', views.get_skill_recommendations, name='skill-recommendations'),
    re_path(r'^register$', views.register, name='register-no-slash'),
    re_path(r'^login$', views.login_view, name='login-no-slash'),
    re_path(r'^logout$', views.logout_view, name='logout-no-slash'),
    re_path(r'^user$', views.get_current_user, name='user-no-slash'),
]
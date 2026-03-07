from rest_framework import serializers
from .models import *

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    skills_required = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'

class JobRecommendationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    
    class Meta:
        model = JobRecommendation
        fields = '__all__'
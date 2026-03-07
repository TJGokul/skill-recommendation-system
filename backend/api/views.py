from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from google import generativeai as genai
from .job_service import JobSearchService
from .ml_models.skill_recommender import SkillRecommender
from .ml_models.ai_skill_recommender import AISkillRecommender
import traceback
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

from .models import *
from .serializers import *
from .ml_models.resume_parser import ImprovedResumeParser as ResumeParser
from .ml_models.job_recommender import JobRecommender
from .ml_models.course_recommender import CourseRecommender

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API key loaded successfully")
else:
    print("⚠️ WARNING: GEMINI_API_KEY not set. AI features will not work.")

# Initialize ML models
parser = ResumeParser()
recommender = JobRecommender()
course_recommender = CourseRecommender()
job_search_service = JobSearchService()
skill_recommender = SkillRecommender()
ai_recommender = AISkillRecommender()

# Helper function to get CSRF token
def get_csrf_token(request):
    from django.middleware.csrf import get_token
    return get_token(request)

# Test API endpoint
@api_view(['GET'])
def test_api(request):
    return Response({
        'message': 'API is working!',
        'status': 'success',
        'endpoints': {
            'test': '/api/test/',
            'register': '/api/register/',
            'login': '/api/login/',
            'logout': '/api/logout/',
            'user': '/api/user/',
            'upload_resume': '/api/upload-resume/',
            'recommendations': '/api/recommendations/<job_seeker_id>/',
            'jobs': '/api/jobs/',
            'skills': '/api/skills/',
            'job_seeker': '/api/job-seeker/',
            'course_recommendations': '/api/course-recommendations/',
            'skill_gap_analysis': '/api/skill-gap-analysis/',
            'free_ai_advice': '/api/free-ai-advice/',
            'analyze_role': '/api/analyze-role/'
        }
    })

@api_view(['POST'])
def register(request):
    """Register a new user"""
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        phone = request.data.get('phone', '')
        location = request.data.get('location', '')
        experience_years = request.data.get('experience_years', 0)
        education = request.data.get('education', '')
        
        # Validate required fields
        if not username or not email or not password:
            return Response({
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create JobSeeker profile
        job_seeker = JobSeeker.objects.create(
            user=user,
            phone=phone,
            location=location,
            experience_years=experience_years if experience_years else 0,
            education=education
        )
        
        # Log the user in
        login(request, user)
        
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'job_seeker_id': job_seeker.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    """Login user"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Get or create job seeker profile
            job_seeker, created = JobSeeker.objects.get_or_create(
                user=user,
                defaults={
                    'phone': '',
                    'location': '',
                    'experience_years': 0,
                    'education': ''
                }
            )
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'job_seeker_id': job_seeker.id
            })
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    """Logout user"""
    try:
        logout(request)
        response = Response({'message': 'Logout successful'})
        
        # Clear cookies
        response.delete_cookie('csrftoken')
        response.delete_cookie('sessionid')
        
        return response
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_current_user(request):
    """Get currently logged in user"""
    if request.user.is_authenticated:
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            return Response({
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name
                },
                'job_seeker_id': job_seeker.id,
                'phone': job_seeker.phone,
                'location': job_seeker.location,
                'experience_years': job_seeker.experience_years,
                'education': job_seeker.education
            })
        except JobSeeker.DoesNotExist:
            return Response({
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name
                }
            })
    return Response({'user': None})

@api_view(['POST'])
def upload_resume(request):
    """Upload and parse resume"""
    try:
        if 'resume' not in request.FILES:
            return Response({'error': 'No resume file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        resume_file = request.FILES['resume']
        print(f"📄 Received file: {resume_file.name}, Size: {resume_file.size} bytes")
        
        # Validate file type
        if not resume_file.name.endswith(('.pdf', '.docx')):
            return Response({'error': 'Only PDF and DOCX files are supported'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(settings.BASE_DIR, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save file temporarily
        file_path = default_storage.save(f'temp/{resume_file.name}', ContentFile(resume_file.read()))
        full_path = default_storage.path(file_path)
        print(f"💾 File saved to: {full_path}")
        
        # Check if file exists
        if not os.path.exists(full_path):
            return Response({'error': 'File could not be saved'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Parse resume
        print("🔍 Calling parser.parse_resume...")
        parsed_data = parser.parse_resume(full_path)
        print(f"✅ Parse successful: Found skills in {len(parsed_data.get('skills', {}).get('by_category', {}))} categories")
        
        # Save resume record
        resume = Resume.objects.create(
            file=resume_file,
            parsed_data=parsed_data
        )
        print(f"✅ Resume saved with ID: {resume.id}")
        
        # If user is authenticated, associate resume with them
        if request.user.is_authenticated:
            try:
                job_seeker = JobSeeker.objects.get(user=request.user)
                resume.job_seeker = job_seeker
                resume.save()
                print(f"✅ Resume associated with user: {request.user.username}")
            except JobSeeker.DoesNotExist:
                print("⚠️ JobSeeker not found for user")
        
        # Clean up temp file
        if os.path.exists(full_path):
            os.remove(full_path)
            print("🧹 Temp file deleted")
        
        return Response({
            'message': 'Resume parsed successfully',
            'resume_id': resume.id,
            'parsed_data': parsed_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ ERROR in upload_resume: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        
        # Clean up temp file if it exists
        try:
            if 'full_path' in locals() and os.path.exists(full_path):
                os.remove(full_path)
        except:
            pass
        
        return Response({'error': f'Error uploading resume: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_job_recommendations(request, job_seeker_id):
    """Get job recommendations for a job seeker"""
    try:
        recommendations = recommender.recommend_jobs(job_seeker_id)
        return Response(recommendations)
    except Exception as e:
        print(f"Error in get_job_recommendations: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_jobs(request):
    """Get all jobs"""
    try:
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_jobs: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_skills(request):
    """Get all skills"""
    try:
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_skills: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_job_seeker(request):
    """Create a job seeker profile"""
    serializer = JobSeekerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_course_recommendations(request):
    """Get course recommendations based on skills"""
    try:
        skills = request.data.get('skills', [])
        target_role = request.data.get('target_role', None)
        
        recommendations = course_recommender.get_course_recommendations(skills, target_role)
        
        return Response({
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error in get_course_recommendations: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_skill_gap_analysis(request):
    """Get skill gap analysis for job roles"""
    try:
        skills = request.data.get('skills', [])
        target_jobs = request.data.get('target_jobs', None)
        
        analysis = course_recommender.get_skill_gap_analysis(skills, target_jobs)
        
        return Response({
            'analysis': analysis
        })
    except Exception as e:
        print(f"Error in get_skill_gap_analysis: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def analyze_role(request):
    """Analyze skills for a specific role"""
    try:
        role = request.data.get('role', '')
        skills = request.data.get('skills', [])
        
        if not role:
            return Response({'error': 'Role is required'}, status=400)
        
        # Extract skill names
        skill_names = []
        for s in skills:
            if isinstance(s, dict):
                skill_names.append(s.get('name', '').lower())
            else:
                skill_names.append(str(s).lower())
        
        # Define role-skill mappings
        role_skills = {
            'frontend': ['javascript', 'react', 'html', 'css', 'typescript', 'angular', 'vue'],
            'backend': ['python', 'java', 'sql', 'django', 'node.js', 'spring', 'c#'],
            'full stack': ['javascript', 'react', 'python', 'sql', 'node.js', 'django', 'html', 'css'],
            'data scientist': ['python', 'sql', 'machine learning', 'statistics', 'pandas', 'r', 'tensorflow'],
            'data analyst': ['sql', 'excel', 'tableau', 'python', 'power bi', 'statistics'],
            'devops': ['docker', 'kubernetes', 'aws', 'jenkins', 'linux', 'terraform', 'ci/cd'],
            'cloud': ['aws', 'azure', 'gcp', 'terraform', 'networking', 'docker'],
            'mobile': ['swift', 'kotlin', 'react native', 'flutter', 'android', 'ios'],
            'product manager': ['agile', 'scrum', 'market research', 'analytics', 'communication', 'leadership'],
            'qa': ['selenium', 'test automation', 'jira', 'manual testing', 'python', 'cypress'],
            'ux/ui': ['figma', 'sketch', 'adobe xd', 'user research', 'prototyping', 'wireframing']
        }
        
        # Find matching role category
        role_lower = role.lower()
        matched_category = None
        for key in role_skills:
            if key in role_lower:
                matched_category = key
                break
        
        required = role_skills.get(matched_category, [])
        
        if not required:
            # Generic skills for unknown roles
            required = ['problem solving', 'communication', 'teamwork', 'adaptability', 'critical thinking']
        
        # Calculate matches
        matched = [s for s in required if s in skill_names]
        missing = [s for s in required if s not in skill_names]
        match_score = (len(matched) / len(required)) * 100 if required else 0
        
        return Response({
            'role': role,
            'requiredSkills': required,
            'matchedSkills': matched,
            'missingSkills': missing,
            'matchScore': round(match_score)
        })
        
    except Exception as e:
        print(f"Error in analyze_role: {str(e)}")
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def free_ai_advice(request):
    """Get free AI career advice using Google Gemini"""
    try:
        question = request.data.get('question', '')
        skills = request.data.get('skills', [])
        experience = request.data.get('experience', 0)
        
        if not question:
            return Response({'error': 'Question is required'}, status=400)
        
        # Check if API key is configured
        if not GEMINI_API_KEY:
            return Response({
                'answer': "AI features are not configured. Please set up your Gemini API key in the .env file. Get a free key from https://aistudio.google.com"
            })
        
        # Build context about the user
        context = ""
        if skills and len(skills) > 0:
            skill_names = []
            for s in skills:
                if isinstance(s, dict):
                    skill_names.append(s.get('name', ''))
                else:
                    skill_names.append(s)
            if skill_names:
                context += f"The user has skills in: {', '.join(skill_names[:5])}. "
        if experience:
            context += f"They have {experience} years of experience. "
        
        # Create prompt for Gemini
        prompt = f"""You are a helpful, friendly career advisor. {context}

The user asks: "{question}"

Provide practical, actionable advice. Be encouraging and specific. 
If they ask about MNCs, suggest companies and preparation strategies.
If they ask about skills, recommend specific technologies and learning resources.
If they ask about salary, give realistic ranges based on experience.
If they ask about interviews, share tips and common questions.

Keep your response to 3-4 sentences, friendly and professional."""
        
        print(f"Calling Gemini API with key: {GEMINI_API_KEY[:10]}...")
        
        # Use Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        print("✅ Gemini API call successful!")
        
        return Response({
            'question': question,
            'answer': response.text,
            'provider': 'gemini-1.5-flash'
        })
        
    except Exception as e:
        # Print detailed error for debugging
        print(f"❌ AI Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        
        # User-friendly error message
        error_message = "I'm having trouble connecting right now. "
        if "API key" in str(e).lower():
            error_message = "There's an issue with the API key configuration. "
        elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
            error_message = "We've reached the API rate limit. Please try again later. "
        elif "model" in str(e).lower():
            error_message = "The AI model is temporarily unavailable. "
            
        return Response({
            'answer': error_message + "Please try again in a few moments."
        }, status=200)
    
# backend/api/views.py - Add this function

@api_view(['POST'])
def search_live_jobs(request):
    """
    Get 6+ job recommendations guaranteed for ANY resume
    """
    try:
        skills = request.data.get('skills', [])
        location = request.data.get('location', '')
        
        print(f"🔍 Searching jobs for: {skills[:3]}")
        
        from .job_service import JobSearchService
        service = JobSearchService()
        jobs = service.search_by_skills(skills, location)
        
        return Response({
            'jobs': jobs,
            'count': len(jobs),
            'source': 'AI Matched'
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return Response({'jobs': [], 'count': 0})
    
@api_view(['GET'])
def get_live_jobs(request):
    """Get live jobs with search query"""
    try:
        query = request.GET.get('q', 'developer')
        location = request.GET.get('location', '')
        
        jobs = job_search_service.search_jobs(query, location)
        
        return Response({
            'jobs': jobs,
            'count': len(jobs)
        })
        
    except Exception as e:
        print(f"Error in get_live_jobs: {e}")
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def latest_resume(request):
    """Get the latest resume for the current user"""
    try:
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        
        # Get job seeker profile
        job_seeker = JobSeeker.objects.get(user=request.user)
        
        # Get latest resume
        latest = Resume.objects.filter(job_seeker=job_seeker).order_by('-uploaded_at').first()
        
        if latest:
            return Response({
                'resume_id': latest.id,
                'parsed_data': latest.parsed_data,
                'uploaded_at': latest.uploaded_at
            })
        else:
            return Response({'message': 'No resume found'})
            
    except JobSeeker.DoesNotExist:
        return Response({'error': 'Job seeker profile not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def get_skill_recommendations(request):
    """
    Get personalized skill recommendations
    """
    try:
        skills = request.data.get('skills', [])
        career_goal = request.data.get('career_goal', '')
        
        recommendations = skill_recommender.get_recommendations(skills, career_goal)
        
        return Response({
            'status': 'success',
            'data': recommendations
        })
        
    except Exception as e:
        print(f"Error in skill recommendations: {e}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@api_view(['POST'])
def get_ai_skill_recommendations(request):
    """
    Get AI-powered skill recommendations based on resume
    """
    try:
        resume_text = request.data.get('resume_text', '')
        skills = request.data.get('skills', [])
        career_goal = request.data.get('career_goal', '')
        
        recommendations = ai_recommender.get_recommendations(resume_text, skills, career_goal)
        
        return Response({
            'status': 'success',
            'data': recommendations
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)
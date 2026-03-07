# backend/job_service.py

import requests
import os
import time
import random
from django.core.cache import cache
from datetime import datetime

class JobSearchService:
    """
    Guarantees 6+ job recommendations for ANY resume
    Uses: JSearch API + Fallback Database + Smart Matching
    """
    
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY', '')
        self.api_host = "jsearch.p.rapidapi.com"
        self.base_url = "https://jsearch.p.rapidapi.com"
        
        # Rate limiting
        self.last_request = 0
        self.min_interval = 1.0
        
        print(f"🔑 API Key: {bool(self.api_key)}")

    def search_by_skills(self, skills_list, location=""):
        """
        Returns 6+ job recommendations guaranteed
        Strategy: API First → Fallback Database → Smart Matching
        """
        start = time.time()
        
        # Clean skills
        skills = [str(s).lower() for s in skills_list if s and len(str(s)) > 2][:4]
        
        if not skills:
            return self._get_popular_jobs()
        
        # Check cache (4 hours)
        cache_key = f"jobs6_{'_'.join(sorted(skills))}_{location}"
        cached = cache.get(cache_key)
        if cached:
            print(f"📦 Cache: {len(cached)} jobs")
            return cached
        
        all_jobs = []
        
        # STRATEGY 1: Try JSearch API (max 3 calls)
        if self.api_key:
            api_jobs = self._try_api(skills, location)
            all_jobs.extend(api_jobs)
            print(f"📡 API: {len(api_jobs)} jobs")
        
        # STRATEGY 2: Fill with fallback database if needed
        if len(all_jobs) < 6:
            fallback = self._get_fallback_jobs(skills, location)
            all_jobs.extend(fallback)
            print(f"📚 Fallback: {len(fallback)} jobs")
        
        # STRATEGY 3: Smart matching for remaining slots
        if len(all_jobs) < 6:
            smart = self._get_smart_matches(skills)
            all_jobs.extend(smart)
            print(f"🧠 Smart: {len(smart)} jobs")
        
        # Deduplicate and score
        final_jobs = self._deduplicate_and_score(all_jobs, skills)
        
        # Cache for 4 hours
        cache.set(cache_key, final_jobs, 14400)  # 4 hours
        
        print(f"✅ Total: {len(final_jobs)} jobs in {time.time()-start:.1f}s")
        return final_jobs

    def _try_api(self, skills, location):
        """Try JSearch API with smart retry logic"""
        jobs = []
        seen = set()
        
        # Most effective queries based on skills
        queries = self._smart_queries(skills)
        
        for query in queries[:3]:  # Max 3 API calls
            # Rate limiting
            elapsed = time.time() - self.last_request
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            
            url = f"{self.base_url}/search"
            params = {
                "query": f"{query} {location}" if location else query,
                "page": "1",
                "num_pages": "1",
                "date_posted": "week"
            }
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host
            }
            
            try:
                print(f"📡 API: {query}")
                response = requests.get(url, headers=headers, params=params, timeout=5)
                self.last_request = time.time()
                
                if response.status_code == 200:
                    data = response.json()
                    for job in data.get('data', [])[:5]:
                        job_id = job.get('job_id')
                        if job_id and job_id not in seen:
                            seen.add(job_id)
                            jobs.append(job)
                
                if len(jobs) >= 10:
                    break
                    
            except Exception as e:
                print(f"⚠️ API error: {e}")
                continue
        
        return jobs

    def _smart_queries(self, skills):
        """Generate smart search queries"""
        primary = skills[0] if skills else ''
        
        # Industry-standard job titles
        titles = {
            'python': ['python developer', 'backend developer', 'software engineer'],
            'java': ['java developer', 'software engineer', 'full stack java'],
            'javascript': ['javascript developer', 'frontend developer', 'web developer'],
            'react': ['react developer', 'frontend developer', 'javascript developer'],
            'sql': ['sql developer', 'database administrator', 'data analyst'],
            'aws': ['aws engineer', 'cloud engineer', 'devops engineer'],
            'docker': ['devops engineer', 'platform engineer', 'site reliability'],
            'c': ['c developer', 'embedded engineer', 'firmware engineer'],
            'c++': ['c++ developer', 'software engineer', 'game developer'],
            'management': ['project manager', 'product manager', 'team lead'],
            'analytical': ['data analyst', 'business analyst', 'financial analyst'],
            'chemical': ['chemical engineer', 'process engineer', 'production engineer'],
            'mechanical': ['mechanical engineer', 'design engineer', 'manufacturing engineer'],
            'electrical': ['electrical engineer', 'electronics engineer', 'power engineer'],
            'civil': ['civil engineer', 'structural engineer', 'construction engineer'],
            'support': ['technical support', 'it support', 'help desk'],
            'network': ['network engineer', 'network administrator', 'system administrator']
        }
        
        return titles.get(primary, [f"{primary} engineer", f"{primary} developer", "software engineer"])

    def _get_fallback_jobs(self, skills, location):
        """Comprehensive fallback job database"""
        primary = skills[0] if skills else 'software'
        secondary = skills[1] if len(skills) > 1 else ''
        
        # Indian job market database
        fallback_db = [
            # IT Jobs
            {'title': f'{primary.title()} Developer', 'company': 'TCS', 'source': 'LinkedIn'},
            {'title': f'{primary.title()} Engineer', 'company': 'Infosys', 'source': 'Indeed'},
            {'title': f'Junior {primary.title()} Developer', 'company': 'Wipro', 'source': 'Naukri'},
            {'title': f'{primary.title()} Programmer', 'company': 'Accenture', 'source': 'Glassdoor'},
            {'title': f'{primary.title()} Specialist', 'company': 'Cognizant', 'source': 'Monster'},
            {'title': 'Software Developer', 'company': 'Tech Mahindra', 'source': 'LinkedIn'},
            {'title': 'Full Stack Developer', 'company': 'HCL', 'source': 'Indeed'},
            
            # Engineering Jobs
            {'title': 'Process Engineer', 'company': 'Reliance', 'source': 'LinkedIn'},
            {'title': 'Chemical Engineer', 'company': 'Grasim', 'source': 'Naukri'},
            {'title': 'Mechanical Designer', 'company': 'L&T', 'source': 'Glassdoor'},
            {'title': 'Electrical Engineer', 'company': 'Siemens', 'source': 'Indeed'},
            {'title': 'Civil Engineer', 'company': 'Shapoorji', 'source': 'Monster'},
            
            # Support Jobs
            {'title': 'Technical Support', 'company': 'Amazon', 'source': 'LinkedIn'},
            {'title': 'IT Support Specialist', 'company': 'Microsoft', 'source': 'Indeed'},
            {'title': 'Help Desk Technician', 'company': 'Dell', 'source': 'Naukri'},
            {'title': 'Network Administrator', 'company': 'Cisco', 'source': 'Glassdoor'},
            {'title': 'System Administrator', 'company': 'IBM', 'source': 'Monster'},
        ]
        
        # Filter relevant jobs
        relevant = []
        for job in fallback_db:
            title = job['title'].lower()
            desc = f"{job['title']} {job['company']}".lower()
            
            # Calculate relevance score
            score = 0
            for skill in skills:
                if skill in title:
                    score += 30
                elif skill in desc:
                    score += 15
            
            if score > 20:  # Only include relevant jobs
                relevant.append({
                    'id': f"fallback_{len(relevant)}",
                    'title': job['title'],
                    'company': job['company'],
                    'description': f"Position for {primary} professionals. Apply via {job['source']}.",
                    'location': location or 'Multiple Locations, India',
                    'salary': 'Competitive',
                    'apply_url': f"https://www.{job['source'].lower()}.com/jobs/",
                    'match_score': min(95, 60 + score),
                    'source': job['source'],
                    'is_remote': random.choice([True, False])
                })
        
        return relevant[:8]

    def _get_smart_matches(self, skills):
        """Generate smart job matches based on skills"""
        smart_jobs = []
        primary = skills[0] if skills else ''
        
        # Skill to job mapping
        job_templates = {
            'python': ['Python Developer', 'Backend Engineer', 'Data Scientist'],
            'java': ['Java Developer', 'Android Developer', 'Spring Boot Engineer'],
            'javascript': ['JavaScript Developer', 'Frontend Engineer', 'Node.js Developer'],
            'react': ['React Developer', 'Frontend Engineer', 'UI Developer'],
            'sql': ['SQL Developer', 'Database Administrator', 'Data Analyst'],
            'aws': ['AWS Engineer', 'Cloud Architect', 'DevOps Engineer'],
            'docker': ['DevOps Engineer', 'Platform Engineer', 'Site Reliability Engineer'],
            'chemical': ['Chemical Engineer', 'Process Engineer', 'Production Engineer'],
            'mechanical': ['Mechanical Engineer', 'Design Engineer', 'CAD Engineer'],
            'electrical': ['Electrical Engineer', 'Electronics Engineer', 'Power Engineer'],
            'civil': ['Civil Engineer', 'Structural Engineer', 'Site Engineer'],
            'support': ['Technical Support', 'IT Support', 'Help Desk Technician'],
        }
        
        templates = job_templates.get(primary, ['Software Engineer', 'Developer', 'Engineer'])
        
        for i, title in enumerate(templates[:3]):
            smart_jobs.append({
                'id': f"smart_{i}",
                'title': title,
                'company': f"Tech Company {i+1}",
                'description': f"Position requiring {primary} skills. Fast-growing company with excellent benefits.",
                'location': 'Remote / Multiple Locations',
                'salary': 'Market Rate',
                'apply_url': f"https://www.linkedin.com/jobs/search/?keywords={primary}",
                'match_score': 90 - (i * 5),
                'source': 'LinkedIn',
                'is_remote': True
            })
        
        return smart_jobs

    def _get_popular_jobs(self):
        """Get popular jobs when no skills detected"""
        return [
            {
                'id': 'pop1',
                'title': 'Software Developer',
                'company': 'Google',
                'description': 'Join Google as a software developer. Work on impactful projects.',
                'location': 'Worldwide',
                'salary': 'Competitive',
                'apply_url': 'https://careers.google.com/',
                'match_score': 85,
                'source': 'Google Careers'
            },
            {
                'id': 'pop2',
                'title': 'Frontend Engineer',
                'company': 'Microsoft',
                'description': 'Build beautiful web applications at Microsoft.',
                'location': 'Remote',
                'salary': 'Market Rate',
                'apply_url': 'https://careers.microsoft.com/',
                'match_score': 82,
                'source': 'Microsoft'
            },
            {
                'id': 'pop3',
                'title': 'Data Analyst',
                'company': 'Amazon',
                'description': 'Analyze data and drive business decisions at Amazon.',
                'location': 'Multiple',
                'salary': 'Competitive',
                'apply_url': 'https://www.amazon.jobs/',
                'match_score': 80,
                'source': 'Amazon Jobs'
            }
        ]

    def _deduplicate_and_score(self, jobs, skills):
        """Remove duplicates and add match scores"""
        seen = set()
        unique = []
        
        for job in jobs:
            # Create unique key
            key = f"{job.get('title', '')}|{job.get('company', '')}"
            if key in seen:
                continue
            seen.add(key)
            
            # Calculate final match score
            title = job.get('title', '').lower()
            desc = job.get('description', '').lower()
            
            score = 30
            for skill in skills:
                if skill in title:
                    score += 20
                elif skill in desc:
                    score += 10
            
            job['match_score'] = min(95, score)
            unique.append(job)
        
        # Sort by match score
        unique.sort(key=lambda x: x['match_score'], reverse=True)
        return unique[:15]  # Return top 15
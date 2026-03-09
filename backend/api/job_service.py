# backend/job_service.py

import requests
import os
import time
from django.core.cache import cache
from datetime import datetime

class JobSearchService:
    """
    Universal JSearch API integration - Works for ALL Industries
    Supports: Medical, Chemical, Electrical, Mechanical, Civil, IT, and more
    """
    
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY', '')
        self.api_host = "jsearch.p.rapidapi.com"
        self.base_url = "https://jsearch.p.rapidapi.com"
        
        # Rate limiting
        self.last_request = 0
        self.min_interval = 1.0
        
        print(f"🔑 JSearch API Key configured: {bool(self.api_key)}")

    def search_by_skills(self, skills_list, location=""):
        """
        Universal job search - Works for ANY industry
        """
        start = time.time()
        
        # Clean skills
        skills = [str(s).lower().strip() for s in skills_list if s and len(str(s)) > 1]
        
        if not skills:
            print("⚠️ No valid skills provided")
            return []
        
        print(f"🔍 Searching jobs for skills: {skills}")
        
        # Check cache
        cache_key = f"jsearch_universal_{'_'.join(sorted(skills))}_{location}"
        cached = cache.get(cache_key)
        if cached:
            print(f"📦 Cache hit: {len(cached)} jobs")
            return cached
        
        # Check API key
        if not self.api_key:
            print("❌ No API key configured")
            return []
        
        # Detect industry from skills
        industry = self._detect_industry(skills)
        print(f"🏭 Detected industry: {industry}")
        
        # Generate industry-specific queries
        queries = self._generate_universal_queries(skills, industry)
        
        # Fetch jobs from API
        all_jobs = self._fetch_jobs_from_api(queries, location)
        
        if not all_jobs:
            print("❌ No jobs found from API")
            return []
        
        # Calculate match scores
        for job in all_jobs:
            job['match_score'] = self._calculate_universal_score(job, skills, industry)
        
        # Sort by match score
        all_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Cache results
        cache.set(cache_key, all_jobs, 60 * 60 * 4)  # 4 hours
        
        print(f"✅ Found {len(all_jobs)} jobs in {time.time()-start:.1f}s")
        return all_jobs[:20]

    def _detect_industry(self, skills):
        """Detect which industry the skills belong to"""
        skills_text = ' '.join(skills).lower()
        
        # Industry keywords
        industries = {
            'medical': [
                'nurse', 'nursing', 'doctor', 'physician', 'surgeon', 'dentist', 
                'pharmacy', 'pharmacist', 'medical', 'clinical', 'hospital', 
                'healthcare', 'health', 'patient', 'therapy', 'therapist', 
                'radiologist', 'cardiologist', 'pediatrician', 'dermatologist',
                'medicine', 'surgery', 'emergency', 'paramedic', 'emt',
                'laboratory', 'lab', 'pathology', 'radiology', 'oncology',
                'neurology', 'cardiology', 'orthopedic', 'gynecology',
                'psychiatry', 'psychologist', 'counselor', 'therapist'
            ],
            'chemical': [
                'chemical', 'chemistry', 'chemist', 'laboratory', 'lab',
                'process', 'production', 'manufacturing', 'pharmaceutical',
                'petrochemical', 'polymer', 'material', 'compound', 'reaction',
                'analysis', 'analytical', 'synthesis', 'formulation',
                'quality control', 'qc', 'qa', 'safety', 'hazardous'
            ],
            'mechanical': [
                'mechanical', 'machinery', 'machine', 'equipment', 'maintenance',
                'repair', 'installation', 'fabrication', 'welding', 'machining',
                'cnc', 'cad', 'cam', 'solidworks', 'autocad', 'inventor',
                'hvac', 'plumbing', 'piping', 'hydraulic', 'pneumatic',
                'thermodynamics', 'fluid', 'mechanics', 'design', 'drafting'
            ],
            'electrical': [
                'electrical', 'electronics', 'electrician', 'circuit', 'wiring',
                'panel', 'breaker', 'transformer', 'motor', 'generator',
                'power', 'distribution', 'transmission', 'substation',
                'instrumentation', 'control', 'plc', 'scada', 'automation',
                'telecom', 'telecommunication', 'network', 'fiber', 'cabling',
                'renewable', 'solar', 'wind', 'energy'
            ],
            'civil': [
                'civil', 'construction', 'building', 'structure', 'infrastructure',
                'road', 'highway', 'bridge', 'tunnel', 'dam', 'foundation',
                'site', 'project', 'supervision', 'survey', 'estimation',
                'quantity', 'billing', 'planning', 'execution', 'contractor',
                'architect', 'architecture', 'structural', 'geotechnical',
                'transportation', 'urban', 'planning', 'development'
            ],
            'software': [
                'software', 'developer', 'programmer', 'coding', 'programming',
                'python', 'java', 'javascript', 'react', 'angular', 'node',
                'sql', 'database', 'web', 'frontend', 'backend', 'fullstack',
                'mobile', 'app', 'ios', 'android', 'cloud', 'aws', 'azure',
                'devops', 'docker', 'kubernetes', 'machine learning', 'ai'
            ],
            'data': [
                'data', 'analyst', 'analysis', 'analytics', 'statistics',
                'excel', 'tableau', 'power bi', 'sql', 'python', 'r',
                'machine learning', 'ai', 'artificial intelligence',
                'business intelligence', 'bi', 'reporting', 'dashboard',
                'visualization', 'predictive', 'modeling', 'mining'
            ],
            'marketing': [
                'marketing', 'digital', 'social media', 'seo', 'sem', 'ppc',
                'content', 'copywriting', 'brand', 'advertising', 'campaign',
                'email', 'marketing automation', 'crm', 'salesforce',
                'market research', 'analytics', 'google analytics', 'facebook'
            ],
            'finance': [
                'finance', 'accounting', 'accountant', 'audit', 'tax',
                'financial', 'analysis', 'analyst', 'investment', 'banking',
                'wealth', 'portfolio', 'risk', 'compliance', 'regulatory',
                'bookkeeping', 'quickbooks', 'sap', 'oracle', 'erp',
                'payroll', 'invoicing', 'budgeting', 'forecasting'
            ],
            'human_resources': [
                'hr', 'human resources', 'recruitment', 'recruiter', 'talent',
                'acquisition', 'staffing', 'onboarding', 'training',
                'development', 'employee relations', 'payroll', 'benefits',
                'compensation', 'performance', 'management', 'culture'
            ],
            'sales': [
                'sales', 'business development', 'bd', 'account executive',
                'account manager', 'sales representative', 'salesperson',
                'b2b', 'b2c', 'inside sales', 'outside sales', 'field sales',
                'territory', 'regional', 'national', 'global', 'quota',
                'crm', 'salesforce', 'negotiation', 'closing', 'prospecting'
            ],
            'customer_service': [
                'customer service', 'support', 'help desk', 'call center',
                'client services', 'customer success', 'csr', 'representative',
                'technical support', 'it support', 'service desk',
                'hospitality', 'retail', 'front desk', 'reception'
            ],
            'education': [
                'teacher', 'teaching', 'professor', 'instructor', 'educator',
                'faculty', 'lecturer', 'trainer', 'coach', 'mentor',
                'school', 'college', 'university', 'academic', 'education',
                'curriculum', 'instruction', 'lesson', 'classroom'
            ],
            'hospitality': [
                'hotel', 'restaurant', 'catering', 'food', 'beverage',
                'chef', 'cook', 'server', 'waiter', 'bartender',
                'management', 'front desk', 'concierge', 'housekeeping',
                'event', 'banquet', 'hospitality', 'tourism', 'travel'
            ]
        }
        
        # Count matches for each industry
        industry_scores = {}
        for industry, keywords in industries.items():
            score = 0
            for keyword in keywords:
                if keyword in skills_text:
                    score += 2
                # Also check for partial matches
                for skill in skills:
                    if keyword in skill or skill in keyword:
                        score += 1
            if score > 0:
                industry_scores[industry] = score
        
        # Return the industry with highest score, or 'general' if none
        if industry_scores:
            return max(industry_scores, key=industry_scores.get)
        return 'general'

    def _generate_universal_queries(self, skills, industry):
        """Generate industry-appropriate search queries"""
        queries = []
        primary_skill = skills[0] if skills else ""
        
        # Industry-specific job titles
        industry_titles = {
            'medical': [
                'nurse', 'doctor', 'physician', 'medical assistant', 
                'healthcare', 'clinical', 'hospital', 'pharmacist',
                'dentist', 'therapist', 'radiologist', 'surgeon'
            ],
            'chemical': [
                'chemical engineer', 'process engineer', 'production engineer',
                'chemical technician', 'laboratory technician', 'chemist',
                'quality control', 'pharmaceutical', 'petrochemical'
            ],
            'mechanical': [
                'mechanical engineer', 'design engineer', 'manufacturing engineer',
                'maintenance engineer', 'machinist', 'cnc operator',
                'hvac technician', 'mechanical designer', 'draftsman'
            ],
            'electrical': [
                'electrical engineer', 'electronics engineer', 'electrician',
                'instrumentation engineer', 'control engineer', 'power engineer',
                'electrical technician', 'automation engineer', 'scada'
            ],
            'civil': [
                'civil engineer', 'site engineer', 'construction manager',
                'project engineer', 'structural engineer', 'quantity surveyor',
                'building inspector', 'construction supervisor', 'architect'
            ],
            'software': [
                'software engineer', 'developer', 'programmer', 'full stack',
                'frontend', 'backend', 'mobile developer', 'devops engineer'
            ],
            'data': [
                'data scientist', 'data analyst', 'data engineer', 
                'business analyst', 'analytics manager', 'bi developer'
            ],
            'marketing': [
                'marketing manager', 'digital marketing', 'social media manager',
                'content writer', 'seo specialist', 'marketing coordinator'
            ],
            'finance': [
                'financial analyst', 'accountant', 'auditor', 'tax specialist',
                'finance manager', 'investment banker', 'wealth manager'
            ],
            'human_resources': [
                'hr manager', 'recruiter', 'talent acquisition', 'hr generalist',
                'training manager', 'compensation specialist', 'hr assistant'
            ],
            'sales': [
                'sales representative', 'account executive', 'business development',
                'sales manager', 'territory manager', 'regional sales'
            ],
            'customer_service': [
                'customer service representative', 'support specialist',
                'help desk technician', 'call center agent', 'client services'
            ],
            'education': [
                'teacher', 'professor', 'instructor', 'educator', 'trainer',
                'school teacher', 'college professor', 'academic advisor'
            ],
            'hospitality': [
                'hotel manager', 'restaurant manager', 'chef', 'cook',
                'front desk agent', 'concierge', 'event coordinator'
            ]
        }
        
        # Add industry-specific titles
        if industry in industry_titles:
            queries.extend(industry_titles[industry])
        
        # Add skill-based queries
        for skill in skills[:3]:
            queries.append(skill)
            queries.append(f"{skill} specialist")
            queries.append(f"{skill} technician")
            queries.append(f"{skill} engineer")
            queries.append(f"{skill} manager")
        
        # Add combination queries
        if len(skills) >= 2:
            queries.append(f"{skills[0]} {skills[1]}")
            queries.append(f"{skills[0]} and {skills[1]}")
        
        # Add general queries based on industry
        if industry == 'general':
            queries.extend([
                f"{primary_skill} jobs",
                f"{primary_skill} position",
                f"{primary_skill} career"
            ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for q in queries:
            if q not in seen:
                seen.add(q)
                unique_queries.append(q)
        
        return unique_queries[:10]  # Return top 10 unique queries

    def _fetch_jobs_from_api(self, queries, location):
        """Fetch jobs from JSearch API"""
        all_jobs = []
        seen_job_ids = set()
        
        for query in queries:
            # Rate limiting
            elapsed = time.time() - self.last_request
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            
            # Prepare search query
            search_query = query
            if location:
                search_query = f"{query} in {location}"
            
            url = f"{self.base_url}/search"
            params = {
                "query": search_query,
                "page": "1",
                "num_pages": "1",
                "date_posted": "week",  # Last 7 days
                "remote_jobs_only": "false"
            }
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host,
                "Content-Type": "application/json"
            }
            
            try:
                print(f"📡 Searching: '{query}'")
                response = requests.get(url, headers=headers, params=params, timeout=12)
                self.last_request = time.time()
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('status') == 'OK' and data.get('data'):
                        jobs = data['data']
                        print(f"   Found {len(jobs)} jobs")
                        
                        for job in jobs:
                            job_id = job.get('job_id')
                            if job_id and job_id not in seen_job_ids:
                                seen_job_ids.add(job_id)
                                formatted_job = self._format_universal_job(job)
                                all_jobs.append(formatted_job)
                    else:
                        print(f"   No jobs found")
                else:
                    print(f"⚠️ API error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout for query: '{query}'")
                continue
            except Exception as e:
                print(f"⚠️ Error: {e}")
                continue
            
            # Stop if we have enough jobs
            if len(all_jobs) >= 30:
                break
        
        return all_jobs

    def _format_universal_job(self, job):
        """Format job data for any industry"""
        # Extract salary
        salary = None
        if job.get('job_min_salary') and job.get('job_max_salary'):
            salary = f"${job['job_min_salary']:,.0f} - ${job['job_max_salary']:,.0f}"
            if job.get('job_salary_period'):
                salary += f" per {job['job_salary_period'].lower()}"
        elif job.get('job_min_salary'):
            salary = f"From ${job['job_min_salary']:,.0f}"
        
        # Location
        location_parts = []
        if job.get('job_city'):
            location_parts.append(job['job_city'])
        if job.get('job_state'):
            location_parts.append(job['job_state'])
        if job.get('job_country'):
            location_parts.append(job['job_country'])
        
        location = ', '.join(location_parts) if location_parts else 'Remote'
        
        # Description
        description = job.get('job_description', '')
        if len(description) > 300:
            description = description[:300] + '...'
        
        return {
            'id': job.get('job_id'),
            'title': job.get('job_title'),
            'company': job.get('employer_name'),
            'company_logo': job.get('employer_logo'),
            'location': location,
            'description': description,
            'salary': salary,
            'apply_url': job.get('job_apply_link'),
            'posted_date': job.get('job_posted_at_datetime_utc'),
            'job_type': job.get('job_employment_type', 'fulltime').lower(),
            'is_remote': job.get('job_is_remote', False),
            'source': 'JSearch API',
            'required_skills': [],  # Will be populated by score calculation
        }

    def _calculate_universal_score(self, job, user_skills, industry):
        """Calculate relevance score for any industry"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        score = 50  # Base score
        matched_skills = []
        
        for skill in user_skills:
            skill_lower = skill.lower()
            
            # Check in title (highest weight)
            if skill_lower in title:
                score += 15
                matched_skills.append(skill)
            # Check in description
            elif skill_lower in description:
                score += 8
                matched_skills.append(skill)
            # Check for partial matches (for industry terms)
            elif any(word in skill_lower for word in description.split()):
                score += 3
        
        # Industry bonus
        industry_keywords = {
            'medical': ['hospital', 'clinic', 'patient', 'health', 'medical'],
            'chemical': ['lab', 'chemical', 'process', 'production'],
            'mechanical': ['mechanical', 'machine', 'equipment', 'maintenance'],
            'electrical': ['electrical', 'power', 'circuit', 'electronic'],
            'civil': ['construction', 'building', 'site', 'infrastructure'],
            'software': ['software', 'development', 'programming', 'coding'],
            'data': ['data', 'analysis', 'analytics', 'statistics'],
            'marketing': ['marketing', 'advertising', 'campaign', 'brand'],
            'finance': ['finance', 'accounting', 'financial', 'investment'],
            'sales': ['sales', 'client', 'customer', 'revenue'],
            'customer_service': ['support', 'service', 'help', 'customer'],
            'education': ['teaching', 'education', 'school', 'college'],
            'hospitality': ['hotel', 'restaurant', 'service', 'guest']
        }
        
        if industry in industry_keywords:
            for keyword in industry_keywords[industry]:
                if keyword in title or keyword in description:
                    score += 10
                    break
        
        # Store matched skills
        job['required_skills'] = list(set(matched_skills))[:8]
        
        return min(98, score)
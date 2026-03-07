import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from collections import Counter

class SkillRecommender:
    """
    AI-Powered Skill Recommendation Engine
    Analyzes current skills and suggests next skills to learn
    """
    
    def __init__(self):
        self.skill_relationships = self._build_skill_graph()
        self.career_paths = self._load_career_paths()
        self.market_demand = self._load_market_demand()
        
    def _build_skill_graph(self):
        """Build knowledge graph of skill relationships"""
        return {
            # Programming Languages
            'python': {
                'related': ['django', 'flask', 'fastapi', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
                'next': ['advanced python', 'design patterns', 'async programming', 'cython'],
                'career_roles': ['backend developer', 'data scientist', 'ml engineer'],
                'demand_score': 95
            },
            'java': {
                'related': ['spring', 'hibernate', 'maven', 'junit', 'gradle', 'kotlin'],
                'next': ['java ee', 'microservices', 'performance tuning', 'reactive programming'],
                'career_roles': ['backend developer', 'android developer', 'enterprise architect'],
                'demand_score': 90
            },
            'javascript': {
                'related': ['react', 'vue', 'angular', 'node.js', 'typescript', 'jquery'],
                'next': ['advanced js', 'functional programming', 'webpack', 'babel'],
                'career_roles': ['frontend developer', 'full stack developer', 'web developer'],
                'demand_score': 98
            },
            'typescript': {
                'related': ['react', 'angular', 'node.js', 'next.js', 'nest.js'],
                'next': ['advanced types', 'decorators', 'generic programming'],
                'career_roles': ['frontend developer', 'full stack developer'],
                'demand_score': 92
            },
            
            # Frameworks
            'react': {
                'related': ['redux', 'next.js', 'react native', 'graphql', 'tailwind', 'material-ui'],
                'next': ['advanced hooks', 'performance optimization', 'custom hooks', 'ssr'],
                'career_roles': ['frontend developer', 'react developer', 'mobile developer'],
                'demand_score': 96
            },
            'django': {
                'related': ['drf', 'celery', 'redis', 'postgresql', 'docker'],
                'next': ['django channels', 'advanced orm', 'scalability'],
                'career_roles': ['backend developer', 'python developer'],
                'demand_score': 88
            },
            'spring': {
                'related': ['spring boot', 'spring cloud', 'hibernate', 'jpa', 'microservices'],
                'next': ['spring security', 'reactive spring', 'cloud native'],
                'career_roles': ['java developer', 'backend developer'],
                'demand_score': 89
            },
            'node.js': {
                'related': ['express', 'nestjs', 'graphql', 'mongodb', 'socket.io'],
                'next': ['advanced node', 'clustering', 'streams', 'worker threads'],
                'career_roles': ['backend developer', 'full stack developer'],
                'demand_score': 91
            },
            
            # Databases
            'sql': {
                'related': ['mysql', 'postgresql', 'sqlite', 'query optimization'],
                'next': ['advanced sql', 'stored procedures', 'triggers', 'performance tuning'],
                'career_roles': ['backend developer', 'data analyst', 'dba'],
                'demand_score': 94
            },
            'mongodb': {
                'related': ['mongoose', 'aggregation', 'indexing', 'replication'],
                'next': ['sharding', 'advanced aggregation', 'data modeling'],
                'career_roles': ['backend developer', 'full stack developer'],
                'demand_score': 86
            },
            'postgresql': {
                'related': ['plpgsql', 'postgis', 'replication', 'backup strategies'],
                'next': ['advanced indexing', 'query planning', 'vacuum strategies'],
                'career_roles': ['backend developer', 'dba', 'data engineer'],
                'demand_score': 89
            },
            
            # Cloud & DevOps
            'aws': {
                'related': ['ec2', 's3', 'lambda', 'dynamodb', 'cloudformation', 'docker'],
                'next': ['aws architect', 'serverless', 'cloud security', 'cost optimization'],
                'career_roles': ['cloud engineer', 'devops engineer', 'solutions architect'],
                'demand_score': 94
            },
            'docker': {
                'related': ['kubernetes', 'jenkins', 'ansible', 'terraform', 'docker-compose'],
                'next': ['container orchestration', 'service mesh', 'istio', 'security'],
                'career_roles': ['devops engineer', 'platform engineer'],
                'demand_score': 92
            },
            'kubernetes': {
                'related': ['helm', 'istio', 'prometheus', 'grafana', 'argocd'],
                'next': ['ckad certification', 'operator pattern', 'service mesh'],
                'career_roles': ['devops engineer', 'site reliability engineer'],
                'demand_score': 91
            },
            
            # Data Science
            'machine learning': {
                'related': ['tensorflow', 'pytorch', 'scikit-learn', 'keras', 'opencv'],
                'next': ['deep learning', 'nlp', 'computer vision', 'mlops'],
                'career_roles': ['ml engineer', 'data scientist', 'ai engineer'],
                'demand_score': 93
            },
            'data analysis': {
                'related': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy'],
                'next': ['statistics', 'feature engineering', 'a/b testing'],
                'career_roles': ['data analyst', 'business analyst'],
                'demand_score': 89
            },
            
            # Soft Skills
            'communication': {
                'related': ['presentation', 'negotiation', 'writing', 'public speaking'],
                'next': ['storytelling', 'technical writing', 'cross-cultural communication'],
                'career_roles': ['all roles'],
                'demand_score': 98
            },
            'leadership': {
                'related': ['team management', 'mentoring', 'conflict resolution'],
                'next': ['strategic planning', 'change management', 'executive leadership'],
                'career_roles': ['tech lead', 'manager', 'director'],
                'demand_score': 95
            },
            'problem solving': {
                'related': ['critical thinking', 'analytical skills', 'decision making'],
                'next': ['algorithms', 'system design', 'architectural thinking'],
                'career_roles': ['all roles'],
                'demand_score': 99
            }
        }
    
    def _load_career_paths(self):
        """Load career progression paths"""
        return {
            'frontend': {
                'entry': ['html', 'css', 'javascript'],
                'mid': ['react/vue', 'typescript', 'state management'],
                'senior': ['performance', 'architecture', 'team leadership'],
                'expert': ['framework design', 'open source', 'technical strategy']
            },
            'backend': {
                'entry': ['python/java', 'sql', 'basic api'],
                'mid': ['frameworks', 'database design', 'microservices'],
                'senior': ['system design', 'scalability', 'mentoring'],
                'expert': ['architecture', 'innovation', 'technical vision']
            },
            'data': {
                'entry': ['python', 'sql', 'statistics'],
                'mid': ['machine learning', 'visualization', 'big data'],
                'senior': ['deep learning', 'mlops', 'research'],
                'expert': ['ai research', 'innovation', 'technical leadership']
            },
            'devops': {
                'entry': ['linux', 'scripting', 'ci/cd basics'],
                'mid': ['containers', 'orchestration', 'cloud'],
                'senior': ['infrastructure as code', 'security', 'sre'],
                'expert': ['platform engineering', 'innovation', 'strategy']
            }
        }
    
    def _load_market_demand(self):
        """Load market demand data for skills"""
        return {
            'python': 95, 'java': 90, 'javascript': 98, 'typescript': 92,
            'react': 96, 'angular': 85, 'vue': 88, 'django': 88,
            'spring': 89, 'node.js': 91, 'sql': 94, 'mongodb': 86,
            'aws': 94, 'docker': 92, 'kubernetes': 91, 'tensorflow': 88,
            'machine learning': 93, 'data analysis': 89, 'communication': 98,
            'leadership': 95, 'problem solving': 99
        }
    
    def get_recommendations(self, current_skills, career_goal=None):
        """
        Get personalized skill recommendations based on current skills
        """
        if not current_skills:
            return self._get_popular_skills()
        
        # Normalize skill names
        current = [s.lower() for s in current_skills]
        
        # Find related skills
        related_skills = []
        for skill in current:
            if skill in self.skill_relationships:
                related_skills.extend(self.skill_relationships[skill]['related'])
                if career_goal:
                    # Filter by career goal
                    related_skills = [
                        s for s in related_skills 
                        if career_goal in ' '.join(self.skill_relationships.get(s, {}).get('career_roles', []))
                    ]
        
        # Count frequencies and add demand scores
        skill_counts = Counter(related_skills)
        scored_skills = []
        
        for skill, count in skill_counts.items():
            demand = self.market_demand.get(skill, 70)
            score = min(95, (count * 20) + (demand * 0.5))
            scored_skills.append({
                'name': skill.title(),
                'relevance': count,
                'demand_score': demand,
                'match_score': int(score),
                'category': self.skill_relationships.get(skill, {}).get('category', 'general'),
                'estimated_time': self._get_learning_time(skill)
            })
        
        # Sort by combined score
        scored_skills.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Get next level skills
        next_level = self._get_next_level_skills(current)
        
        # Get career path suggestions
        career_suggestions = self._suggest_career_paths(current)
        
        return {
            'recommendations': scored_skills[:10],
            'next_level': next_level[:5],
            'career_paths': career_suggestions,
            'skill_gaps': self._analyze_skill_gaps(current, career_goal)
        }
    
    def _get_next_level_skills(self, current_skills):
        """Get advanced version of current skills"""
        next_level = []
        for skill in current_skills:
            if skill in self.skill_relationships:
                next_level.extend(self.skill_relationships[skill]['next'])
        return list(set(next_level))[:5]
    
    def _suggest_career_paths(self, current_skills):
        """Suggest career paths based on current skills"""
        suggestions = []
        for path_name, path in self.career_paths.items():
            match_score = 0
            for level, skills in path.items():
                for skill in skills:
                    if skill in current_skills:
                        match_score += 25
            if match_score > 30:
                suggestions.append({
                    'name': path_name.title(),
                    'match': min(95, match_score),
                    'next_step': path['mid'][0] if path_name in self.career_paths else ''
                })
        return sorted(suggestions, key=lambda x: x['match'], reverse=True)
    
    def _analyze_skill_gaps(self, current_skills, career_goal):
        """Analyze skill gaps for specific career goal"""
        if not career_goal:
            return []
        
        goal_requirements = {
            'frontend': ['javascript', 'react', 'html', 'css'],
            'backend': ['python', 'java', 'sql', 'apis'],
            'fullstack': ['javascript', 'react', 'python', 'sql'],
            'devops': ['docker', 'kubernetes', 'aws', 'linux'],
            'data': ['python', 'sql', 'statistics', 'machine learning']
        }
        
        required = goal_requirements.get(career_goal.lower(), [])
        gaps = [s for s in required if s not in current_skills]
        
        return [{'skill': s, 'priority': 'high' if i < 2 else 'medium'} for i, s in enumerate(gaps)]
    
    def _get_learning_time(self, skill):
        """Estimate learning time for a skill"""
        base_times = {
            'programming': 80,
            'framework': 60,
            'database': 50,
            'cloud': 70,
            'devops': 65,
            'soft_skill': 30
        }
        category = self.skill_relationships.get(skill, {}).get('category', 'general')
        return base_times.get(category, 50)
    
    def _get_popular_skills(self):
        """Return popular skills for users with no skills"""
        popular = [
            {'name': 'Python', 'demand_score': 95, 'match_score': 90, 'category': 'programming', 'estimated_time': 80},
            {'name': 'JavaScript', 'demand_score': 98, 'match_score': 95, 'category': 'programming', 'estimated_time': 70},
            {'name': 'React', 'demand_score': 96, 'match_score': 92, 'category': 'framework', 'estimated_time': 60},
            {'name': 'SQL', 'demand_score': 94, 'match_score': 88, 'category': 'database', 'estimated_time': 50},
            {'name': 'AWS', 'demand_score': 94, 'match_score': 85, 'category': 'cloud', 'estimated_time': 70},
            {'name': 'Communication', 'demand_score': 98, 'match_score': 80, 'category': 'soft_skill', 'estimated_time': 30}
        ]
        return {'recommendations': popular, 'next_level': [], 'career_paths': []}
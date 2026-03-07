import re
import PyPDF2
import docx
from typing import List, Dict

class ImprovedResumeParser:
    def __init__(self):
        self.skill_database = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
                'swift', 'kotlin', 'typescript', 'go', 'rust', 'scala', 'c',
                'c programming', 'c language', 'c (programming language)'
            ],
            'frameworks': [
                'django', 'flask', 'react', 'angular', 'vue', 'spring',
                'laravel', 'node.js', 'express', 'next.js', 'tensorflow',
                'pytorch', 'keras', 'jquery', 'bootstrap', 'oop',
                'object oriented programming', 'object-oriented'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sqlite', 'cassandra', 'dynamodb', 'firebase',
                'sql', 'database', 'dbms'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                'terraform', 'ansible', 'prometheus', 'grafana', 'devops'
            ],
            'soft_skills': [
                'communication', 'leadership', 'teamwork', 'problem solving',
                'analytical', 'management', 'presentation', 'negotiation',
                'time management', 'critical thinking', 'creativity',
                'logical thinking', 'mathematics', 'problem-solving',
                'analytical skills', 'logical reasoning', 'aptitude'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'nlp', 'computer vision',
                'data analysis', 'statistics', 'tableau', 'power bi',
                'excel', 'r', 'spss', 'sas', 'data structures',
                'algorithms', 'dsa', 'data structures and algorithms'
            ]
        }
        
        # Enhanced section patterns for irregular resumes
        self.section_patterns = {
            'education': [
                r'education', r'academic', r'qualifications', r'degree',
                r'b\.sc', r'm\.sc', r'bachelor', r'master', r'university',
                r'college', r'school', r'graduation'
            ],
            'experience': [
                r'experience', r'work experience', r'employment', r'work history',
                r'professional experience', r'career', r'job'
            ],
            'projects': [
                r'projects', r'portfolio', r'work samples', r'mini project',
                r'project work', r'academic projects', r'personal projects'
            ],
            'skills': [
                r'skills', r'technical skills', r'key skills', r'competencies',
                r'expertise', r'proficiencies', r'technologies'
            ],
            'certifications': [
                r'certifications', r'certificates', r'courses', r'training',
                r'professional development', r'credentials'
            ],
            'contact': [
                r'contact', r'personal details', r'contact info', r'reach me',
                r'phone', r'email', r'mobile', r'address'
            ],
            'summary': [
                r'summary', r'profile', r'about me', r'objective',
                r'career objective', r'professional summary'
            ]
        }
    
    def _extract_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"PDF extraction error: {e}")
            raise e
        return text
    
    def _extract_docx(self, file_path):
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                if paragraph.text:
                    text += paragraph.text + "\n"
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            raise e
        return text
    
    def extract_text(self, file_path):
        """Extract text from file based on extension"""
        if file_path.endswith('.pdf'):
            return self._extract_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self._extract_docx(file_path)
        return ""
    
    def _detect_sections(self, text):
        """
        Enhanced section detection for irregular resume formats
        Returns a dictionary of section name -> content
        """
        lines = text.split('\n')
        sections = {
            'header': [],
            'education': [],
            'experience': [],
            'projects': [],
            'skills': [],
            'certifications': [],
            'contact': [],
            'summary': [],
            'other': []
        }
        
        current_section = 'header'
        section_confidence = {}
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Skip empty lines
            if not line_lower:
                continue
            
            # Check for section headers
            detected = False
            for section, patterns in self.section_patterns.items():
                for pattern in patterns:
                    if re.search(rf'\b{pattern}\b', line_lower):
                        # Found a section header
                        current_section = section
                        detected = True
                        section_confidence[section] = section_confidence.get(section, 0) + 1
                        break
                if detected:
                    break
            
            # If no header detected, check for content-based indicators
            if not detected:
                # Education indicators
                if any(word in line_lower for word in ['b.sc', 'bachelor', 'university', 'college', 'degree']):
                    current_section = 'education'
                # Skill indicators
                elif any(word in line_lower for word in ['skill', 'proficient', 'knowledge']):
                    current_section = 'skills'
                # Project indicators
                elif any(word in line_lower for word in ['project', 'developed', 'built', 'created']):
                    current_section = 'projects'
                # Contact indicators
                elif any(word in line_lower for word in ['@', 'phone', 'mobile', 'contact']):
                    current_section = 'contact'
            
            # Add line to appropriate section
            if current_section in sections:
                sections[current_section].append(line)
            else:
                sections['other'].append(line)
        
        return sections
    
    def parse_resume(self, file_path):
        """Enhanced main method to parse resume and extract all information"""
        try:
            text = self.extract_text(file_path)
            
            if not text:
                return {
                    'personal_info': {},
                    'skills': {'by_category': {}, 'flat_list': []},
                    'experience': [],
                    'education': [],
                    'projects': [],
                    'certifications': [],
                    'languages': [],
                    'experience_years': 0,
                    'raw_text_preview': "No text could be extracted from the file."
                }
            
            # Detect sections (new!)
            sections = self._detect_sections(text)
            
            # Extract years of experience
            experience_years = self._extract_experience_years(text)
            
            # Extract all skills (enhanced)
            skills_data = self.extract_all_skills(text, sections.get('skills', []))
            
            return {
                'personal_info': self.extract_personal_info(text, sections.get('header', [])),
                'skills': skills_data,
                'experience': self.extract_experience_details(text, sections.get('experience', [])),
                'education': self.extract_education_details(text, sections.get('education', [])),
                'projects': self.extract_projects(text, sections.get('projects', [])),
                'certifications': self.extract_certifications(text, sections.get('certifications', [])),
                'languages': self.extract_languages(text),
                'summary': self._extract_summary(text, sections.get('summary', [])),
                'experience_years': experience_years,
                'raw_text_preview': text[:1000] + '...' if len(text) > 1000 else text,
                'detected_sections': {k: len(v) for k, v in sections.items() if v}  # Debug info
            }
        except Exception as e:
            print(f"Error in parse_resume: {e}")
            raise e
    
    def extract_all_skills(self, text, skill_section_lines=None):
        """Enhanced skill extraction with context from skill section"""
        text_lower = text.lower()
        found_skills = {}
        flat_skills = []
        
        # First, check if there's a dedicated skills section
        skill_section_text = ' '.join(skill_section_lines).lower() if skill_section_lines else ''
        
        for category, skills in self.skill_database.items():
            category_skills = []
            for skill in skills:
                # Look for exact matches in full text
                if skill in text_lower:
                    # Check if skill appears in skill section (higher confidence)
                    in_skill_section = skill in skill_section_text
                    
                    # Determine proficiency level
                    proficiency = self._get_proficiency_level(skill, text_lower, in_skill_section)
                    
                    skill_obj = {
                        'name': skill,
                        'proficiency': proficiency,
                        'context': self._get_skill_context(skill, text),
                        'in_skill_section': in_skill_section
                    }
                    category_skills.append(skill_obj)
                    flat_skills.append(skill_obj)
            
            if category_skills:
                found_skills[category] = category_skills
        
        # Sort skills by proficiency (expert first)
        flat_skills.sort(key=lambda x: 
                         {'expert': 4, 'advanced': 3, 'intermediate': 2, 'beginner': 1}.get(x['proficiency'], 0), 
                         reverse=True)
        
        return {
            'by_category': found_skills,
            'flat_list': flat_skills,
            'count': len(flat_skills)
        }
    
    def _get_proficiency_level(self, skill, text, in_skill_section=False):
        """Enhanced proficiency detection"""
        # Boost confidence if in skill section
        confidence_boost = 1 if in_skill_section else 0
        
        if f"expert in {skill}" in text or f"lead {skill}" in text:
            return "expert"
        elif f"advanced {skill}" in text or f"{skill} expert" in text:
            return "advanced"
        elif f"intermediate {skill}" in text or f"working knowledge of {skill}" in text:
            return "intermediate"
        elif f"beginner {skill}" in text or f"learning {skill}" in text:
            return "beginner"
        
        # Count occurrences with context boost
        count = text.count(skill) + confidence_boost
        if count > 5:
            return "expert"
        elif count > 3:
            return "advanced"
        elif count > 1:
            return "intermediate"
        return "beginner"
    
    def _get_skill_context(self, skill, text):
        """Get the sentence containing the skill"""
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if skill in sentence.lower():
                return sentence.strip()
        return ""
    
    def _extract_experience_years(self, text):
        """Extract total years of experience with enhanced patterns"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)\+?\s*years?',
            r'(\d+)\s*yrs?\s*(?:of)?\s*experience',
            r'(\d+)\+?\s*years?\s+experience',
            r'worked for (\d+)\+?\s*years?',
            r'(\d+)\+?\s*year career'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        
        # Try to calculate from work experience entries
        exp_entries = re.findall(r'(\d{4})\s*(?:-|–|to)\s*(\d{4}|present|current)', text.lower())
        if exp_entries:
            total_years = 0
            current_year = 2025  # You might want to get current year dynamically
            for start, end in exp_entries:
                if end in ['present', 'current']:
                    total_years += current_year - int(start)
                else:
                    total_years += int(end) - int(start)
            return total_years
        
        return 0
    
    def extract_personal_info(self, text, header_lines=None):
        """Enhanced personal info extraction"""
        info = {}
        
        # Use header lines if available
        header_text = ' '.join(header_lines) if header_lines else text[:500]
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            info['email'] = email_match.group()
        
        # Extract phone - enhanced pattern
        phone_patterns = [
            r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}',
            r'\b\d{10}\b',
            r'\b\d{5}\s?\d{5}\b'
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                info['phone'] = phone_match.group()
                break
        
        # Enhanced name extraction
        lines = text.strip().split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Name should be 2-4 words, all caps or title case, no special characters
            if (line and 2 <= len(line.split()) <= 4 and 
                not re.search(r'@|http|www|\d{4,}', line) and
                not any(word in line.lower() for word in ['education', 'skills', 'experience', 'contact'])):
                
                # Check if it looks like a name (all caps or title case)
                words = line.split()
                if all(w[0].isupper() for w in words) or line.isupper():
                    info['name'] = line
                    break
        
        # Extract location
        location_patterns = [
            r'(?:location|address|city|based in)[:\s]+([^,\n]+(?:,\s*[^,\n]+)?)',
            r'([A-Z][a-z]+(?:[\s,]+[A-Z][a-z]+)*,\s*[A-Z]{2})',
            r'([A-Za-z\s]+-?\s*\d{6})'  # Indian PIN code pattern
        ]
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['location'] = match.group(1).strip() if match.groups() else match.group(0).strip()
                break
        
        return info
    
    def extract_experience_details(self, text, exp_section_lines=None):
        """Enhanced work experience extraction"""
        experiences = []
        
        # Use provided section or find it
        exp_text = ' '.join(exp_section_lines) if exp_section_lines else text
        
        # Try different section patterns
        section_patterns = [
            r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL EXPERIENCE).*?\n(.*?)(?=\n\s*(?:EDUCATION|PROJECTS|SKILLS|CERTIFICATIONS|$))',
            r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT).*?(?=\n\s*(?:EDUCATION|PROJECTS|SKILLS|$))'
        ]
        
        for pattern in section_patterns:
            section_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if section_match:
                exp_text = section_match.group(1) if section_match.groups() else section_match.group(0)
                break
        
        # Extract individual job entries
        job_blocks = re.split(r'\n(?=\d{4}|\w+\s+\d{4}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4})', 
                              exp_text, flags=re.IGNORECASE)
        
        for block in job_blocks[:5]:
            if not block.strip() or len(block.strip()) < 15:
                continue
            
            # Extract dates
            date_patterns = [
                r'(\d{4})\s*(?:-|–|to)\s*(\d{4}|present|current)',
                r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\s*(?:-|–|to)\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4}|present|current)',
                r'(\d{4})\s*(?:-|–|to)\s*(?:present|current)'
            ]
            
            dates = []
            for pattern in date_patterns:
                date_match = re.search(pattern, block, re.IGNORECASE)
                if date_match:
                    dates = date_match.groups()
                    break
            
            # Extract company and title
            lines = block.strip().split('\n')
            title = lines[0].strip() if lines else ""
            company = ""
            
            # Try to find company (often the second line or after date)
            for i, line in enumerate(lines[1:4]):  # Check next few lines
                if line and not re.match(r'^\d{4}', line) and len(line.split()) <= 5:
                    company = line.strip()
                    break
            
            # Extract responsibilities
            responsibilities = []
            for line in lines:
                line = line.strip()
                if (line and len(line) > 15 and 
                    not re.match(r'^\d{4}', line) and
                    line != title and line != company and
                    not any(date in line for date in str(dates))):
                    responsibilities.append(line[:150])
            
            if title and (company or responsibilities):
                experiences.append({
                    'title': title[:100],
                    'company': company[:100] if company else "Unknown",
                    'dates': dates,
                    'responsibilities': responsibilities[:3],
                    'duration': self._calculate_duration(dates) if dates else None
                })
        
        return experiences
    
    def _calculate_duration(self, dates):
        """Calculate duration from date range"""
        if not dates or len(dates) < 2:
            return None
        try:
            start = int(dates[0])
            end = dates[1]
            if end in ['present', 'current']:
                return f"{2025 - start}+ years"  # Use current year
            else:
                return f"{int(end) - start} years"
        except:
            return None
    
    def extract_education_details(self, text, edu_section_lines=None):
        """Enhanced education extraction"""
        education = []
        
        # Use provided section or find it
        edu_text = ' '.join(edu_section_lines) if edu_section_lines else text
        
        # Try to find education section
        section_patterns = [
            r'(?:EDUCATION|ACADEMIC|QUALIFICATIONS|ACADEMIC BACKGROUND).*?\n(.*?)(?=\n\s*(?:EXPERIENCE|PROJECTS|SKILLS|CERTIFICATIONS|$))',
            r'(?:EDUCATION|ACADEMIC).*?(?=\n\s*(?:EXPERIENCE|PROJECTS|SKILLS|$))'
        ]
        
        for pattern in section_patterns:
            section_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if section_match:
                edu_text = section_match.group(1) if section_match.groups() else section_match.group(0)
                break
        
        # Common degree patterns
        degree_patterns = [
            (r'(bachelor|master|phd|doctorate)', 'degree'),
            (r'b\.?\s?sc|bachelor of science', 'B.Sc'),
            (r'm\.?\s?sc|master of science', 'M.Sc'),
            (r'b\.?\s?tech|bachelor of technology', 'B.Tech'),
            (r'm\.?\s?tech|master of technology', 'M.Tech'),
            (r'b\.?\s?e|bachelor of engineering', 'B.E'),
            (r'm\.?\s?e|master of engineering', 'M.E'),
            (r'bca|bachelor of computer applications', 'BCA'),
            (r'mca|master of computer applications', 'MCA'),
            (r'diploma', 'Diploma'),
            (r'high school', 'High School')
        ]
        
        lines = edu_text.split('\n')
        current_edu = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for year
            year_match = re.search(r'\b(19|20)\d{2}\b', line)
            if year_match and 'year' not in current_edu:
                current_edu['year'] = year_match.group()
            
            # Check for degree
            for pattern, degree_name in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    current_edu['degree'] = degree_name
                    break
            
            # Check for institution
            if any(word in line.lower() for word in ['university', 'college', 'institute', 'school']):
                current_edu['institution'] = line
            
            # If we have both degree and institution, save and reset
            if 'degree' in current_edu and 'institution' in current_edu:
                if 'year' not in current_edu:
                    # Try to find year in the same line
                    year_match = re.search(r'\b(19|20)\d{2}\b', line)
                    if year_match:
                        current_edu['year'] = year_match.group()
                
                education.append({
                    'degree': current_edu.get('degree', ''),
                    'institution': current_edu.get('institution', ''),
                    'year': current_edu.get('year', ''),
                    'raw_text': line[:100]
                })
                current_edu = {}
        
        # If we couldn't parse structured education, try regex on the whole text
        if not education:
            # Look for common patterns like "University 2018-2021 Degree"
            edu_pattern = r'([A-Za-z\s]+(?:University|College|Institute)).*?(\d{4}).*?([A-Za-z\.\s]+(?:B\.?Sc|M\.?Sc|B\.?Tech|B\.?E|Degree))'
            matches = re.findall(edu_pattern, text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'institution': match[0].strip(),
                    'year': match[1],
                    'degree': match[2].strip(),
                    'raw_text': ' '.join(match)
                })
        
        return education[:3]  # Limit to top 3
    
    def extract_projects(self, text, project_section_lines=None):
        """Enhanced project extraction"""
        projects = []
        
        # Use provided section or find it
        project_text = ' '.join(project_section_lines) if project_section_lines else text
        
        # Try to find projects section
        section_patterns = [
            r'(?:PROJECTS|PORTFOLIO|WORK SAMPLES|PERSONAL PROJECTS|MINI PROJECT).*?\n(.*?)(?=\n\s*(?:EDUCATION|EXPERIENCE|SKILLS|CERTIFICATIONS|$))',
            r'(?:PROJECTS|PORTFOLIO).*?(?=\n\s*(?:EDUCATION|EXPERIENCE|SKILLS|$))'
        ]
        
        for pattern in section_patterns:
            section_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if section_match:
                project_text = section_match.group(1) if section_match.groups() else section_match.group(0)
                break
        
        # Split by project indicators
        project_blocks = re.split(r'\n(?=[A-Z][^a-z]*:?|\d+\.|\*|\-|Project\s+\d+)', project_text)
        
        for block in project_blocks[:5]:
            if not block.strip() or len(block.strip()) < 20:
                continue
            
            lines = block.strip().split('\n')
            name = lines[0].strip() if lines else ""
            
            # Clean up project name
            name = re.sub(r'^[\d\*\.\-\s]+', '', name)
            name = re.sub(r':$', '', name)
            
            # Extract technologies if mentioned
            technologies = []
            tech_match = re.search(r'(?:using|with|technologies?|tech stack)[:\s]+([^.\n]+)', block, re.IGNORECASE)
            if tech_match:
                tech_text = tech_match.group(1)
                technologies = [t.strip() for t in re.split(r'[,&\s]+', tech_text) if t.strip()]
            
            description = ' '.join(lines[1:]).strip() if len(lines) > 1 else ""
            
            projects.append({
                'name': name[:100],
                'description': description[:300],
                'technologies': technologies[:5]
            })
        
        return projects
    
    def extract_certifications(self, text, cert_section_lines=None):
        """Enhanced certification extraction"""
        certs = []
        
        # Use provided section or search whole text
        search_text = ' '.join(cert_section_lines) if cert_section_lines else text
        
        cert_patterns = [
            r'(?:certified|certification|certificate)[\s:]+([^.\n]+)',
            r'(?:aws|google|microsoft|oracle|cisco)[\s-]+(?:certified|certification)[\s:]+([^.\n]+)',
            r'(?:pmp|itil|scrum|cspo|ceh|cissp)[\s,]+([^.\n]+)?',
            r'(?:completion of|completed)[\s:]+([^.\n]+(?:course|training|program))'
        ]
        
        for pattern in cert_patterns:
            matches = re.finditer(pattern, search_text, re.IGNORECASE)
            for match in matches:
                cert = match.group(1).strip() if match.groups() else match.group(0).strip()
                if len(cert) > 3 and cert not in certs:
                    certs.append(cert[:100])
        
        return list(set(certs))[:5]
    
    def extract_languages(self, text):
        """Enhanced language extraction"""
        languages = []
        
        common_languages = [
            'english', 'spanish', 'french', 'german', 'chinese', 'japanese',
            'korean', 'hindi', 'tamil', 'telugu', 'bengali', 'marathi',
            'gujarati', 'punjabi', 'russian', 'arabic', 'portuguese',
            'italian', 'dutch', 'polish', 'turkish', 'vietnamese'
        ]
        
        text_lower = text.lower()
        
        # Look for language section
        lang_section = re.search(r'(?:LANGUAGES?|LINGUISTIC).*?\n(.*?)(?=\n\s*\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        lang_text = lang_section.group(1).lower() if lang_section else text_lower
        
        for lang in common_languages:
            if lang in lang_text or lang in text_lower:
                # Look for proficiency indicators
                proficiency = "basic"
                if f"fluent in {lang}" in text_lower or f"native {lang}" in text_lower:
                    proficiency = "fluent"
                elif f"professional working proficiency in {lang}" in text_lower:
                    proficiency = "professional"
                elif f"conversational {lang}" in text_lower:
                    proficiency = "conversational"
                elif f"advanced {lang}" in text_lower:
                    proficiency = "advanced"
                elif f"intermediate {lang}" in text_lower:
                    proficiency = "intermediate"
                
                # Check if in language section (higher confidence)
                if lang in lang_text:
                    if proficiency == "basic":
                        proficiency = "mentioned"
                
                languages.append({
                    'name': lang.capitalize(),
                    'proficiency': proficiency,
                    'in_language_section': lang in lang_text
                })
        
        return languages
    
    def _extract_summary(self, text, summary_lines=None):
        """Extract professional summary/objective"""
        if summary_lines:
            return ' '.join(summary_lines)[:500]
        
        # Try to find summary section
        summary_patterns = [
            r'(?:SUMMARY|PROFILE|ABOUT ME|OBJECTIVE|CAREER OBJECTIVE).*?\n(.*?)(?=\n\s*(?:EDUCATION|EXPERIENCE|SKILLS|PROJECTS|$))',
            r'(?:SUMMARY|PROFILE).*?(?=\n\s*(?:EDUCATION|EXPERIENCE|SKILLS|$))'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1) if match.groups() else match.group(0)
                return ' '.join(summary.split())[:500]
        
        return ""
    
    def suggest_improvements(self, parsed_data):
        """Enhanced suggestions based on parsed data"""
        suggestions = []
        
        # Extract skills
        skills_data = parsed_data.get('skills', {})
        flat_skills = skills_data.get('flat_list', [])
        skill_names = [s['name'] for s in flat_skills]
        
        experience = parsed_data.get('experience_years', 0)
        education = parsed_data.get('education', [])
        projects = parsed_data.get('projects', [])
        
        # Check for missing important skills
        if len(skill_names) < 5:
            suggestions.append({
                'type': 'skill',
                'priority': 'high',
                'suggestion': 'Add more skills to your resume. Employers look for at least 5-8 relevant skills.',
                'resources': ['Skill gap analysis tool', 'Online courses']
            })
        
        # Check for specific in-demand skills
        in_demand = ['python', 'javascript', 'react', 'aws', 'docker', 'sql']
        missing_demand = [s for s in in_demand if s not in skill_names]
        
        if missing_demand:
            suggestions.append({
                'type': 'skill',
                'priority': 'medium',
                'suggestion': f'Consider learning in-demand skills: {", ".join(missing_demand[:3])}',
                'resources': ['Coursera', 'Udemy', 'LinkedIn Learning']
            })
        
        # Check for soft skills
        soft_skills = [s for s in skill_names if s in ['communication', 'leadership', 'teamwork', 'problem solving']]
        if len(soft_skills) < 2:
            suggestions.append({
                'type': 'soft_skill',
                'priority': 'medium',
                'suggestion': 'Add soft skills like communication, teamwork, and problem-solving.',
                'resources': ['Soft skills training', 'Communication courses']
            })
        
        # Check for certifications
        certs = parsed_data.get('certifications', [])
        if not certs and experience > 0:
            suggestions.append({
                'type': 'certification',
                'priority': 'low',
                'suggestion': 'Consider getting professional certifications to boost your profile.',
                'resources': ['AWS Certification', 'Google Professional Certificates']
            })
        
        # Check for projects
        if not projects and experience == 0:
            suggestions.append({
                'type': 'project',
                'priority': 'high',
                'suggestion': 'Add personal projects to demonstrate your skills, especially since you have no work experience.',
                'resources': ['GitHub', 'Personal portfolio', 'Open source contributions']
            })
        
        # Check for education
        if not education:
            suggestions.append({
                'type': 'education',
                'priority': 'high',
                'suggestion': 'Include your educational background.',
                'resources': ['Add degrees', 'Certifications', 'Courses']
            })
        
        return suggestions
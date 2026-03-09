# backend/api/ml_models/career_knowledge_base.py

class CareerKnowledgeBase:
    """
    Comprehensive knowledge base for all job-related queries
    """
    
    @staticmethod
    def get_all_documents():
        """Return all career knowledge documents"""
        return [
            # ========== RESUME & CV ==========
            {
                'id': 'resume_001',
                'category': 'resume',
                'title': 'How to Write a Resume',
                'content': """
                To write an effective resume:
                1. Start with a strong summary that highlights your key qualifications
                2. List your work experience in reverse chronological order
                3. Use bullet points with quantifiable achievements (e.g., "Increased sales by 30%")
                4. Include relevant skills section with technical and soft skills
                5. Add education and certifications
                6. Keep it to 1-2 pages maximum
                7. Use a clean, professional format
                8. Tailor your resume for each job application
                9. Proofread carefully for errors
                10. Save as PDF to preserve formatting
                """
            },
            {
                'id': 'resume_002',
                'category': 'resume',
                'title': 'Resume Tips for Freshers',
                'content': """
                For fresh graduates with no experience:
                - Focus on education, projects, and internships
                - Include relevant coursework and academic achievements
                - List technical skills and tools you've learned
                - Add volunteer work and extracurricular activities
                - Highlight soft skills like communication and teamwork
                - Include a link to your portfolio or GitHub
                - Mention any certifications or online courses
                - Use a functional resume format if needed
                - Emphasize your willingness to learn
                - Add a strong objective statement
                """
            },
            {
                'id': 'resume_003',
                'category': 'resume',
                'title': 'ATS-Friendly Resume Tips',
                'content': """
                To make your resume ATS-friendly:
                - Use standard fonts like Arial, Calibri, or Times New Roman
                - Avoid columns, tables, and graphics
                - Use standard section headings (Experience, Education, Skills)
                - Include keywords from the job description
                - Save as .docx or .txt format, not PDF
                - Use bullet points with simple formatting
                - Avoid headers and footers
                - Spell out abbreviations
                - Use both full forms and acronyms (e.g., "Search Engine Optimization (SEO)")
                - Test your resume with online ATS simulators
                """
            },
            
            # ========== INTERVIEWS ==========
            {
                'id': 'interview_001',
                'category': 'interview',
                'title': 'Common Interview Questions',
                'content': """
                Common interview questions:
                1. Tell me about yourself
                2. Why do you want to work here?
                3. What are your strengths and weaknesses?
                4. Where do you see yourself in 5 years?
                5. Why did you leave your last job?
                6. Tell me about a challenge you faced and how you overcame it
                7. How do you handle pressure or stress?
                8. What are your salary expectations?
                9. Do you have any questions for us?
                10. Describe your ideal work environment
                
                How to answer:
                - Use the STAR method (Situation, Task, Action, Result)
                - Be honest and authentic
                - Relate answers to the job requirements
                - Show enthusiasm for the role
                - Prepare specific examples
                """
            },
            {
                'id': 'interview_002',
                'category': 'interview',
                'title': 'Technical Interview Preparation',
                'content': """
                How to prepare for technical interviews:
                
                For Software Engineering:
                - Practice coding on LeetCode, HackerRank
                - Review data structures and algorithms
                - Understand system design concepts
                - Be ready to explain your past projects
                - Practice whiteboarding
                
                For Data Science:
                - Review statistics and machine learning concepts
                - Practice SQL queries
                - Be ready to explain model evaluation metrics
                - Prepare case study examples
                - Know your tools (Python, R, SQL)
                
                General Tips:
                - Research the company's tech stack
                - Prepare questions for the interviewers
                - Practice explaining your thought process
                - Review fundamental concepts
                - Get good sleep before the interview
                """
            },
            {
                'id': 'interview_003',
                'category': 'interview',
                'title': 'Behavioral Interview Questions',
                'content': """
                Behavioral questions using STAR method:
                
                S - Situation: Set the context
                T - Task: Describe the responsibility
                A - Action: Explain what you did
                R - Result: Share the outcome
                
                Common behavioral questions:
                1. Tell me about a time you led a team
                2. Describe a conflict and how you resolved it
                3. Give an example of a goal you achieved
                4. Tell me about a time you failed
                5. Describe a situation where you had to learn quickly
                6. How do you handle multiple priorities?
                7. Tell me about a time you went above and beyond
                8. Describe a situation where you had to persuade others
                9. How do you handle criticism?
                10. Tell me about a time you innovated
                """
            },
            
            # ========== SALARY NEGOTIATION ==========
            {
                'id': 'salary_001',
                'category': 'salary',
                'title': 'Salary Negotiation Tips',
                'content': """
                How to negotiate your salary:
                
                Before the interview:
                - Research market rates for your role and location
                - Use sites like Glassdoor, Payscale, LinkedIn Salary
                - Know your minimum acceptable salary
                - Consider total compensation (bonus, equity, benefits)
                
                During negotiation:
                - Never give the first number if possible
                - Let them make the first offer
                - Provide a range, not a fixed number
                - Justify your ask with research and your value
                - Consider the entire package, not just base salary
                - Be professional and positive
                
                What to say:
                - "Based on my research and experience, I'm looking for..."
                - "I'm very excited about this role. Can we discuss the compensation package?"
                - "Is there flexibility in the salary range?"
                - "What does the total compensation package include?"
                
                Common mistakes:
                - Accepting too quickly
                - Not negotiating at all
                - Being aggressive or entitled
                - Focusing only on base salary
                - Not knowing your market value
                """
            },
            {
                'id': 'salary_002',
                'category': 'salary',
                'title': 'Salary Ranges by Role',
                'content': """
                Approximate salary ranges for common roles (US market, varies by location):
                
                Entry Level (0-2 years):
                - Software Engineer: $70,000 - $95,000
                - Data Analyst: $60,000 - $80,000
                - Marketing Coordinator: $45,000 - $60,000
                - Sales Development Rep: $40,000 - $55,000 + commission
                - HR Assistant: $40,000 - $55,000
                
                Mid Level (3-5 years):
                - Software Engineer: $95,000 - $130,000
                - Data Scientist: $100,000 - $140,000
                - Product Manager: $100,000 - $140,000
                - Marketing Manager: $70,000 - $100,000
                - Account Executive: $60,000 - $85,000 + commission
                
                Senior Level (6+ years):
                - Senior Software Engineer: $130,000 - $170,000
                - Lead Data Scientist: $140,000 - $180,000
                - Senior Product Manager: $140,000 - $180,000
                - Engineering Manager: $160,000 - $210,000
                - Director of Marketing: $120,000 - $160,000
                
                For India market (in INR, approximate):
                Entry Level: ₹3,00,000 - ₹6,00,000
                Mid Level: ₹8,00,000 - ₹15,00,000
                Senior Level: ₹18,00,000 - ₹30,00,000+
                """
            },
            
            # ========== CAREER PATHS ==========
            {
                'id': 'career_001',
                'category': 'career_path',
                'title': 'Software Development Career Path',
                'content': """
                Career progression in software development:
                
                Entry Level (0-2 years):
                - Junior Developer
                - Associate Software Engineer
                - Focus: Learning, implementing features, fixing bugs
                
                Mid Level (3-5 years):
                - Software Engineer
                - Full Stack Developer
                - Focus: Independent work, mentoring juniors, project ownership
                
                Senior Level (5-8 years):
                - Senior Software Engineer
                - Tech Lead
                - Focus: Architecture, mentoring, technical decisions
                
                Lead/Management (8+ years):
                - Lead Engineer
                - Engineering Manager
                - Focus: Team leadership, strategy, people management
                
                Architect/Specialist (8+ years):
                - Software Architect
                - Principal Engineer
                - Focus: System design, technical vision, innovation
                
                Skills to advance:
                - Deepen technical expertise
                - Learn system design and architecture
                - Develop communication and leadership skills
                - Understand business context
                - Build your network
                - Contribute to open source
                """
            },
            {
                'id': 'career_002',
                'category': 'career_path',
                'title': 'Data Science Career Path',
                'content': """
                Career progression in data science:
                
                Entry Level (0-2 years):
                - Junior Data Analyst
                - Associate Data Scientist
                - Focus: Data cleaning, basic analysis, visualization
                
                Mid Level (3-5 years):
                - Data Scientist
                - Machine Learning Engineer
                - Focus: Model development, feature engineering, deployment
                
                Senior Level (5-8 years):
                - Senior Data Scientist
                - Lead ML Engineer
                - Focus: Advanced modeling, project leadership, mentoring
                
                Lead/Management (8+ years):
                - Data Science Manager
                - Head of Analytics
                - Focus: Team leadership, strategy, stakeholder management
                
                Specialist (8+ years):
                - Principal Data Scientist
                - AI Researcher
                - Focus: Research, innovation, cutting-edge techniques
                
                Skills to advance:
                - Master statistics and ML algorithms
                - Learn big data technologies
                - Develop business acumen
                - Improve communication skills
                - Build domain expertise
                - Stay updated with research
                """
            },
            
            # ========== JOB SEARCH ==========
            {
                'id': 'jobsearch_001',
                'category': 'job_search',
                'title': 'Effective Job Search Strategies',
                'content': """
                How to find your next job:
                
                1. Update your LinkedIn profile
                   - Professional photo
                   - Detailed experience
                   - Skills section
                   - Recommendations
                
                2. Network actively
                   - Attend industry events
                   - Join professional groups
                   - Connect with recruiters
                   - Informational interviews
                
                3. Use multiple job boards
                   - LinkedIn Jobs
                   - Indeed
                   - Glassdoor
                   - AngelList (startups)
                   - Company career pages
                
                4. Work with recruiters
                   - Specialized recruiters for your field
                   - Be clear about your preferences
                   - Stay in touch
                
                5. Apply strategically
                   - Quality over quantity
                   - Tailor each application
                   - Follow up after applying
                
                6. Prepare your materials
                   - Updated resume
                   - Cover letter template
                   - Portfolio/GitHub
                   - References ready
                
                7. Track your applications
                   - Spreadsheet with company, role, status
                   - Notes on each interaction
                   - Follow-up reminders
                """
            },
            {
                'id': 'jobsearch_002',
                'category': 'job_search',
                'title': 'How to Research Companies',
                'content': """
                Research companies before applying:
                
                What to look for:
                - Company size and stage (startup vs enterprise)
                - Funding and financial health
                - Culture and values
                - Tech stack (for technical roles)
                - Recent news and developments
                - Employee reviews on Glassdoor
                - Leadership team
                
                Where to research:
                - Company website and blog
                - LinkedIn company page
                - Glassdoor reviews
                - Crunchbase for funding info
                - Twitter/LinkedIn for updates
                - News articles
                - Employee LinkedIn profiles
                
                Questions to answer:
                - Is the company growing?
                - What do employees say about working there?
                - What technologies do they use?
                - Who are their competitors?
                - What's their mission and vision?
                - Would you be proud to work there?
                
                Use this research in:
                - Your cover letter
                - Interview answers
                - Questions for interviewers
                - Salary negotiations
                """
            },
            
            # ========== NETWORKING ==========
            {
                'id': 'networking_001',
                'category': 'networking',
                'title': 'Professional Networking Tips',
                'content': """
                How to build your professional network:
                
                Online Networking:
                - Optimize your LinkedIn profile
                - Share industry-relevant content
                - Comment on posts from people in your field
                - Join LinkedIn groups
                - Connect with a personalized message
                - Engage with your network regularly
                
                In-person Networking:
                - Attend industry conferences
                - Go to local meetups
                - Participate in workshops
                - Volunteer at events
                - Prepare an elevator pitch
                - Follow up with new contacts
                
                Informational Interviews:
                - Reach out to people in roles you want
                - Prepare thoughtful questions
                - Respect their time (30 min max)
                - Ask for advice, not a job
                - Send a thank-you note
                
                Maintaining relationships:
                - Check in periodically
                - Congratulate on achievements
                - Share relevant articles
                - Offer help when you can
                - Be genuine and authentic
                
                Common mistakes:
                - Only reaching out when you need something
                - Not personalizing connection requests
                - Being too pushy
                - Not following up
                - Neglecting your network
                """
            },
            
            # ========== WORKPLACE ==========
            {
                'id': 'workplace_001',
                'category': 'workplace',
                'title': 'Work-Life Balance Tips',
                'content': """
                How to maintain work-life balance:
                
                Set boundaries:
                - Define your work hours and stick to them
                - Don't check email after hours
                - Learn to say no
                - Take your full lunch break
                - Use vacation days
                
                Manage time effectively:
                - Prioritize tasks
                - Use time-blocking
                - Take breaks throughout the day
                - Avoid multitasking
                - Delegate when possible
                
                Remote work tips:
                - Create a dedicated workspace
                - Maintain a routine
                - Take regular breaks
                - Connect with colleagues virtually
                - Set clear end-of-day rituals
                
                Prevent burnout:
                - Recognize the signs (exhaustion, cynicism)
                - Take mental health days
                - Exercise regularly
                - Get enough sleep
                - Pursue hobbies outside work
                - Talk to someone if struggling
                
                Talk to your manager:
                - Be honest about your capacity
                - Discuss workload concerns
                - Suggest solutions
                - Ask for flexibility if needed
                - Use company wellness resources
                """
            }
        ]

    @staticmethod
    def get_documents_by_category(category):
        """Get documents for a specific category"""
        all_docs = CareerKnowledgeBase.get_all_documents()
        return [doc for doc in all_docs if doc['category'] == category]
    
    @staticmethod
    def search_by_keyword(keyword):
        """Simple keyword search"""
        all_docs = CareerKnowledgeBase.get_all_documents()
        keyword_lower = keyword.lower()
        results = []
        
        for doc in all_docs:
            if keyword_lower in doc['content'].lower() or keyword_lower in doc['title'].lower():
                results.append(doc)
        
        return results
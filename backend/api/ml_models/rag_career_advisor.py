# backend/api/ml_models/rag_career_advisor.py

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from .career_knowledge_base import CareerKnowledgeBase
from .job_classifier import JobQueryClassifier

class RAGCareerAdvisor:
    """
    Retrieval-Augmented Generation for career advice
    """
    
    def __init__(self, index_path=None):
        # Initialize components
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier = JobQueryClassifier()
        self.knowledge_base = CareerKnowledgeBase()
        
        # Paths for saving/loading index
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_path = index_path or os.path.join(self.base_dir, '../../../data/career_faiss.index')
        self.docs_path = os.path.join(self.base_dir, '../../../data/career_docs.pkl')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        # Initialize or load index
        self.index = None
        self.documents = []
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize or load the FAISS index"""
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            # Load existing index
            self.index = faiss.read_index(self.index_path)
            with open(self.docs_path, 'rb') as f:
                self.documents = pickle.load(f)
            print(f"✅ Loaded {len(self.documents)} documents from index")
        else:
            # Build new index from knowledge base
            self._build_index()
    
    def _build_index(self):
        """Build FAISS index from knowledge base"""
        print("🔨 Building career knowledge index...")
        
        # Get all documents
        all_docs = self.knowledge_base.get_all_documents()
        
        if not all_docs:
            print("⚠️ No documents found in knowledge base")
            return
        
        # Prepare texts for embedding
        texts = []
        self.documents = []
        
        for doc in all_docs:
            # Combine title and content for better search
            text = f"{doc['title']}\n{doc['content']}"
            texts.append(text)
            self.documents.append({
                'id': doc['id'],
                'category': doc['category'],
                'title': doc['title'],
                'content': doc['content'],
                'text': text
            })
        
        # Create embeddings
        print(f"📊 Creating embeddings for {len(texts)} documents...")
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        # Save index and documents
        faiss.write_index(self.index, self.index_path)
        with open(self.docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
        
        print(f"✅ Built index with {len(self.documents)} documents")
    
    def search(self, query, k=5):
        """
        Search for relevant career documents
        Returns list of (document, score) tuples
        """
        if self.index is None or not self.documents:
            return []
        
        # Create query embedding
        query_embedding = self.embedder.encode([query])
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), min(k, len(self.documents)))
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.documents):
                # Convert distance to similarity score (lower distance = better)
                similarity = 1 / (1 + distances[0][i])
                results.append({
                    'document': self.documents[idx],
                    'score': float(similarity),
                    'distance': float(distances[0][i])
                })
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def generate_response(self, question, user_skills=None, experience=None):
        """
        Generate career advice response
        """
        # First, classify the question
        classification = self.classifier.classify(question)
        
        # If not job-related, return appropriate message
        if not classification['is_job_related']:
            return {
                'answer': "I'm a career advisor assistant and can only help with job-related questions. Please ask me about resumes, interviews, career paths, salary negotiations, or job searching.",
                'is_job_related': False,
                'category': None,
                'sources': []
            }
        
        # Extract entities (roles, skills)
        entities = self.classifier.extract_entities(question)
        
        # Enhance query with classification for better search
        enhanced_query = question
        if classification['primary_category']:
            enhanced_query = f"[{classification['primary_category']}] {question}"
        
        # Search for relevant documents
        search_results = self.search(enhanced_query, k=3)
        
        # If no results from search, try keyword search in knowledge base
        if not search_results:
            # Fallback to keyword search
            keyword_results = self.knowledge_base.search_by_keyword(question)
            if keyword_results:
                # Format keyword results
                answer = self._format_documents_answer(keyword_results, question, entities, classification)
                return {
                    'answer': answer,
                    'is_job_related': True,
                    'category': classification['primary_category'],
                    'sources': keyword_results,
                    'search_method': 'keyword'
                }
            else:
                # Generic response based on category
                answer = self._get_generic_response(classification['primary_category'], question, entities)
                return {
                    'answer': answer,
                    'is_job_related': True,
                    'category': classification['primary_category'],
                    'sources': []
                }
        
        # Format answer from search results
        answer = self._format_search_results(search_results, question, entities, classification)
        
        return {
            'answer': answer,
            'is_job_related': True,
            'category': classification['primary_category'],
            'sources': [r['document'] for r in search_results[:2]],
            'search_method': 'vector'
        }
    
    def _format_search_results(self, results, question, entities, classification):
        """Format search results into a coherent answer"""
        
        # Start with a greeting based on category
        category_names = {
            'resume': "resume",
            'interview': "interview",
            'salary': "salary",
            'career_path': "career path",
            'job_search': "job search",
            'networking': "networking",
            'workplace': "workplace"
        }
        
        category = classification['primary_category']
        category_name = category_names.get(category, "career")
        
        # Build answer
        answer_parts = []
        
        # Introduction
        if entities['roles'] or entities['skills']:
            role_text = f" for {', '.join(entities['roles'])}" if entities['roles'] else ""
            skill_text = f" with skills in {', '.join(entities['skills'])}" if entities['skills'] else ""
            answer_parts.append(f"Here's advice about {category_name}{role_text}{skill_text}:\n")
        else:
            answer_parts.append(f"Here's some helpful {category_name} advice:\n")
        
        # Add content from top results
        for i, result in enumerate(results[:2]):
            doc = result['document']
            answer_parts.append(f"\n📌 {doc['title']}:")
            # Get first few sentences of content
            content_lines = doc['content'].strip().split('\n')
            preview = '\n'.join(content_lines[:min(5, len(content_lines))])
            answer_parts.append(preview)
        
        # Add follow-up suggestion
        answer_parts.append("\n\nWould you like more specific information about this topic?")
        
        return '\n'.join(answer_parts)
    
    def _format_documents_answer(self, docs, question, entities, classification):
        """Format multiple documents into answer"""
        answer_parts = [f"I found some information that might help:\n"]
        
        for i, doc in enumerate(docs[:3]):
            answer_parts.append(f"\n📌 {doc['title']}:")
            content_lines = doc['content'].strip().split('\n')
            preview = '\n'.join(content_lines[:min(4, len(content_lines))])
            answer_parts.append(preview)
        
        answer_parts.append("\n\nIs there a specific aspect you'd like to know more about?")
        
        return '\n'.join(answer_parts)
    
    def _get_generic_response(self, category, question, entities):
        """Provide generic response when no specific information found"""
        
        generic_responses = {
            'resume': """
I don't have specific information about that resume question, but here are general resume tips:
- Keep your resume concise (1-2 pages)
- Use action verbs and quantify achievements
- Tailor your resume for each job application
- Include relevant keywords from the job description
- Proofread carefully for errors

Would you like to ask about a specific aspect of resume writing?
            """,
            'interview': """
I don't have specific information about that interview question, but here are general interview tips:
- Research the company beforehand
- Prepare stories using the STAR method
- Practice common interview questions
- Prepare thoughtful questions to ask
- Follow up with a thank-you note

What specific aspect of interviewing would you like help with?
            """,
            'salary': """
I don't have specific salary information for that query, but here are general salary negotiation tips:
- Research market rates for your role and location
- Know your minimum acceptable salary
- Consider total compensation (bonus, benefits, equity)
- Practice your negotiation conversation
- Be professional and positive

Would you like to ask about salary for a specific role?
            """,
            'career_path': """
I don't have specific information about that career path, but here's general career advice:
- Identify your interests and strengths
- Research roles that match your skills
- Network with people in your target field
- Consider additional education or certifications
- Set short-term and long-term career goals

What specific career path are you interested in?
            """
        }
        
        return generic_responses.get(category, """
I don't have specific information about that question. Could you please rephrase or ask about a different aspect of your career?

I can help with:
- Resume writing and review
- Interview preparation
- Salary negotiations
- Career path planning
- Job search strategies
- Professional networking
        """)
# scripts/build_knowledge_base.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.ml_models.rag_career_advisor import RAGCareerAdvisor

def main():
    print("="*50)
    print("🔨 Building Career Knowledge Base")
    print("="*50)
    
    # Initialize advisor (will build index automatically)
    advisor = RAGCareerAdvisor()
    
    print("\n✅ Knowledge base built successfully!")
    print(f"📊 Total documents indexed: {len(advisor.documents)}")
    
    # Test a few queries
    test_queries = [
        "How to write a resume?",
        "What questions are asked in technical interviews?",
        "How to negotiate salary?",
        "What is the career path for a software engineer?",
        "Tell me about networking"
    ]
    
    print("\n" + "="*50)
    print("🧪 Testing Search Functionality")
    print("="*50)
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        results = advisor.search(query, k=2)
        print(f"✅ Found {len(results)} relevant documents")
        for i, result in enumerate(results[:2]):
            print(f"  {i+1}. {result['document']['title']} (score: {result['score']:.2f})")
    
    print("\n✅ Build complete!")

if __name__ == "__main__":
    main()
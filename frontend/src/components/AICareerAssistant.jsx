import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './AICareerAssistant.css';

function AICareerAssistant({ skills = [], experience = 0 }) {
  const [question, setQuestion] = useState('');
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState('light');
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  // Load theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, []);

  // Scroll to bottom when conversation updates
  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    
    // Add user message with timestamp
    const userMessage = { 
      role: 'user', 
      text: question,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    
    const newConversation = [...conversation, userMessage];
    setConversation(newConversation);
    
    try {
      // Call your RAG-enhanced backend
      const response = await axios.post('http://localhost:8000/api/free-ai-advice/', {
        question: question,
        skills: skills || [],
        experience: experience || 0
      });
      
      // Add AI response with metadata
      setConversation([...newConversation, { 
        role: 'ai', 
        text: response.data.answer,
        category: response.data.category,
        isJobRelated: response.data.is_job_related,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
      
    } catch (error) {
      console.error('Error:', error);
      
      // Friendly error message
      let errorMessage = "I'm having trouble connecting. Please check your internet connection and try again.";
      
      if (error.response?.status === 429) {
        errorMessage = "Too many requests. Please wait a moment before asking another question.";
      } else if (error.response?.status === 500) {
        errorMessage = "Server error. Our team has been notified. Please try again later.";
      }
      
      setConversation([...newConversation, { 
        role: 'ai', 
        text: errorMessage,
        isError: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setLoading(false);
      setQuestion('');
      // Focus back on input
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAskQuestion();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuestion(suggestion);
    // Auto-submit after short delay
    setTimeout(() => {
      handleAskQuestion();
    }, 100);
  };

  const formatMessage = (text) => {
    // Simple formatting for bullet points
    if (text.includes('⭐️')) {
      return text.split('⭐️').map((part, index) => {
        if (index === 0) return part;
        return (
          <div key={index} className="tip-item">
            <span className="tip-icon">⭐️</span>
            <span>{part}</span>
          </div>
        );
      });
    }
    return text;
  };

  return (
    <div className="ai-assistant">
      <div className="assistant-header">
        <h2>AI Career Assistant</h2>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span className="job-badge">Job-Specific AI</span>
          <button 
            onClick={toggleTheme}
            style={{
              background: 'rgba(255,255,255,0.2)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '30px',
              padding: '0.4rem 1rem',
              color: 'white',
              cursor: 'pointer',
              fontSize: '0.85rem'
            }}
          >
            {theme === 'light' ? '🌙 Dark' : '☀️ Light'}
          </button>
        </div>
      </div>
      
      <div className="chat-area">
        {conversation.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '3rem',
            color: 'var(--text-muted)'
          }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>👋</div>
            <h3>Welcome to AI Career Assistant!</h3>
            <p>Ask me anything about resumes, interviews, career paths, or job searching.</p>
          </div>
        ) : (
          conversation.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-content">
                <div className="message-header">
                  <span className="message-role">
                    {msg.role === 'user' ? 'You' : 'AI Assistant'}
                  </span>
                  {msg.role === 'ai' && msg.isJobRelated && (
                    <span className="job-badge" style={{ fontSize: '0.7rem', padding: '0.2rem 0.6rem' }}>
                      Job-Specific
                    </span>
                  )}
                  <span className="message-time">{msg.timestamp}</span>
                </div>
                <div className="message-text">
                  {msg.role === 'ai' ? formatMessage(msg.text) : msg.text}
                </div>
                {msg.category && (
                  <span className="category-tag">
                    📌 {msg.category}
                  </span>
                )}
              </div>
            </div>
          ))
        )}
        
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Finding the best career advice for you...</p>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <input
          ref={inputRef}
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about resumes, interviews, careers..."
          disabled={loading}
        />
        <button onClick={handleAskQuestion} disabled={loading || !question.trim()}>
          {loading ? '...' : 'Ask'}
        </button>
      </div>

      <div className="suggestions">
        <p>Try asking:</p>
        <div className="suggestions-buttons">
          <button onClick={() => handleSuggestionClick("How to write a resume?")}>
            📄 Resume tips
          </button>
          <button onClick={() => handleSuggestionClick("Common interview questions")}>
            🎤 Interview prep
          </button>
          <button onClick={() => handleSuggestionClick("Salary negotiation tips")}>
            💰 Salary advice
          </button>
          <button onClick={() => handleSuggestionClick("Career path for software engineer")}>
            🚀 Career path
          </button>
          <button onClick={() => handleSuggestionClick("Skills to learn for data science")}>
            📊 Skill recommendations
          </button>
          <button onClick={() => handleSuggestionClick("How to switch careers")}>
            🔄 Career change
          </button>
        </div>
      </div>
    </div>
  );
}

export default AICareerAssistant;
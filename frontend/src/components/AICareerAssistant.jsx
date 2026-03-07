import React, { useState } from 'react';
import axios from 'axios';
import './AICareerAssistant.css';

function AICareerAssistant({ skills, experience }) {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversation, setConversation] = useState([]);

  // Predefined questions for quick access
  const predefinedQuestions = [
    "How can I join an MNC?",
    "What skills should I learn next?",
    "How much salary can I expect?",
    "What certifications would help?",
    "Which companies are hiring?"
  ];

  const handleAskQuestion = async (q) => {
    if (!q.trim()) return;
    
    setLoading(true);
    
    // Add user question to conversation
    const updatedConversation = [...conversation, { role: 'user', text: q }];
    setConversation(updatedConversation);
    setQuestion('');

    try {
      // Format skills properly for the backend
      const formattedSkills = skills ? skills.map(s => {
        if (typeof s === 'string') return s;
        return s.name || '';
      }).filter(s => s) : [];
      
      // Call backend API
      const response = await axios.post('http://localhost:8000/api/free-ai-advice/', {
        question: q,
        skills: formattedSkills,
        experience: experience || 0,
        conversation_history: updatedConversation.slice(-6) // Last 3 exchanges
      });

      // Get answer from response
      const answer = response.data.answer || response.data.message || "I'm not sure how to answer that.";
      
      // Add AI response to conversation
      setConversation(prev => [...prev, { role: 'ai', text: answer }]);
      
    } catch (error) {
      console.error('Error getting AI advice:', error);
      
      // Handle different error types
      let errorMsg = "I'm having trouble connecting right now. ";
      
      if (error.response) {
        // The request was made and the server responded with a status code
        if (error.response.status === 500) {
          errorMsg += "The AI service is temporarily unavailable.";
        } else if (error.response.data && error.response.data.error) {
          errorMsg += error.response.data.error;
        } else {
          errorMsg += "Please try again later.";
        }
      } else if (error.request) {
        // The request was made but no response received
        errorMsg += "Cannot reach the server. Make sure Django backend is running on port 8000.";
      } else {
        // Something happened in setting up the request
        errorMsg += "Please check your connection and try again.";
      }
      
      setConversation(prev => [...prev, { role: 'ai', text: errorMsg }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-assistant">
      <div className="assistant-header">
        <h2>🤖 AI Career Assistant</h2>
        <span className="free-badge">FREE AI</span>
      </div>
      
      <p className="assistant-subtitle">
        Ask me anything about your career! (Powered by Gemini AI - 100% Free)
      </p>

      <div className="quick-questions">
        {predefinedQuestions.map((q, i) => (
          <button
            key={i}
            className="question-chip"
            onClick={() => handleAskQuestion(q)}
            disabled={loading}
          >
            {q}
          </button>
        ))}
      </div>

      <div className="chat-area">
        {conversation.length === 0 ? (
          <div className="welcome-message">
            <p>👋 Hi! I'm your AI career assistant. Ask me anything about:</p>
            <ul>
              <li>🎯 How to join MNCs and prepare for interviews</li>
              <li>📚 Skills to learn based on your profile</li>
              <li>💰 Salary expectations in your field</li>
              <li>🏢 Companies hiring in your domain</li>
              <li>📝 Resume and certification tips</li>
            </ul>
          </div>
        ) : (
          conversation.map((msg, index) => (
            <div 
              key={index} 
              className={`message ${msg.role === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <div className="message-avatar">
                {msg.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <strong>{msg.role === 'user' ? 'You' : 'AI Assistant'}</strong>
                <p>{msg.text}</p>
              </div>
            </div>
          ))
        )}
        
        {loading && (
          <div className="ai-thinking">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span>AI is thinking...</span>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion(question)}
          placeholder="Type your career question here..."
          disabled={loading}
        />
        <button 
          className="btn btn-primary"
          onClick={() => handleAskQuestion(question)}
          disabled={!question.trim() || loading}
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>
      
      <div className="ai-footer">
        <p className="free-tier-note">
          ✨ Powered by Google Gemini AI - 1,500 free requests per day
        </p>
        {skills && skills.length > 0 && (
          <p className="context-note">
            📊 Using your skills: {skills.slice(0, 3).map(s => {
              if (typeof s === 'string') return s;
              return s.name || '';
            }).join(', ')}
            {skills.length > 3 && ` +${skills.length - 3} more`}
          </p>
        )}
      </div>
    </div>
  );
}

export default AICareerAssistant;
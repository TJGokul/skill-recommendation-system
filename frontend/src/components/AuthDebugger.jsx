import React, { useState, useEffect } from 'react';
import api from '../services/api';

function AuthDebugger() {
  const [debugInfo, setDebugInfo] = useState({
    cookies: '',
    testResults: {},
    loading: false
  });

  useEffect(() => {
    checkAllEndpoints();
  }, []);

  const checkAllEndpoints = async () => {
    setDebugInfo(prev => ({ ...prev, loading: true }));
    
    // Check cookies
    const cookies = document.cookie || 'No cookies found';
    console.log('Current cookies:', cookies);

    const results = {};

    // Test 1: Test endpoint (public)
    try {
      console.log('Testing /api/test/...');
      const testRes = await api.get('/test/');
      results.test = { 
        success: true, 
        status: testRes.status,
        data: testRes.data 
      };
      console.log('Test endpoint success:', testRes.data);
    } catch (err) {
      console.error('Test endpoint failed:', err);
      results.test = { 
        success: false, 
        message: err.message,
        response: err.response?.data
      };
    }

    // Test 2: User endpoint (protected)
    try {
      console.log('Testing /api/user/...');
      const userRes = await api.get('/user/');
      results.user = { 
        success: true, 
        status: userRes.status,
        data: userRes.data 
      };
      console.log('User endpoint success:', userRes.data);
    } catch (err) {
      console.error('User endpoint failed:', err);
      results.user = { 
        success: false, 
        message: err.message,
        status: err.response?.status,
        data: err.response?.data
      };
    }

    setDebugInfo({
      cookies,
      testResults: results,
      loading: false
    });
  };

  const testLogin = async () => {
    const username = prompt("Enter username:");
    const password = prompt("Enter password:");
    
    if (!username || !password) return;

    try {
      console.log('Attempting login...');
      const response = await api.post('/login/', { username, password });
      console.log('Login response:', response.data);
      alert('Login successful!');
      checkAllEndpoints();
    } catch (err) {
      console.error('Login error:', err);
      alert(`Login failed: ${err.response?.data?.error || err.message}`);
    }
  };

  const copyDebugInfo = () => {
    const info = {
      cookies: debugInfo.cookies,
      testResults: debugInfo.testResults,
      userAgent: navigator.userAgent,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };
    navigator.clipboard.writeText(JSON.stringify(info, null, 2));
    alert('Debug info copied to clipboard!');
  };

  return (
    <div style={{
      padding: '20px',
      margin: '20px',
      border: '3px solid #ff6b6b',
      borderRadius: '12px',
      background: '#fff3f3',
      fontFamily: 'monospace',
      fontSize: '14px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
        <h2 style={{ margin: 0, color: '#d32f2f' }}>🔐 Authentication Debugger</h2>
        <button onClick={copyDebugInfo}>📋 Copy</button>
      </div>
      
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button onClick={checkAllEndpoints}>🔄 Refresh</button>
        <button onClick={testLogin} style={{ background: '#4caf50', color: 'white' }}>
          🔑 Test Login
        </button>
      </div>

      <div style={{ background: '#fff', padding: '15px', borderRadius: '8px' }}>
        <p><strong>🍪 Cookies:</strong> {debugInfo.cookies}</p>
        <p><strong>⏳ Loading:</strong> {debugInfo.loading ? 'Yes' : 'No'}</p>
        
        <div>
          <strong>📡 Test Results:</strong>
          <pre style={{ background: '#f5f5f5', padding: '10px', overflow: 'auto' }}>
            {JSON.stringify(debugInfo.testResults, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}

export default AuthDebugger;
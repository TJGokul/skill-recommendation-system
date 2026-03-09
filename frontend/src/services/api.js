// frontend/src/services/api.js
import axios from 'axios';

// Use relative URL - will be handled by Vite proxy
const api = axios.create({
  baseURL: '/api',  // Changed from http://127.0.0.1:8000/api
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Force withCredentials for all requests
api.defaults.withCredentials = true;

export const getCSRFToken = () => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
};

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    console.log('🍪 Cookies:', document.cookie);
    
    // Check if session cookie exists
    if (!document.cookie.includes('sessionid')) {
      console.warn('⚠️ No session cookie found!');
    }
    
    // Add CSRF token for POST requests
    if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase())) {
      const csrfToken = getCSRFToken();
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
        console.log('🔑 Added CSRF token');
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.status} from ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.log('🔒 Session expired - redirecting to login');
    }
    return Promise.reject(error);
  }
);

export default api;
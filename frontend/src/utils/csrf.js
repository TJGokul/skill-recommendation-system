// frontend/src/utils/csrf.js

export function getCSRFToken() {
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
}

export function setCSRFTokenHeader() {
  const csrfToken = getCSRFToken();
  return {
    'X-CSRFToken': csrfToken,
    'Content-Type': 'application/json',
  };
}
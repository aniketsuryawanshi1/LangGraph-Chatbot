import axios from "axios";

// API Base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error("API Error:", error);

    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.message || "Server error occurred");
    } else if (error.request) {
      // Request made but no response
      throw new Error("No response from server. Please check your connection.");
    } else {
      // Something else happened
      throw new Error(error.message || "An error occurred");
    }
  }
);

/**
 * Send a chat message
 * @param {string} query - User's message
 * @param {string|null} sessionId - Optional session ID
 * @returns {Promise<Object>} - Response with bot message
 */
export const sendMessage = async (query, sessionId = null) => {
  return await api.post("/chat/", {
    query,
    session_id: sessionId,
  });
};

/**
 * Get session history
 * @param {string} sessionId - Session ID
 * @param {number} limit - Number of messages to fetch
 * @returns {Promise<Object>} - Session history
 */
export const getSessionHistory = async (sessionId, limit = 20) => {
  return await api.get(`/chat/history/${sessionId}/`, {
    params: { limit },
  });
};

/**
 * Clear session history
 * @param {string} sessionId - Session ID to clear
 * @returns {Promise<Object>} - Clear confirmation
 */
export const clearSession = async (sessionId) => {
  return await api.delete(`/chat/session/${sessionId}/`);
};

/**
 * Get chatbot statistics
 * @returns {Promise<Object>} - Statistics data
 */
export const getStatistics = async () => {
  return await api.get("/chat/statistics/");
};

/**
 * Health check
 * @returns {Promise<Object>} - Health status
 */
export const healthCheck = async () => {
  return await api.get("/chat/health/");
};

export default api;

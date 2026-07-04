/**
 * API Configuration and Endpoints
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    VERIFY_TOKEN: '/auth/verify-token',
    LOGOUT: '/auth/logout'
  },

  // Users
  USERS: {
    LIST: '/users',
    GET: (id) => `/users/${id}`,
    CREATE: '/users',
    UPDATE: (id) => `/users/${id}`,
    DELETE: (id) => `/users/${id}`,
    CHANGE_STATUS: (id, status) => `/users/${id}/status/${status}`
  },

  // Books
  BOOKS: {
    LIST: '/books',
    SEARCH: '/books/search',
    GET: (id) => `/books/${id}`,
    CREATE: '/books',
    UPDATE: (id) => `/books/${id}`,
    DELETE: (id) => `/books/${id}`
  },

  // Catalog (Authors, Genres, Languages)
  CATALOG: {
    AUTHORS: '/catalog/authors',
    GENRES: '/catalog/genres',
    LANGUAGES: '/catalog/languages'
  },

  // Members
  MEMBERS: {
    LIST: '/members',
    SEARCH: '/members/search',
    GET: (id) => `/members/${id}`,
    CREATE: '/members',
    UPDATE: (id) => `/members/${id}`,
    DELETE: (id) => `/members/${id}`,
    PLANS: '/members/plans'
  },

  // Transactions (Issue/Return Books)
  TRANSACTIONS: {
    ISSUE: '/transactions/issue',
    RETURN: (issueId) => `/transactions/return/${issueId}`,
    LIST: '/transactions',
    GET: (id) => `/transactions/${id}`,
    FINES: '/transactions/fines',
    GET_FINE: (id) => `/transactions/fines/${id}`,
    PAY_FINE: (id) => `/transactions/fines/${id}/pay`
  },

  // Health Check
  HEALTH: '/health'
}

export { API_BASE_URL }

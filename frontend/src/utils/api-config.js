/**
 * API Configuration
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: `${API_BASE_URL}/auth/login`,
    REGISTER: `${API_BASE_URL}/auth/register`,
    VERIFY_TOKEN: `${API_BASE_URL}/auth/verify-token`,
  },

  // Users
  USERS: {
    LIST: `${API_BASE_URL}/users`,
    GET: (id) => `${API_BASE_URL}/users/${id}`,
    CREATE: `${API_BASE_URL}/users`,
    UPDATE: (id) => `${API_BASE_URL}/users/${id}`,
    DELETE: (id) => `${API_BASE_URL}/users/${id}`,
    UPDATE_STATUS: (id, status) => `${API_BASE_URL}/users/${id}/status/${status}`,
  },

  // Books
  BOOKS: {
    LIST: `${API_BASE_URL}/books`,
    SEARCH: `${API_BASE_URL}/books/search`,
    GET: (id) => `${API_BASE_URL}/books/${id}`,
    BY_ISBN: (isbn) => `${API_BASE_URL}/books/isbn/${isbn}`,
    CREATE: `${API_BASE_URL}/books`,
    UPDATE: (id) => `${API_BASE_URL}/books/${id}`,
    DELETE: (id) => `${API_BASE_URL}/books/${id}`,
    AVAILABLE_COPIES: (id) => `${API_BASE_URL}/books/${id}/available-copies`,
  },

  // Catalog (Languages, Genres, Authors)
  CATALOG: {
    LANGUAGES: `${API_BASE_URL}/catalog/languages`,
    GENRES: `${API_BASE_URL}/catalog/genres`,
    GENRE_UPDATE: (id) => `${API_BASE_URL}/catalog/genres/${id}`,
    GENRE_DELETE: (id) => `${API_BASE_URL}/catalog/genres/${id}`,
    AUTHORS: `${API_BASE_URL}/catalog/authors`,
    AUTHOR_GET: (id) => `${API_BASE_URL}/catalog/authors/${id}`,
    AUTHOR_UPDATE: (id) => `${API_BASE_URL}/catalog/authors/${id}`,
    AUTHOR_DELETE: (id) => `${API_BASE_URL}/catalog/authors/${id}`,
  },

  // Members
  MEMBERS: {
    LIST: `${API_BASE_URL}/members`,
    SEARCH: `${API_BASE_URL}/members/search`,
    GET: (id) => `${API_BASE_URL}/members/${id}`,
    BY_CODE: (code) => `${API_BASE_URL}/members/code/${code}`,
    CREATE: `${API_BASE_URL}/members`,
    UPDATE: (id) => `${API_BASE_URL}/members/${id}`,
    DELETE: (id) => `${API_BASE_URL}/members/${id}`,
    UPDATE_STATUS: (id, status) => `${API_BASE_URL}/members/${id}/status/${status}`,
    
    // Membership Plans
    PLANS: `${API_BASE_URL}/members/plans`,
    PLAN_GET: (id) => `${API_BASE_URL}/members/plans/${id}`,
    PLAN_UPDATE: (id) => `${API_BASE_URL}/members/plans/${id}`,
    PLAN_DELETE: (id) => `${API_BASE_URL}/members/plans/${id}`,
  },

  // Transactions (Issue/Return)
  TRANSACTIONS: {
    ISSUE: `${API_BASE_URL}/transactions/issue`,
    RETURN: (issueId) => `${API_BASE_URL}/transactions/return/${issueId}`,
    GET_ISSUE: (id) => `${API_BASE_URL}/transactions/issues/${id}`,
    MEMBER_ISSUED: (memberId) => `${API_BASE_URL}/transactions/member/${memberId}/issued`,
    OVERDUE: `${API_BASE_URL}/transactions/overdue`,
    REPORT_ISSUED: `${API_BASE_URL}/transactions/report/issued`,
    
    // Fines
    GET_FINE: (id) => `${API_BASE_URL}/transactions/fines/${id}`,
    MEMBER_FINES: (memberId) => `${API_BASE_URL}/transactions/member/${memberId}/fines`,
    OUTSTANDING_FINES: (memberId) => `${API_BASE_URL}/transactions/member/${memberId}/fines/outstanding`,
    PAY_FINE: (id) => `${API_BASE_URL}/transactions/fines/${id}/pay`,
    REPORT_FINES: `${API_BASE_URL}/transactions/report/fines`,
    LIST_FINES: `${API_BASE_URL}/transactions/fines`,
  }
}

export default API_BASE_URL

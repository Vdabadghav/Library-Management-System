/**
 * API Service Layer
 * Handles all HTTP requests to the backend
 */
import axios from 'axios'
import { API_ENDPOINTS } from './api-config'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - add token to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ==================== Authentication ====================
export const authService = {
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  
  register: (userData) =>
    api.post('/auth/register', userData),
  
  verifyToken: (token) =>
    api.post('/auth/verify-token', { token })
}

// ==================== User Management ====================
export const userService = {
  listUsers: (skip = 0, limit = 100) =>
    api.get('/users', { params: { skip, limit } }),
  
  getUser: (userId) =>
    api.get(`/users/${userId}`),
  
  createUser: (userData) =>
    api.post('/users', userData),
  
  updateUser: (userId, userData) =>
    api.put(`/users/${userId}`, userData),
  
  deleteUser: (userId) =>
    api.delete(`/users/${userId}`),
  
  updateUserStatus: (userId, status) =>
    api.patch(`/users/${userId}/status/${status}`)
}

// ==================== Book Management ====================
export const bookService = {
  listBooks: (skip = 0, limit = 100) =>
    api.get('/books', { params: { skip, limit } }),
  
  searchBooks: (params) =>
    api.get('/books/search', { params }),
  
  getBook: (bookId) =>
    api.get(`/books/${bookId}`),
  
  getBookByISBN: (isbn) =>
    api.get(`/books/isbn/${isbn}`),
  
  createBook: (bookData) =>
    api.post('/books', bookData),
  
  updateBook: (bookId, bookData) =>
    api.put(`/books/${bookId}`, bookData),
  
  deleteBook: (bookId) =>
    api.delete(`/books/${bookId}`),
  
  getAvailableCopies: (bookId) =>
    api.get(`/books/${bookId}/available-copies`)
}

// ==================== Catalog Management ====================
export const catalogService = {
  // Languages
  getLanguages: () =>
    api.get('/catalog/languages'),
  
  createLanguage: (name, code) =>
    api.post('/catalog/languages', { name, code }),
  
  deleteLanguage: (languageId) =>
    api.delete(`/catalog/languages/${languageId}`),
  
  // Genres
  getGenres: () =>
    api.get('/catalog/genres'),
  
  createGenre: (name, description) =>
    api.post('/catalog/genres', { name, description }),
  
  updateGenre: (genreId, name, description) =>
    api.put(`/catalog/genres/${genreId}`, { name, description }),
  
  deleteGenre: (genreId) =>
    api.delete(`/catalog/genres/${genreId}`),
  
  // Authors
  getAuthors: () =>
    api.get('/catalog/authors'),
  
  getAuthor: (authorId) =>
    api.get(`/catalog/authors/${authorId}`),
  
  createAuthor: (fullName, biography) =>
    api.post('/catalog/authors', { full_name: fullName, biography }),
  
  updateAuthor: (authorId, fullName, biography) =>
    api.put(`/catalog/authors/${authorId}`, { full_name: fullName, biography }),
  
  deleteAuthor: (authorId) =>
    api.delete(`/catalog/authors/${authorId}`)
}

// ==================== Member Management ====================
export const memberService = {
  // Members
  listMembers: (skip = 0, limit = 100) =>
    api.get('/members', { params: { skip, limit } }),
  
  searchMembers: (params) =>
    api.get('/members/search', { params }),
  
  getMember: (memberId) =>
    api.get(`/members/${memberId}`),
  
  getMemberByCode: (memberCode) =>
    api.get(`/members/code/${memberCode}`),
  
  createMember: (memberData) =>
    api.post('/members', memberData),
  
  updateMember: (memberId, memberData) =>
    api.put(`/members/${memberId}`, memberData),
  
  deleteMember: (memberId) =>
    api.delete(`/members/${memberId}`),
  
  updateMemberStatus: (memberId, status) =>
    api.patch(`/members/${memberId}/status/${status}`),
  
  // Membership Plans
  getPlans: () =>
    api.get('/members/plans'),
  
  getPlan: (planId) =>
    api.get(`/members/plans/${planId}`),
  
  createPlan: (planData) =>
    api.post('/members/plans', planData),
  
  updatePlan: (planId, planData) =>
    api.put(`/members/plans/${planId}`, planData),
  
  deletePlan: (planId) =>
    api.delete(`/members/plans/${planId}`)
}

// ==================== Transactions ====================
export const transactionService = {
  // Issue/Return
  issueBook: (bookId, memberId, issuedByUserId) =>
    api.post('/transactions/issue', {
      book_id: bookId,
      member_id: memberId,
      issued_by_user_id: issuedByUserId
    }),
  
  returnBook: (issueId, returnDate = null, finePaid = false) =>
    api.post(`/transactions/return/${issueId}`, {
      return_date: returnDate,
      fine_paid: finePaid
    }),
  
  getIssue: (issueId) =>
    api.get(`/transactions/issues/${issueId}`),
  
  getMemberIssuedBooks: (memberId) =>
    api.get(`/transactions/member/${memberId}/issued`),
  
  getOverdueBooks: () =>
    api.get('/transactions/overdue'),
  
  getIssuedBooksReport: (startDate, endDate, skip = 0, limit = 100) =>
    api.get('/transactions/report/issued', {
      params: { start_date: startDate, end_date: endDate, skip, limit }
    }),
  
  // Fines
  getFine: (fineId) =>
    api.get(`/transactions/fines/${fineId}`),
  
  getMemberFines: (memberId) =>
    api.get(`/transactions/member/${memberId}/fines`),
  
  getMemberOutstandingFines: (memberId) =>
    api.get(`/transactions/member/${memberId}/fines/outstanding`),
  
  markFinePaid: (fineId) =>
    api.post(`/transactions/fines/${fineId}/pay`),
  
  getFineReport: (startDate, endDate) =>
    api.get('/transactions/report/fines', {
      params: { start_date: startDate, end_date: endDate }
    }),
  
  listFines: (skip = 0, limit = 100) =>
    api.get('/transactions/fines', { params: { skip, limit } })
}

export default api

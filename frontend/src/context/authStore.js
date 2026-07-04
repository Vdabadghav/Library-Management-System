/**
 * Authentication Context
 * Manages user authentication state and JWT tokens
 */
import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  // State
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isLoading: false,
  error: null,

  // Actions
  setUser: (user) => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
    set({ user })
  },

  setToken: (token) => {
    if (token) {
      localStorage.setItem('access_token', token)
    } else {
      localStorage.removeItem('access_token')
    }
    set({ token, isAuthenticated: !!token })
  },

  setLoading: (isLoading) => set({ isLoading }),

  setError: (error) => set({ error }),

  login: (userData, token) => {
    set({ user: userData, token, isAuthenticated: true, error: null })
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('access_token', token)
  },

  logout: () => {
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null
    })
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
  },

  register: (userData) => {
    set({ user: userData, error: null })
    localStorage.setItem('user', JSON.stringify(userData))
  },

  clearError: () => set({ error: null })
}))

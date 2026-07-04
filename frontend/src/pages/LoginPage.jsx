/**
 * Login Page
 */
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/api'
import { useAuthStore } from '../context/authStore'
import '../styles/Auth.css'

function LoginPage() {
  const navigate = useNavigate()
  const { login, setError, setLoading } = useAuthStore()
  
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [error, setLocalError] = useState('')
  const [loading, setLocalLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }))
    setLocalError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLocalLoading(true)
    
    try {
      const response = await authService.login(
        formData.username,
        formData.password
      )
      
      if (response.data) {
        login(response.data.user, response.data.access_token)
        navigate('/')
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Login failed'
      setLocalError(errorMessage)
    } finally {
      setLocalLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>📚 Library Management System</h1>
        <h2>Login</h2>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="auth-link">
          Don't have an account? <a href="/register">Register here</a>
        </p>
      </div>
    </div>
  )
}

export default LoginPage

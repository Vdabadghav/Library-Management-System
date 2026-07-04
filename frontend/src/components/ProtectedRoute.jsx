/**
 * Protected Route Component
 * Ensures user is authenticated before accessing route
 */
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../context/authStore'

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute

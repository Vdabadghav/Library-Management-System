/**
 * Main Application Component
 */
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './context/authStore'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import BooksPage from './pages/BooksPage'
import MembersPage from './pages/MembersPage'
import IssuePage from './pages/IssuePage'

// Components
import ProtectedRoute from './components/ProtectedRoute'
import Navigation from './components/Navigation'

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  return (
    <Router>
      {isAuthenticated && <Navigation />}
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes */}
        <Route
          path="/"
          element={<ProtectedRoute><DashboardPage /></ProtectedRoute>}
        />
        <Route
          path="/books"
          element={<ProtectedRoute><BooksPage /></ProtectedRoute>}
        />
        <Route
          path="/members"
          element={<ProtectedRoute><MembersPage /></ProtectedRoute>}
        />
        <Route
          path="/issue"
          element={<ProtectedRoute><IssuePage /></ProtectedRoute>}
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App

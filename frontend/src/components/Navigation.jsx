/**
 * Navigation Component
 * Top navigation bar with logout functionality
 */
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../context/authStore'
import '../styles/Navigation.css'

function Navigation() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          📚 Library Management System
        </Link>

        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">Dashboard</Link>
          </li>
          <li className="nav-item">
            <Link to="/books" className="nav-link">Books</Link>
          </li>
          <li className="nav-item">
            <Link to="/members" className="nav-link">Members</Link>
          </li>
          <li className="nav-item">
            <Link to="/issue" className="nav-link">Issue/Return</Link>
          </li>
        </ul>

        <div className="nav-user">
          <span className="user-name">{user?.full_name || 'User'}</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navigation

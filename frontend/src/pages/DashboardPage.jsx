/**
 * Dashboard Page
 * Displays summary information and recent activities
 */
import { useState, useEffect } from 'react'
import '../styles/Dashboard.css'

function DashboardPage() {
  const [stats, setStats] = useState({
    totalBooks: 0,
    totalMembers: 0,
    booksIssued: 0,
    overdueBooks: 0,
    outstandingFines: 0
  })

  useEffect(() => {
    // TODO: Fetch dashboard stats from API
    // This will be implemented in the next phase
    setStats({
      totalBooks: 1250,
      totalMembers: 450,
      booksIssued: 180,
      overdueBooks: 12,
      outstandingFines: 2500.50
    })
  }, [])

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Books</h3>
          <p className="stat-value">{stats.totalBooks}</p>
        </div>
        
        <div className="stat-card">
          <h3>Active Members</h3>
          <p className="stat-value">{stats.totalMembers}</p>
        </div>
        
        <div className="stat-card">
          <h3>Books Issued</h3>
          <p className="stat-value">{stats.booksIssued}</p>
        </div>
        
        <div className="stat-card">
          <h3>Overdue Books</h3>
          <p className="stat-value" style={{ color: '#e74c3c' }}>{stats.overdueBooks}</p>
        </div>
        
        <div className="stat-card">
          <h3>Outstanding Fines</h3>
          <p className="stat-value">${stats.outstandingFines}</p>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <a href="/books" className="btn btn-primary">📚 Manage Books</a>
          <a href="/members" className="btn btn-primary">👥 Manage Members</a>
          <a href="/issue" className="btn btn-primary">📤 Issue/Return Books</a>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Recent Activity</h2>
        <p style={{ textAlign: 'center', color: '#95a5a6' }}>
          Recent activities will be displayed here
        </p>
      </div>
    </div>
  )
}

export default DashboardPage

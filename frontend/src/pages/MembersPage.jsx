/**
 * Members Management Page
 */
import { useState, useEffect } from 'react'
import { memberService } from '../services/api'
import '../styles/Pages.css'

function MembersPage() {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchMembers()
  }, [])

  const fetchMembers = async () => {
    try {
      setLoading(true)
      const response = await memberService.listMembers()
      setMembers(response.data)
    } catch (err) {
      setError('Failed to fetch members')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    try {
      const response = await memberService.searchMembers({ name: searchTerm })
      setMembers(response.data)
    } catch (err) {
      setError('Search failed')
    }
  }

  if (loading) return <div className="loading">Loading members...</div>

  return (
    <div className="page-container">
      <h1>Members Management</h1>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search by name or member code..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit" className="btn btn-primary">Search</button>
      </form>

      <button className="btn btn-success" onClick={() => alert('Add member form coming soon')}>
        ➕ Register New Member
      </button>

      <table className="data-table">
        <thead>
          <tr>
            <th>Member Code</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Plan</th>
            <th>Status</th>
            <th>Expiry Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {members.length > 0 ? (
            members.map((member) => (
              <tr key={member.id}>
                <td>{member.member_code}</td>
                <td>{member.full_name}</td>
                <td>{member.email || '-'}</td>
                <td>{member.phone_number || '-'}</td>
                <td>{member.membership_plan?.name || '-'}</td>
                <td>
                  <span className={`status ${member.status}`}>
                    {member.status}
                  </span>
                </td>
                <td>{new Date(member.expiry_date).toLocaleDateString()}</td>
                <td>
                  <button className="btn-small">View</button>
                  <button className="btn-small">Edit</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="8" style={{ textAlign: 'center' }}>No members found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default MembersPage

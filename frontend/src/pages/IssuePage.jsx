/**
 * Issue/Return Books Page
 */
import { useState, useEffect } from 'react'
import { transactionService, memberService, bookService } from '../services/api'
import { useAuthStore } from '../context/authStore'
import '../styles/Pages.css'

function IssuePage() {
  const user = useAuthStore((state) => state.user)
  const [activeTab, setActiveTab] = useState('issue')
  
  // Issue state
  const [bookId, setBookId] = useState('')
  const [memberId, setMemberId] = useState('')
  const [issueError, setIssueError] = useState('')
  const [issueSuccess, setIssueSuccess] = useState('')
  const [issuingLoading, setIssuingLoading] = useState(false)

  // Return state
  const [issueIdToReturn, setIssueIdToReturn] = useState('')
  const [returnError, setReturnError] = useState('')
  const [returnSuccess, setReturnSuccess] = useState('')
  const [returningLoading, setReturningLoading] = useState(false)

  const handleIssueBook = async (e) => {
    e.preventDefault()
    setIssueError('')
    setIssueSuccess('')
    
    if (!bookId || !memberId) {
      setIssueError('Please select both book and member')
      return
    }

    setIssuingLoading(true)
    try {
      await transactionService.issueBook(
        parseInt(bookId),
        parseInt(memberId),
        user.id
      )
      setIssueSuccess('Book issued successfully!')
      setBookId('')
      setMemberId('')
    } catch (err) {
      setIssueError(err.response?.data?.detail || 'Failed to issue book')
    } finally {
      setIssuingLoading(false)
    }
  }

  const handleReturnBook = async (e) => {
    e.preventDefault()
    setReturnError('')
    setReturnSuccess('')
    
    if (!issueIdToReturn) {
      setReturnError('Please enter issue ID')
      return
    }

    setReturningLoading(true)
    try {
      await transactionService.returnBook(parseInt(issueIdToReturn))
      setReturnSuccess('Book returned successfully!')
      setIssueIdToReturn('')
    } catch (err) {
      setReturnError(err.response?.data?.detail || 'Failed to return book')
    } finally {
      setReturningLoading(false)
    }
  }

  return (
    <div className="page-container">
      <h1>Issue & Return Books</h1>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'issue' ? 'active' : ''}`}
          onClick={() => setActiveTab('issue')}
        >
          📤 Issue Book
        </button>
        <button
          className={`tab ${activeTab === 'return' ? 'active' : ''}`}
          onClick={() => setActiveTab('return')}
        >
          📥 Return Book
        </button>
      </div>

      {activeTab === 'issue' && (
        <div className="form-container">
          <h2>Issue a Book</h2>
          
          {issueError && <div className="error-message">{issueError}</div>}
          {issueSuccess && <div className="success-message">{issueSuccess}</div>}

          <form onSubmit={handleIssueBook}>
            <div className="form-group">
              <label htmlFor="bookId">Book ID</label>
              <input
                type="number"
                id="bookId"
                value={bookId}
                onChange={(e) => setBookId(e.target.value)}
                placeholder="Enter book ID"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="memberId">Member ID</label>
              <input
                type="number"
                id="memberId"
                value={memberId}
                onChange={(e) => setMemberId(e.target.value)}
                placeholder="Enter member ID"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={issuingLoading}>
              {issuingLoading ? 'Issuing...' : 'Issue Book'}
            </button>
          </form>
        </div>
      )}

      {activeTab === 'return' && (
        <div className="form-container">
          <h2>Return a Book</h2>
          
          {returnError && <div className="error-message">{returnError}</div>}
          {returnSuccess && <div className="success-message">{returnSuccess}</div>}

          <form onSubmit={handleReturnBook}>
            <div className="form-group">
              <label htmlFor="issueId">Issue ID</label>
              <input
                type="number"
                id="issueId"
                value={issueIdToReturn}
                onChange={(e) => setIssueIdToReturn(e.target.value)}
                placeholder="Enter issue ID"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={returningLoading}>
              {returningLoading ? 'Processing...' : 'Return Book'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}

export default IssuePage

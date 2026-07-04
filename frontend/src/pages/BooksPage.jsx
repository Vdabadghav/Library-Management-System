/**
 * Books Management Page
 * Add, edit, delete, and search books
 */
import { useState, useEffect } from 'react'
import { bookService } from '../services/api'
import '../styles/Pages.css'

function BooksPage() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  const formatAuthors = (authors) =>
    authors?.length ? authors.map((author) => author.full_name).join(', ') : '-'

  const formatGenres = (genres) =>
    genres?.length ? genres.map((genre) => genre.name).join(', ') : '-'

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    try {
      setLoading(true)
      const response = await bookService.listBooks()
      setBooks(response.data)
    } catch (err) {
      setError('Failed to fetch books')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    try {
      const response = await bookService.searchBooks({ title: searchTerm })
      setBooks(response.data)
    } catch (err) {
      setError('Search failed')
    }
  }

  if (loading) return <div className="loading">Loading books...</div>

  return (
    <div className="page-container">
      <h1>Books Management</h1>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search by title, author, or ISBN..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit" className="btn btn-primary">Search</button>
      </form>

      <button className="btn btn-success" onClick={() => alert('Add book form coming soon')}>
        ➕ Add New Book
      </button>

      <table className="data-table">
        <thead>
          <tr>
            <th>ISBN</th>
            <th>Title</th>
            <th>Author</th>
            <th>Genre</th>
            <th>Publisher</th>
            <th>Year</th>
            <th>Total Copies</th>
            <th>Available</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {books.length > 0 ? (
            books.map((book) => (
              <tr key={book.id}>
                <td>{book.isbn}</td>
                <td>{book.title}</td>
                <td>{formatAuthors(book.authors)}</td>
                <td>{formatGenres(book.genres)}</td>
                <td>{book.publisher}</td>
                <td>{book.publication_year}</td>
                <td>{book.total_copies}</td>
                <td>{book.copies_available ?? book.total_copies - (book.copies_issued || 0)}</td>
                <td>
                  <button className="btn-small">Edit</button>
                  <button className="btn-small">Delete</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9" style={{ textAlign: 'center' }}>No books found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default BooksPage

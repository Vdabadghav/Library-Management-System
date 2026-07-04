# Library Management System - Frontend Setup Guide

## 📋 Project Overview
This is a React + Vite frontend for the Library Management System with:
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: Zustand
- **Styling**: CSS3

## ⚙️ Prerequisites

- Node.js 16.9.0 or higher
- npm or yarn
- Backend API running on http://localhost:8000

## 🚀 Installation Steps

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Development Server

```bash
# Start development server
npm run dev

# Frontend will be available at: http://localhost:5173
```

### 4. Build for Production

```bash
npm run build

# Output will be in the 'dist' folder
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/              # Reusable React components
│   │   ├── Navigation.jsx       # Top navigation bar
│   │   └── ProtectedRoute.jsx   # Route protection wrapper
│   ├── pages/                   # Page components
│   │   ├── LoginPage.jsx        # Login page
│   │   ├── RegisterPage.jsx     # Registration page
│   │   ├── DashboardPage.jsx    # Dashboard
│   │   ├── BooksPage.jsx        # Books management
│   │   ├── MembersPage.jsx      # Members management
│   │   └── IssuePage.jsx        # Issue/Return books
│   ├── services/                # API communication
│   │   └── api.js              # API service functions
│   ├── context/                 # State management
│   │   └── authStore.js        # Zustand auth store
│   ├── styles/                  # CSS files
│   │   ├── index.css           # Global styles
│   │   ├── Navigation.css      # Navigation styles
│   │   ├── Auth.css            # Authentication pages
│   │   ├── Dashboard.css       # Dashboard styles
│   │   └── Pages.css           # Page styles
│   ├── utils/                   # Utility functions
│   │   └── api-config.js       # API endpoints configuration
│   ├── App.jsx                 # Main app component
│   └── main.jsx                # Entry point
├── public/                      # Static assets
├── index.html                   # HTML template
├── package.json                 # Dependencies
├── vite.config.js              # Vite configuration
└── FRONTEND_SETUP.md           # This file
```

## 🔗 API Integration

### Environment Configuration

Create a `.env` file in the frontend directory (optional):

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### API Service Usage

The `services/api.js` provides ready-to-use functions for all endpoints:

```javascript
// Example: Login
import { authService } from './services/api'

const response = await authService.login(username, password)

// Example: Get books
import { bookService } from './services/api'

const books = await bookService.listBooks()

// Example: Issue a book
import { transactionService } from './services/api'

await transactionService.issueBook(bookId, memberId, userId)
```

## 🔐 Authentication Flow

### 1. Login Process
```javascript
// User login
const response = await authService.login(username, password)

// Store user and token
useAuthStore.setState({
  user: response.data.user,
  token: response.data.access_token,
  isAuthenticated: true
})

// JWT token is automatically added to all requests
```

### 2. Protected Routes
Routes are protected using the `ProtectedRoute` component:

```jsx
<Route
  path="/dashboard"
  element={<ProtectedRoute><DashboardPage /></ProtectedRoute>}
/>
```

If user is not authenticated, they are redirected to login.

### 3. Logout
```javascript
const logout = useAuthStore((state) => state.logout)
logout() // Clears user data and token
```

## 📝 Component Development Guide

### Creating a New Page

```jsx
// src/pages/NewPage.jsx
import { useState, useEffect } from 'react'
import { useAuthStore } from '../context/authStore'
import '../styles/NewPage.css'

function NewPage() {
  const user = useAuthStore((state) => state.user)
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch data on mount
  }, [])

  return (
    <div className="page-container">
      <h1>Page Title</h1>
      {/* Your content here */}
    </div>
  )
}

export default NewPage
```

### Using API Services

```jsx
import { bookService } from '../services/api'

// List books
const books = await bookService.listBooks(skip, limit)

// Search books
const results = await bookService.searchBooks({
  title: 'Harry Potter',
  author: 'Rowling'
})

// Get specific book
const book = await bookService.getBook(bookId)
```

### Zustand State Management

```jsx
import { useAuthStore } from '../context/authStore'

function MyComponent() {
  // Select state
  const user = useAuthStore((state) => state.user)
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  // Call actions
  const logout = useAuthStore((state) => state.logout)
  
  return <div>{user?.full_name}</div>
}
```

## 🎨 Styling

The application uses CSS3 with a utility-first approach:

### Color Palette
- Primary: `#3498db` (Blue)
- Success: `#27ae60` (Green)
- Danger: `#e74c3c` (Red)
- Dark: `#2c3e50` (Dark Blue)
- Light: `#ecf0f1` (Light Gray)

### Responsive Design
Pages use CSS Grid and Flexbox for responsive layouts.

## 🧪 Testing in Development

### Manual Testing Steps

1. **Login**
   - Navigate to http://localhost:5173/login
   - Enter test credentials
   - Verify token is stored

2. **Protected Route**
   - Try accessing /books without logging in
   - Should redirect to /login

3. **API Calls**
   - Check browser Network tab
   - Verify requests include Authorization header
   - Check response status codes

### Browser DevTools

1. **Application Tab**
   - Check localStorage for `access_token` and `user`
   - Monitor state changes

2. **Network Tab**
   - Monitor API requests to http://localhost:8000/api/v1
   - Check request/response headers and body
   - Verify token is included in Authorization header

3. **Console**
   - Check for errors
   - Use `localStorage.getItem('access_token')` to check token

## 📦 Available Scripts

```bash
# Development
npm run dev          # Start dev server

# Production
npm run build        # Build for production
npm run preview      # Preview production build locally

# Linting
npm run lint         # Run ESLint
```

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Server
1. Upload `dist/` folder contents to your web server
2. Configure server to serve `index.html` for all routes
3. Update `VITE_API_URL` in environment

### Using with Node.js/Express
```bash
# Install serve to test locally
npm install -g serve
serve -s dist -l 3000
```

## 🔧 Troubleshooting

### CORS Errors
```
Error: Access to XMLHttpRequest blocked by CORS
Solution:
- Ensure backend is running on http://localhost:8000
- Check ALLOWED_ORIGINS in backend .env
- Verify proxy settings in vite.config.js
```

### Token Not Persisting
```
Solution:
- Check browser localStorage is enabled
- Verify token is saved after login
- Check localStorage in DevTools → Application tab
```

### API Calls Failing
```
Solution:
- Check backend is running
- Verify API endpoint in api-config.js
- Check Network tab in DevTools
- Verify token is included in Authorization header
```

### Hot Reload Not Working
```
Solution:
- Check Vite dev server is running (port 5173)
- Restart dev server: Ctrl+C then npm run dev
- Clear browser cache
```

## 📚 Key Features

### ✅ Implemented
- [x] Authentication (Login/Register)
- [x] Protected Routes
- [x] Navigation Bar
- [x] Dashboard
- [x] Books Management (List, Search)
- [x] Members Management (List, Search)
- [x] Issue/Return Books
- [x] Responsive Design

### 🚧 To Be Implemented
- [ ] Book Add/Edit/Delete
- [ ] Member Add/Edit/Delete
- [ ] Catalog Management (Authors, Genres, Languages)
- [ ] Fines Management
- [ ] Reports
- [ ] Advanced Filters
- [ ] Pagination
- [ ] User Management (Admin)
- [ ] Activity Log Viewer
- [ ] Notifications
- [ ] Print/Export functionality

## 🔐 Security Best Practices

1. **Token Storage**
   - Tokens stored in localStorage (consider httpOnly cookies)
   - Tokens sent with every API request

2. **HTTPS**
   - Use HTTPS in production
   - Set secure flag on cookies

3. **XSS Protection**
   - React automatically escapes content
   - Never use `dangerouslySetInnerHTML`

4. **CSRF Protection**
   - Implement CSRF tokens if needed
   - Backend validates token origin

## 📞 Support

For issues:
1. Check browser console for errors
2. Check Network tab for API responses
3. Verify backend is running
4. Check .env configuration
5. Review error messages carefully

---

**Happy coding!** 🚀

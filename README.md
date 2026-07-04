# Library Management System - Complete Production-Quality Application

A comprehensive full-stack Library Management System built with modern technologies following best practices for production-quality code.

## 🎯 Overview

This system manages day-to-day operations of a library branch, handling:
- 📚 **Book Catalog Management** - Add, edit, search books with multiple authors and genres
- 👥 **Member Management** - Register members, manage memberships and status
- 🔄 **Book Transactions** - Issue and return books with automatic due date calculation
- 💰 **Fine Management** - Automatic fine calculation for overdue books
- 👤 **User Management** - Staff accounts with role-based access control
- 📊 **Reports & Analytics** - Comprehensive system reporting
- 🔐 **Security** - JWT authentication, password hashing, audit logging

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy 2.0
- **Database**: MySQL 5.7+
- **Authentication**: JWT + bcrypt
- **API Docs**: Swagger UI & ReDoc
- **Async**: Native async/await support

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 5.0
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: Zustand
- **Styling**: CSS3 with Flexbox/Grid

### DevOps
- **Server**: Uvicorn
- **Task Runner**: Node.js/npm

## 📋 Project Structure

```
Library Management System/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── core/                     # Configuration & Security
│   │   │   ├── config.py             # Environment configuration
│   │   │   ├── security.py           # JWT & Password handling
│   │   │   └── logging_config.py     # Logging setup
│   │   ├── db/                       # Database
│   │   │   └── database.py           # SQLAlchemy setup
│   │   ├── models/                   # Data Models
│   │   │   └── models.py             # 11 ORM models with relationships
│   │   ├── schemas/                  # Data Validation
│   │   │   └── schemas.py            # 20+ Pydantic schemas
│   │   ├── crud/                     # Database Operations
│   │   │   ├── user.py               # User CRUD
│   │   │   ├── book.py               # Book CRUD
│   │   │   ├── member.py             # Member CRUD
│   │   │   ├── catalog.py            # Language/Genre/Author CRUD
│   │   │   └── transaction.py        # Issue/Return/Fine CRUD
│   │   ├── api/                      # API Endpoints
│   │   │   └── endpoints/
│   │   │       ├── auth.py           # Authentication endpoints
│   │   │       ├── users.py          # User management
│   │   │       ├── books.py          # Book management
│   │   │       ├── catalog.py        # Catalog management
│   │   │       ├── members.py        # Member management
│   │   │       └── transactions.py   # Issue/Return/Fine
│   │   ├── utils/
│   │   │   └── exceptions.py         # Custom exceptions
│   │   └── main.py                   # FastAPI app factory
│   ├── run.py                        # Entry point
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                  # Environment template
│   ├── BACKEND_SETUP.md              # Backend documentation
│   └── logs/                         # Application logs
│
├── frontend/                         # React + Vite Frontend
│   ├── src/
│   │   ├── components/               # Reusable components
│   │   │   ├── Navigation.jsx        # Top navigation
│   │   │   └── ProtectedRoute.jsx    # Route protection
│   │   ├── pages/                    # Page components
│   │   │   ├── LoginPage.jsx         # Login
│   │   │   ├── RegisterPage.jsx      # Registration
│   │   │   ├── DashboardPage.jsx     # Dashboard
│   │   │   ├── BooksPage.jsx         # Books management
│   │   │   ├── MembersPage.jsx       # Members management
│   │   │   └── IssuePage.jsx         # Issue/Return
│   │   ├── services/                 # API integration
│   │   │   └── api.js                # API service functions
│   │   ├── context/                  # State management
│   │   │   └── authStore.js          # Zustand auth store
│   │   ├── styles/                   # CSS files
│   │   ├── utils/                    # Utilities
│   │   │   └── api-config.js         # API endpoint config
│   │   ├── App.jsx                   # Main app
│   │   └── main.jsx                  # Entry point
│   ├── index.html                    # HTML template
│   ├── package.json                  # Dependencies
│   ├── vite.config.js                # Vite config
│   ├── FRONTEND_SETUP.md             # Frontend documentation
│   └── public/                       # Static assets
│
├── FUNCTIONAL_REQUIREMENTS.docx      # System requirements
└── README.md                         # This file
```

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- Node.js 16.9.0+
- MySQL 5.7+

### 1. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
copy .env.example .env

# Start server
python run.py
```

Backend will run on: **http://localhost:8000**

API Docs available at: **http://localhost:8000/docs**

### 2. Frontend Setup
```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

### 3. Database Setup
```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE library_management_db CHARACTER SET utf8mb4;

# Create user (optional)
CREATE USER 'library_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON library_management_db.* TO 'library_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Test the Application
1. Open http://localhost:5173 in browser
2. Click "Register" to create an account
3. Admin must approve account (use admin credentials)
4. Login with approved account
5. Use the dashboard to navigate

## 📊 Database Schema

### 11 Main Models
1. **User** - Staff accounts
2. **Role** - Role definitions
3. **Permission** - Role permissions
4. **Language** - Book languages
5. **Genre** - Book genres
6. **Author** - Book authors
7. **Book** - Book catalog
8. **MembershipPlan** - Membership definitions
9. **Member** - Library members
10. **BookIssue** - Issue/return tracking
11. **Fine** - Fine records
12. **ActivityLog** - Audit trail

### Key Relationships
- Book → many Authors (many-to-many)
- Book → many Genres (many-to-many)
- Member → MembershipPlan (1-to-many)
- BookIssue → Book, Member, User (1-to-many)
- Fine → Member, BookIssue (1-to-many)

## 🔐 Security Features

✅ **Authentication**
- JWT token-based authentication
- Secure password hashing with bcrypt
- Token expiration management

✅ **Authorization**
- Role-based access control (Administrator, Manager, Librarian)
- Feature-level permissions
- Protected routes in frontend

✅ **Audit Trail**
- Complete activity logging
- Track all user actions
- Timestamp and IP logging

✅ **Data Validation**
- Pydantic schema validation
- Input sanitization
- Business logic constraints

✅ **Error Handling**
- Comprehensive error messages
- Custom exception hierarchy
- HTTP status codes

## 📝 API Endpoints Overview

### Authentication (6 endpoints)
- POST `/auth/login` - User login
- POST `/auth/register` - User registration
- POST `/auth/verify-token` - Verify JWT token

### Users (6 endpoints)
- GET `/users` - List users
- GET `/users/{id}` - Get user
- POST `/users` - Create user
- PUT `/users/{id}` - Update user
- DELETE `/users/{id}` - Delete user
- PATCH `/users/{id}/status/{status}` - Update status

### Books (7 endpoints)
- GET `/books` - List books
- GET `/books/search` - Search books
- GET `/books/{id}` - Get book
- POST `/books` - Create book
- PUT `/books/{id}` - Update book
- DELETE `/books/{id}` - Delete book
- GET `/books/{id}/available-copies` - Check availability

### Catalog (10 endpoints)
- Languages CRUD (4 endpoints)
- Genres CRUD (4 endpoints)
- Authors CRUD (6 endpoints)

### Members (11 endpoints)
- Members CRUD (6 endpoints)
- Membership Plans CRUD (5 endpoints)
- Member status management
- Search functionality

### Transactions (13 endpoints)
- POST `/issue` - Issue book
- POST `/return/{id}` - Return book
- GET `/overdue` - Get overdue books
- GET `/fines/{id}` - Get fine
- POST `/fines/{id}/pay` - Pay fine
- Reports endpoints

**Total: 53+ API endpoints**

## 🎨 Frontend Features

### Pages
- **Login** - Authentication
- **Register** - Self-registration (requires admin approval)
- **Dashboard** - Summary statistics
- **Books** - Browse, search, manage books
- **Members** - Manage library members
- **Issue/Return** - Book transactions

### Components
- **Navigation** - Top navigation bar with user info
- **ProtectedRoute** - Route protection wrapper
- **Forms** - Input validation
- **Tables** - Data display with sorting
- **Modals** - Dialogs for actions

### State Management
- **Zustand** - Simple, powerful state management
- **localStorage** - Token and user persistence
- **Axios Interceptors** - Automatic token injection

## 💾 Production Checklist

- [ ] Change SECRET_KEY in backend .env
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_ORIGINS for CORS
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS
- [ ] Set up proper database backups
- [ ] Configure logging to file
- [ ] Set up error monitoring
- [ ] Implement rate limiting
- [ ] Enable CSRF protection
- [ ] Configure authentication properly
- [ ] Test all functionality
- [ ] Perform security audit
- [ ] Load testing
- [ ] Documentation updates

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Password validation
- [ ] Token expiration
- [ ] Add/edit/delete books
- [ ] Search functionality
- [ ] Member registration
- [ ] Issue book functionality
- [ ] Fine calculation
- [ ] Role-based access
- [ ] Error handling
- [ ] API responses

### Automated Testing (Future)
- Unit tests for backend
- Integration tests for API
- Component tests for frontend
- E2E tests

## 📚 Documentation

Detailed setup guides are provided:
- [Backend Setup Guide](backend/BACKEND_SETUP.md)
- [Frontend Setup Guide](frontend/FRONTEND_SETUP.md)
- [System Requirements](FUNCTIONAL_REQUIREMENTS.docx)

## 🤝 Contributing

This is a learning project demonstrating:
- Professional code structure
- Best practices in web development
- Production-quality patterns
- Comprehensive documentation
- Error handling and logging
- Database design with relationships
- API design patterns
- Frontend state management
- Security implementation

## 📞 Support & Troubleshooting

### Common Issues

**MySQL Connection Error**
```bash
# Check MySQL is running
mysql --version

# Start MySQL service
# Windows: net start MySQL57
# macOS: brew services start mysql
# Linux: sudo service mysql start
```

**Port Already in Use**
```bash
# Find process on port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Module Not Found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
npm install --legacy-peer-deps
```

**CORS Errors**
- Ensure backend is running on http://localhost:8000
- Check ALLOWED_ORIGINS in .env
- Verify frontend proxy configuration

## 📊 Performance Considerations

- **Database Indexes**: Added on frequently queried fields
- **Connection Pooling**: Configured with 10 connections
- **Pagination**: Implemented on list endpoints
- **Lazy Loading**: Frontend implements code splitting
- **Caching**: Can be added with Redis
- **Compression**: Vite minifies production builds

## 🔄 Development Workflow

1. **Backend Development**
   ```bash
   cd backend && source venv/bin/activate && python run.py
   ```

2. **Frontend Development**
   ```bash
   cd frontend && npm run dev
   ```

3. **API Testing**
   - Use Swagger UI at http://localhost:8000/docs
   - Test in browser or Postman

4. **Frontend Testing**
   - Use browser DevTools
   - Check Network and Console tabs
   - Verify localStorage states

## 🎓 Learning Resources

This project demonstrates:
- RESTful API design
- SQLAlchemy ORM relationships
- Pydantic data validation
- JWT authentication
- React Hooks and state management
- Component-based architecture
- Error handling patterns
- Logging best practices
- Database indexing
- CORS configuration

## 📄 License

This is a demonstration project for educational purposes.

## 🙏 Acknowledgments

Built following industry best practices and modern web development standards.

---

**Ready to use!** Start with the Quick Start section above or read the detailed setup guides in each directory.

For questions or issues, refer to the troubleshooting sections in:
- [Backend Setup](backend/BACKEND_SETUP.md#-troubleshooting)
- [Frontend Setup](frontend/FRONTEND_SETUP.md#-troubleshooting)

# Library Management System - Backend Setup Guide

## 📋 Project Overview
This is a comprehensive Library Management System built with:
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Authentication**: JWT
- **API Documentation**: Swagger UI & ReDoc

## ⚙️ Prerequisites

- Python 3.9+
- MySQL Server 5.7+ or MariaDB 10.3+
- pip (Python package manager)
- git

## 🚀 Installation Steps

### 1. MySQL Database Setup

#### Option A: Using MySQL CLI
```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE library_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create database user (recommended for production)
CREATE USER 'library_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON library_management_db.* TO 'library_user'@'localhost';
FLUSH PRIVILEGES;

# Verify
SHOW DATABASES;
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect with root credentials
3. File → New Query Tab
4. Execute the SQL commands above

### 2. Python Virtual Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Verify activation (you should see (venv) in terminal)
which python  # On Windows: where python
```

### 3. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Environment Configuration

```bash
# Copy example environment file
copy .env.example .env

# Or on macOS/Linux:
cp .env.example .env

# Edit .env file with your configuration
# Change these values:
MYSQL_USER=library_user        # Your MySQL user
MYSQL_PASSWORD=secure_password # Your MySQL password
MYSQL_DATABASE=library_management_db
SECRET_KEY=your-production-secret-key
FRONTEND_URL=http://localhost:5173
```

### 5. Run the Server

```bash
# Start FastAPI development server
python run.py

# Or using uvicorn directly:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

### 6. Access API Documentation

Once the server is running, open your browser and visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app factory
│   ├── core/
│   │   ├── config.py          # Settings management
│   │   ├── security.py        # JWT & password hashing
│   │   └── logging_config.py  # Logging setup
│   ├── db/
│   │   └── database.py        # SQLAlchemy configuration
│   ├── models/
│   │   └── models.py          # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py         # Pydantic validation schemas
│   ├── crud/
│   │   ├── user.py            # User operations
│   │   ├── book.py            # Book operations
│   │   ├── member.py          # Member operations
│   │   ├── catalog.py         # Catalog operations
│   │   └── transaction.py     # Issue/Return operations
│   ├── api/
│   │   └── endpoints/
│   │       ├── auth.py        # Authentication endpoints
│   │       ├── users.py       # User management endpoints
│   │       ├── books.py       # Book management endpoints
│   │       ├── catalog.py     # Catalog endpoints
│   │       ├── members.py     # Member endpoints
│   │       └── transactions.py # Issue/Return endpoints
│   └── utils/
│       └── exceptions.py      # Custom exceptions
├── tests/                      # Test files (optional)
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
├── run.py                      # Server entry point
├── .env.example               # Environment template
└── .env                       # Environment configuration (create from example)
```

## 🔐 Security Considerations

### For Development
- `SECRET_KEY` = simple value (changed in .env.example)
- `DEBUG` = True (set to False in production)
- `ALLOWED_ORIGINS` includes localhost

### For Production
1. **Change SECRET_KEY**:
   ```python
   import secrets
   secrets.token_urlsafe(32)  # Generate strong key
   ```

2. **Update .env**:
   ```
   DEBUG=False
   SECRET_KEY=<generated-secure-key>
   MYSQL_PASSWORD=<strong-password>
   ALLOWED_ORIGINS=["https://yourdomain.com"]
   ```

3. **Use HTTPS** in production
4. **Use environment variables** for sensitive data
5. **Enable CORS** only for your frontend domain

## 📊 Database Models & Relationships

### User Management
- `User`: Staff accounts with roles (Administrator, Manager, Librarian)
- `Role`: Role definitions with permissions
- `Permission`: Feature-level permissions

### Catalog Management
- `Book`: Books in the library catalog
- `Author`: Book authors (many-to-many with books)
- `Genre`: Book genres (many-to-many with books)
- `Language`: Languages for books

### Member Management
- `Member`: Library members
- `MembershipPlan`: Membership plan definitions
- Relationships: Member → Plan (1-to-many)

### Transactions
- `BookIssue`: Book issue/return tracking
- `Fine`: Fine records for overdue books
- Relationships: BookIssue → Book, Member, User
- Relationships: Fine → Member, BookIssue

### Audit
- `ActivityLog`: Complete audit trail of all actions

## 🔄 API Workflow Examples

### 1. User Registration & Login
```
POST /api/v1/auth/register        # User self-registers
POST /api/v1/auth/login           # User logs in → JWT token
POST /api/v1/auth/verify-token    # Verify token
```

### 2. Admin Approves User
```
GET /api/v1/users/                # List users (inactive status)
PATCH /api/v1/users/{id}/status/active  # Approve user
```

### 3. Member Registration
```
GET /api/v1/members/plans         # Get available plans
POST /api/v1/members/             # Register member
```

### 4. Book Issuance
```
GET /api/v1/books/search          # Search for books
GET /api/v1/books/{id}            # Check availability
POST /api/v1/transactions/issue   # Issue book to member
```

### 5. Book Return & Fine
```
POST /api/v1/transactions/return/{issue_id}  # Return book
GET /api/v1/transactions/fines/{fine_id}     # View fine
POST /api/v1/transactions/fines/{id}/pay     # Pay fine
```

## 🧪 Testing the API

### Using cURL
```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "SecurePass123"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123"
  }'
```

### Using Swagger UI
1. Visit http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Enter parameters and click "Execute"

## 📝 Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_HOST` | Database host | localhost |
| `MYSQL_PORT` | Database port | 3306 |
| `MYSQL_USER` | Database user | root |
| `MYSQL_PASSWORD` | Database password | (empty) |
| `MYSQL_DATABASE` | Database name | library_management_db |
| `SECRET_KEY` | JWT secret key | dev-key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 30 |
| `DEBUG` | Debug mode | True |
| `FRONTEND_URL` | Frontend URL | http://localhost:5173 |
| `LOG_LEVEL` | Logging level | INFO |

## ✅ Verification Checklist

- [ ] MySQL database created
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Server starts without errors
- [ ] Health check endpoint responds
- [ ] Swagger UI is accessible
- [ ] Database tables created automatically

## 🆘 Troubleshooting

### Connection Error: MySQL
```
Error: mysql.connector.errors.DatabaseError
Solution:
1. Check MySQL is running
2. Verify connection details in .env
3. Ensure database exists: SHOW DATABASES;
```

### Port Already in Use
```
Error: Address already in use
Solution:
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process and restart
```

### Import Errors
```
Error: ModuleNotFoundError
Solution:
1. Verify virtual environment is activated
2. Reinstall dependencies: pip install -r requirements.txt
3. Check Python version: python --version (should be 3.9+)
```

### Database Tables Not Created
```
Solution:
1. Restart the server
2. Check logs for errors: tail -f logs/app.log
3. Manually create tables using Alembic (future enhancement)
```

## 📚 Next Steps

1. **Frontend Setup**: Follow React/Vite setup guide
2. **API Integration**: Connect frontend to backend APIs
3. **Testing**: Run unit and integration tests
4. **Deployment**: Deploy to production environment

## 📖 Useful Commands

```bash
# Show database tables
mysql -u library_user -p library_management_db
SHOW TABLES;

# View active processes
ps aux | grep python

# Kill server process
Ctrl + C

# Check logs
tail -f logs/app.log

# Reinstall dependencies (if needed)
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

For issues or questions:
1. Check logs in `logs/app.log`
2. Review error messages in Swagger UI
3. Verify .env configuration
4. Check MySQL connection

---

**Happy coding!** 🚀

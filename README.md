# Social Media Backend API

A modern, production-ready REST API for a social media platform built with FastAPI, featuring JWT authentication, secure post management, and optimized querying.

## 🎯 Project Overview

This backend API demonstrates clean architecture and best practices in building scalable web applications. Users can create posts with content, discover and upvote posts from the community, and enjoy a seamless social experience with secure authentication.

### Core Features

- **🔐 JWT Authentication** - Secure user authentication with token-based authorization
- **📝 Post Management** - Create, read, and manage posts with rich content
- **👍 Upvote System** - Users can upvote posts to show appreciation
- **📄 Pagination** - Efficient data fetching with limit/offset pagination for scalability
- **🔍 Search** - Search posts by title for easy discovery
- **⚙️ Limit Control** - Configurable result limits for optimized performance
- **✅ Input Validation** - Robust Pydantic validation and error handling
- **⚡ Async Operations** - Non-blocking request handling for optimal performance
- **📚 Auto API Docs** - Interactive Swagger UI and ReDoc documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-project-name>

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once running, access the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Project Structure

```
project/
├── main.py                  # Application entry point & routes
├── models.py                # SQLAlchemy ORM models
├── schemas.py               # Pydantic request/response schemas
├── database.py              # Database configuration & session
├── auth.py                  # JWT authentication logic
├── config.py                # Environment & app configuration
├── requirements.txt         # Project dependencies
└── README.md
```

## 🔑 Key Implementation Details

### Authentication & Security
- JWT token-based authentication for secure endpoints
- Password hashing for user security
- Token validation on protected routes
- Proper authorization checks

### API Endpoints

**Users API (Authentication)**
- `POST /users/register` - User registration
- `POST /users/login` - User login (returns JWT token)

**Posts API**
- `POST /posts` - Create a new post (authenticated)
- `GET /posts` - Fetch all posts with pagination and search
  - Query Parameters:
    - `skip` (int) - Number of posts to skip (default: 0)
    - `limit` (int) - Maximum number of posts to return (default: 10)
    - `search` (str) - Search posts by title
- `GET /posts/{post_id}` - Get specific post
- `POST /posts/{post_id}/upvote` - Upvote a post (authenticated)

For complete API documentation and additional endpoints, visit the interactive Swagger UI at `/docs`

### Data Validation & Error Handling
- ✅ Pydantic models for strict input validation
- ✅ HTTP status codes (200, 201, 400, 401, 404, 500, etc.)
- ✅ Meaningful error messages for debugging
- ✅ Exception handling for database errors

### Database Design
- PostgreSQL for reliable data persistence
- Efficient indexing on frequently queried fields
- Proper foreign key relationships
- Pagination for scalable data retrieval

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | High-performance web framework |
| **PostgreSQL** | Relational database |
| **SQLAlchemy** | ORM for database operations |
| **Pydantic** | Data validation & serialization |
| **PyJWT** | JWT token generation & verification |
| **Uvicorn** | ASGI server |
| **Python 3.9+** | Programming language |

## 📊 Database Schema

### Users Table
```
users
├── id (INTEGER, Primary Key)
├── email (VARCHAR, Unique)
├── password (VARCHAR, hashed)
└── created_at (TIMESTAMP with timezone)
```

### Posts Table
```
posts
├── id (INTEGER, Primary Key)
├── title (VARCHAR)
├── content (VARCHAR)
├── published (BOOLEAN, default: TRUE)
├── created_at (TIMESTAMP with timezone)
└── owner_id (INTEGER, Foreign Key → users.id, ON DELETE CASCADE)
```

### Votes Table (Upvotes)
```
votes
├── user_id (INTEGER, Foreign Key → users.id, ON DELETE CASCADE, Primary Key)
├── post_id (INTEGER, Foreign Key → posts.id, ON DELETE CASCADE, Primary Key)
└── Composite Primary Key: (user_id, post_id) - ensures one vote per user per post
```

### Entity Relationships
- **Users → Posts**: One-to-Many relationship (one user can create many posts)
- **Users → Votes**: One-to-Many relationship (one user can vote on many posts)
- **Posts → Votes**: One-to-Many relationship (one post can receive many votes)
- **Cascade Delete**: When a user is deleted, all their posts and votes are automatically deleted

## 💡 What I Learned Building This

- Designing RESTful APIs with proper HTTP semantics
- Implementing secure JWT authentication flows
- Building efficient pagination systems
- Database normalization and relationships
- Async programming patterns in Python
- Input validation and error handling best practices
- Code organization and separation of concerns

## 🚀 Future Enhancements

- Add comment system on posts
- Implement real-time notifications
- Add user follow/unfollow functionality
- Deploy to cloud (AWS/Heroku/DigitalOcean)
- Add rate limiting to prevent abuse
- Implement caching for frequently accessed data
- Add comprehensive test suite

## 📝 Example Usage

```bash
# Register a new user
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"secure123"}'

# Login and get JWT token
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secure123"}'

# Create a post (with JWT token)
curl -X POST "http://localhost:8000/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Post","content":"Hello world!"}'

# Fetch posts with pagination (first 10 posts)
curl "http://localhost:8000/posts?skip=0&limit=10"

# Search posts by title
curl "http://localhost:8000/posts?search=fastapi"

# Search with custom limit
curl "http://localhost:8000/posts?search=python&limit=5"

# Get next page of posts
curl "http://localhost:8000/posts?skip=10&limit=10"

# Upvote a post
curl -X POST "http://localhost:8000/posts/1/upvote" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get a specific post
curl "http://localhost:8000/posts/1"
```

---



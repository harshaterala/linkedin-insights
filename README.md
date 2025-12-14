# LinkedIn Insights Microservice

A high-performance FastAPI microservice for scraping, analyzing, and visualizing LinkedIn company page data.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📋 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Configuration](#-configuration)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **🔍 LinkedIn Scraping**: Automated scraping of company pages, posts, and employee data
- **📊 Analytics Dashboard**: Interactive web dashboard with company insights and metrics
- **🚀 RESTful API**: Comprehensive API endpoints with OpenAPI/Swagger documentation
- **💾 PostgreSQL Storage**: Efficient data storage with SQLAlchemy ORM
- **🐳 Docker Ready**: Containerized deployment with Docker Compose
- **📈 Real-time Monitoring**: Health checks and performance metrics
- **🔐 Extensible Architecture**: Modular design for easy feature additions

## 🏗️ Architecture

```
LinkedIn Insights follows a clean, modular architecture:

┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    FastAPI Application Layer                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   API    │  │  Auth    │  │  Rate    │  │   CORS   │   │
│  │  Routes  │  │  Middle- │  │ Limiting │  │  Middle- │   │
│  │          │  │   ware   │  │          │  │   ware   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Page     │  │   Post     │  │   User     │           │
│  │  Service   │  │  Service   │  │  Service   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                      Data Access Layer                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  SQLAlchemy ORM                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │   Page   │  │   Post   │  │   User   │  Models   │   │
│  │  │  Model   │  │  Model   │  │  Model   │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘           │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                      PostgreSQL Database                     │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Docker** & **Docker Compose** (Recommended)
- **Python 3.11+** (For local development)
- **PostgreSQL** (Optional, Docker provides this)

### Option 1: Docker (Recommended - 2 Minutes)
```bash
# Clone the repository
git clone https://github.com/harshaterala/linkedin-insights.git
cd linkedin-insights

# Start all services
docker-compose up -d

# Wait for services to initialize
sleep 10

# Verify the application is running
curl http://localhost:8000/health
```

### Option 2: Local Development
```bash
# Clone the repository
git clone https://github.com/harshaterala/linkedin-insights.git
cd linkedin-insights

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Points
Once running, access the service at:
- 🌐 **Dashboard**: http://localhost:8000
- 📚 **Swagger UI**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc
- 🏥 **Health Check**: http://localhost:8000/health
- 🐘 **PostgreSQL**: localhost:5432 (username: postgres, password: password)

## 📚 API Documentation

### Core Endpoints

#### Company Pages
```http
GET    /api/v1/pages/{page_id}                # Get company details
POST   /api/v1/pages/{page_id}/scrape         # Scrape company data
GET    /api/v1/pages/                         # Search companies
GET    /api/v1/pages/{page_id}/employees      # Get company employees
GET    /api/v1/pages/{page_id}/posts          # Get company posts
```

#### Posts & Engagement
```http
GET    /api/v1/posts/{post_id}/comments       # Get post comments
GET    /api/v1/analytics/engagement           # Engagement analytics
```

#### System
```http
GET    /health                                # Health check
GET    /dashboard                             # Web dashboard
GET    /docs                                  # Interactive API docs
GET    /redoc                                 # Alternative API docs
```

### Example API Usage
```bash
# Get company details (auto-scrapes if not in DB)
curl -X GET "http://localhost:8000/api/v1/pages/deepsolv"

# Scrape and save company data
curl -X POST "http://localhost:8000/api/v1/pages/deepsolv/scrape"

# Search companies with filters
curl -X GET "http://localhost:8000/api/v1/pages/?min_followers=10000&industry=technology&page=1&size=10"

# Get company employees
curl -X GET "http://localhost:8000/api/v1/pages/deepsolv/employees?limit=20"
```

## 📁 Project Structure

```
linkedin-insights/
├── app/                          # Main application code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Application configuration
│   ├── database.py              # Database connection and session management
│   ├── models/                  # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── page.py             # Company page model
│   │   ├── post.py             # Post model
│   │   └── user.py             # User/employee model
│   ├── schemas/                 # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── page.py             # Page request/response schemas
│   │   ├── post.py             # Post schemas
│   │   └── user.py             # User schemas
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── scraper.py          # LinkedIn scraping service
│   │   ├── page_service.py     # Page-related business logic
│   │   └── post_service.py     # Post-related business logic
│   ├── api/                    # API route handlers
│   │   ├── __init__.py
│   │   ├── pages.py            # Page-related endpoints
│   │   ├── posts.py            # Post-related endpoints
│   │   └── users.py            # User-related endpoints
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── helpers.py          # Helper functions
├── templates/                   # HTML templates (Jinja2)
│   └── dashboard.html          # Main dashboard template
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_pages.py          # Page-related tests
│   ├── test_scraper.py        # Scraper tests
│   └── conftest.py            # Pytest configuration
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Multi-container orchestration
├── .env.example               # Environment variables template
├── README.md                  # This file
├── postman_collection.json    # Postman API collection
└── linkedin-insights-openapi.json  # OpenAPI specification
```

## 🐳 Deployment

### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: linkedin_insights
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/linkedin_insights
      APP_NAME: LinkedIn Insights Microservice
      DEBUG: ${DEBUG:-False}
      API_V1_PREFIX: /api/v1
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./app:/app/app
      - ./templates:/app/templates
    command: >
      sh -c "python -c 'from app.database import Base, engine; Base.metadata.create_all(bind=engine)' &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

volumes:
  postgres_data:
```

### Cloud Deployment

#### Render.com
```yaml
# render.yaml
services:
  - type: web
    name: linkedin-insights
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: linkedin-insights-db
          property: connectionString
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### Railway.app
```bash
# Deploy with Railway CLI
railway init
railway link
railway up
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost/linkedin_insights

# Application Settings
APP_NAME=LinkedIn Insights Microservice
DEBUG=True
API_V1_PREFIX=/api/v1

# LinkedIn Scraper Settings (Optional)
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
SCRAPER_TIMEOUT=30
MAX_POSTS_TO_SCRAPE=15
MAX_EMPLOYEES_TO_SCRAPE=20

# Pagination
DEFAULT_PAGE_SIZE=10
MAX_PAGE_SIZE=100
```

### Database Schema
```sql
-- Main tables
CREATE TABLE linkedin_pages (
    id SERIAL PRIMARY KEY,
    page_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    url VARCHAR(500),
    profile_picture_url VARCHAR(500),
    description TEXT,
    website VARCHAR(500),
    industry VARCHAR(200),
    total_followers INTEGER DEFAULT 0,
    head_count INTEGER,
    specialities JSONB,
    location VARCHAR(200),
    founded_year INTEGER,
    company_type VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    last_scraped_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE linkedin_posts (
    id SERIAL PRIMARY KEY,
    linkedin_post_id VARCHAR(100) UNIQUE,
    content TEXT,
    page_id INTEGER REFERENCES linkedin_pages(id),
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    posted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE social_media_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    profile_url VARCHAR(500),
    page_id INTEGER REFERENCES linkedin_pages(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 🛠️ Development

### Setting Up Development Environment
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pylint black

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Code formatting
black app/ tests/

# Linting
pylint app/
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pages.py -v

# Run tests with coverage report
pytest --cov=app --cov-report=html tests/

# Run tests in parallel
pytest -n auto tests/
```

### API Development
```bash
# Start development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Generate OpenAPI schema
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi(), indent=2))" > openapi.json

# Test API endpoints
curl http://localhost:8000/api/v1/pages/deepsolv
curl http://localhost:8000/health
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
   ```bash
   fork https://github.com/harshaterala/linkedin-insights
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Follow PEP 8 style guide
   - Write tests for new functionality
   - Update documentation as needed

4. **Commit Your Changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```

5. **Push to the Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

### Development Guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation
- Ensure code passes all tests
- Follow the existing code style

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** team for the incredible web framework
- **SQLAlchemy** for the powerful ORM
- **PostgreSQL** for the reliable database
- **Docker** for containerization
- **All contributors** who help improve this project

## 📞 Support

For support, please:
1. Check the [documentation](#-api-documentation)
2. Open an [issue](https://github.com/harshaterala/linkedin-insights/issues)
3. Email: [your-email@example.com](mailto:your-email@example.com)

## 📊 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/harshaterala/linkedin-insights)
![GitHub issues](https://img.shields.io/github/issues/harshaterala/linkedin-insights)
![GitHub pull requests](https://img.shields.io/github/issues-pr/harshaterala/linkedin-insights)

**Current Version**: 1.0.0  
**Last Updated**: December 2024  
**Maintainer**: [T Harshavardhan](https://github.com/harshaterala)

---

<div align="center">
  <p>Built with ❤️ using FastAPI, PostgreSQL, and Docker</p>
  <p>
    <a href="https://github.com/harshaterala/linkedin-insights/stargazers">⭐ Star us on GitHub</a>
    ·
    <a href="https://github.com/harshaterala/linkedin-insights/issues">🐛 Report Bug</a>
    ·
    <a href="https://github.com/harshaterala/linkedin-insights/issues">💡 Request Feature</a>
  </p>
</div>

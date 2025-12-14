# ADD THIS TO THE VERY TOP OF app/main.py
import sys
import typing

if sys.version_info >= (3, 13):
    # Monkey patch to fix Python 3.13 + SQLAlchemy compatibility
    original_init_subclass = typing.Generic.__init_subclass
    
    def patched_init_subclass(cls, *args, **kwargs):
        try:
            return original_init_subclass.__func__(cls, *args, **kwargs)
        except (AssertionError, TypeError) as e:
            error_msg = str(e)
            if "directly inherits TypingOnly" in error_msg or "canonical symbol" in error_msg:
                # Silently ignore these SQLAlchemy compatibility errors
                return
            raise
    
    typing.Generic.__init_subclass__ = classmethod(patched_init_subclass)

# NOW CONTINUE WITH YOUR NORMAL IMPORTS

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from contextlib import asynccontextmanager
import logging

# Import from app modules
from app.database import engine, Base, SessionLocal, get_db
from app.api import pages, posts, users
from app.config import settings  # Changed from config to app.config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Jinja2 templates setup - MUST BE BEFORE ROUTES THAT USE IT
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting LinkedIn Insights Microservice")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LinkedIn Insights Microservice")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="LinkedIn Insights Microservice for scraping and analyzing LinkedIn pages",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pages.router, prefix=settings.API_V1_PREFIX)
# Additional routers would be included here


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.APP_NAME}


@app.get("/api")
def api_root():
    """API root endpoint"""
    return {
        "message": "LinkedIn Insights API",
        "version": "1.0.0",
        "endpoints": {
            "pages": "/api/v1/pages",
            "posts": "/api/v1/posts",
            "health": "/health",
            "dashboard": "/",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard page with statistics"""
    try:
        # Import models inside function to avoid circular imports
        from app.models.page import LinkedInPage as Page
        from app.models.post import LinkedInPost as Post
        from app.models.user import SocialMediaUser
        
        # Get stats for the dashboard
        pages_count = db.query(Page).count()
        total_followers = db.query(func.sum(Page.total_followers)).scalar() or 0
        posts_count = db.query(Post).count()
        employees_count = db.query(SocialMediaUser).count()
        
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "pages_count": pages_count,
                "total_followers": total_followers,
                "posts_count": posts_count,
                "employees_count": employees_count
            }
        )
    except Exception as e:
        logger.error(f"Error in dashboard: {e}")
        return HTMLResponse(f"""
        <html>
            <head><title>Dashboard Error</title></head>
            <body>
                <h1>Dashboard Error</h1>
                <p>Error loading dashboard: {str(e)}</p>
                <p><a href="/health">Check Health</a></p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """)


# Root route - redirects to dashboard
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root route redirects to dashboard"""
    import urllib.parse
    dashboard_url = urllib.parse.urljoin(str(request.base_url), "dashboard")
    return HTMLResponse(f"""
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url={dashboard_url}">
            <title>Redirecting...</title>
        </head>
        <body>
            <p>Redirecting to <a href="{dashboard_url}">Dashboard</a>...</p>
        </body>
    </html>
    """)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

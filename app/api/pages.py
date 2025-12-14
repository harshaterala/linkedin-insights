from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.schemas.page import (
    PageInDB, PageFilter, PaginatedPages, 
    PageWithDetails, PageCreate, PageUpdate
)
from app.schemas.post import PostInDB, PostWithComments
from app.schemas.user import SocialMediaUserInDB
from app.services.page_service import PageService, PostService
from app.models.page import SocialMediaUser
from app.models.post import Post
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pages", tags=["pages"])


@router.get("/{page_id}", response_model=PageWithDetails)
def get_page(
    page_id: str,
    scrape_if_missing: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get page details by LinkedIn page ID.
    
    - **page_id**: LinkedIn page ID (from URL)
    - **scrape_if_missing**: If True, scrape page if not in database
    """
    # Try to get from database first
    page = PageService.get_page_by_page_id(db, page_id)
    
    # If not found and scraping is enabled, scrape it
    if not page and scrape_if_missing:
        page = PageService.scrape_and_save_page(db, page_id)
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with ID '{page_id}' not found"
        )
    
    # Get additional counts
    posts_count = db.query(Post).filter(Post.page_id == page.id).count()
    employees_count = db.query(SocialMediaUser).filter(SocialMediaUser.page_id == page.id).count()
    
    return PageWithDetails(
        **page.__dict__,
        posts_count=posts_count,
        employees_count=employees_count
    )


@router.post("/{page_id}/scrape", response_model=PageInDB)
def scrape_page(
    page_id: str,
    db: Session = Depends(get_db)
):
    """
    Force scrape a page and save to database.
    """
    page = PageService.scrape_and_save_page(db, page_id)
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to scrape page with ID '{page_id}'"
        )
    
    return page


@router.get("/", response_model=PaginatedPages)
def search_pages(
    min_followers: Optional[int] = Query(None, ge=0),
    max_followers: Optional[int] = Query(None, ge=0),
    name: Optional[str] = None,
    industry: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search pages with filters and pagination.
    
    - **min_followers**: Minimum follower count
    - **max_followers**: Maximum follower count
    - **name**: Search by page name (partial match)
    - **industry**: Filter by industry
    - **page**: Page number
    - **size**: Items per page
    """
    filters = PageFilter(
        min_followers=min_followers,
        max_followers=max_followers,
        name=name,
        industry=industry,
        page=page,
        size=size
    )
    
    return PageService.search_pages(db, filters)


@router.get("/{page_id}/employees", response_model=List[SocialMediaUserInDB])
def get_page_employees(
    page_id: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get employees/people working at a page.
    
    - **page_id**: LinkedIn page ID
    - **limit**: Maximum number of employees to return
    """
    page = PageService.get_page_by_page_id(db, page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with ID '{page_id}' not found"
        )
    
    employees = PageService.get_page_employees(db, page.id, limit)
    return employees


@router.get("/{page_id}/posts", response_model=List[PostInDB])
def get_page_posts(
    page_id: str,
    limit: int = Query(15, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recent posts for a page.
    
    - **page_id**: LinkedIn page ID
    - **limit**: Maximum number of posts to return
    """
    page = PageService.get_page_by_page_id(db, page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with ID '{page_id}' not found"
        )
    
    posts = PageService.get_recent_posts(db, page.id, limit)
    return posts


@router.get("/posts/{post_id}/comments", response_model=PostWithComments)
def get_post_comments(
    post_id: int,
    scrape_if_missing: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get comments for a post.
    
    - **post_id**: Database ID of the post
    - **scrape_if_missing**: If True, scrape comments if not in database
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID '{post_id}' not found"
        )
    
    # Scrape comments if requested and not already in database
    if scrape_if_missing:
        PostService.scrape_and_save_comments(db, post)
    
    comments = PostService.get_post_comments(db, post_id)
    
    return PostWithComments(
        **post.__dict__,
        comments=comments
    )


@router.get("/{page_id}/followers-range")
def get_pages_in_follower_range(
    page_id: str,
    range_percent: float = Query(10.0, ge=1.0, le=100.0),
    db: Session = Depends(get_db)
):
    """
    Find pages with similar follower count (±range_percent).
    
    - **page_id**: Reference page ID
    - **range_percent**: Percentage range for follower count
    """
    page = PageService.get_page_by_page_id(db, page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with ID '{page_id}' not found"
        )
    
    range_value = page.total_followers * (range_percent / 100)
    min_followers = max(0, page.total_followers - range_value)
    max_followers = page.total_followers + range_value
    
    similar_pages = db.query(Page).filter(
        Page.id != page_odj.id,
        Page.total_followers >= min_followers,
        Page.total_followers <= max_followers
    ).limit(10).all()
    
    return {
        "reference_page": page.name,
        "reference_followers": page.total_followers,
        "range_percent": range_percent,
        "similar_pages": similar_pages
    }
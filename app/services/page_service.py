from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
import logging

from app.models.page import Page, SocialMediaUser
from app.models.post import Post, Comment
from app.schemas.page import PageCreate, PageUpdate, PageFilter, PaginatedPages
from app.schemas.post import PostCreate, CommentBase
import app.services.scraper as scraper_module

logger = logging.getLogger(__name__)


class PageService:
    @staticmethod
    def get_page_by_id(db: Session, page_id: int) -> Optional[Page]:
        return db.query(Page).filter(Page.id == page_id).first()
    
    @staticmethod
    def get_page_by_page_id(db: Session, page_id: str) -> Optional[Page]:
        return db.query(Page).filter(Page.page_id == page_id).first()
    
    @staticmethod
    def create_page(db: Session, page_data: PageCreate) -> Page:
        db_page = Page(**page_data.dict())
        db.add(db_page)
        db.commit()
        db.refresh(db_page)
        return db_page
    
    @staticmethod
    def update_page(db: Session, page: Page, update_data: PageUpdate) -> Page:
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(page, field, value)
        
        db.add(page)
        db.commit()
        db.refresh(page)
        return page
    
    @staticmethod
    def search_pages(db: Session, filters: PageFilter) -> PaginatedPages:
        query = db.query(Page)
        
        if filters.min_followers is not None:
            query = query.filter(Page.total_followers >= filters.min_followers)
        
        if filters.max_followers is not None:
            query = query.filter(Page.total_followers <= filters.max_followers)
        
        if filters.name:
            query = query.filter(Page.name.ilike(f"%{filters.name}%"))
        
        if filters.industry:
            query = query.filter(Page.industry.ilike(f"%{filters.industry}%"))
        
        total = query.count()
        offset = (filters.page - 1) * filters.size
        pages = query.offset(offset).limit(filters.size).all()
        
        total_pages = (total + filters.size - 1) // filters.size
        
        return PaginatedPages(
            items=pages,
            total=total,
            page=filters.page,
            size=filters.size,
            pages=total_pages
        )
    
    @staticmethod
    def scrape_and_save_page(db: Session, page_id: str) -> Optional[Page]:
        try:
            existing_page = PageService.get_page_by_page_id(db, page_id)
            if existing_page:
                logger.info(f"Page {page_id} already exists in database")
                return existing_page
            
            # Mock implementation - in real app, use actual scraper
            from app.services.scraper import scraper
            scraped_data = scraper.scrape_page(page_id)
            
            if not scraped_data:
                logger.error(f"Failed to scrape page {page_id}")
                return None
            
            page_dict = {
                "page_id": scraped_data.page_id,
                "name": scraped_data.name,
                "url": scraped_data.url,
                "profile_picture_url": scraped_data.profile_picture_url,
                "description": scraped_data.description,
                "website": scraped_data.website,
                "industry": scraped_data.industry,
                "total_followers": scraped_data.total_followers,
                "head_count": scraped_data.head_count,
                "specialities": scraped_data.specialities,
                "location": scraped_data.location,
                "founded_year": scraped_data.founded_year,
                "company_type": scraped_data.company_type,
            }
            
            page_create = PageCreate(**page_dict)
            page = PageService.create_page(db, page_create)
            
            return page
            
        except Exception as e:
            logger.error(f"Error in scrape_and_save_page for {page_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_page_employees(db: Session, page_id: int, limit: int = 20) -> List[SocialMediaUser]:
        return db.query(SocialMediaUser).filter(
            SocialMediaUser.page_id == page_id
        ).limit(limit).all()
    
    @staticmethod
    def get_recent_posts(db: Session, page_id: int, limit: int = 15) -> List[Post]:
        return db.query(Post).filter(
            Post.page_id == page_id
        ).order_by(Post.posted_at.desc()).limit(limit).all()


class PostService:
    @staticmethod
    def get_post_comments(db: Session, post_id: int, limit: int = 50) -> List[Comment]:
        return db.query(Comment).filter(
            Comment.post_id == post_id
        ).order_by(Comment.commented_at.desc()).limit(limit).all()
    
    @staticmethod
    def scrape_and_save_comments(db: Session, post: Post):
        try:
            if not post.post_url:
                return
            
            # Mock implementation
            from app.services.scraper import scraper
            scraped_comments = scraper.scrape_post_comments(post.post_url)
            
            for comment_data in scraped_comments:
                comment = Comment(
                    linkedin_comment_id=f"comment_{post.id}_{len(scraped_comments)}",
                    content=comment_data["content"],
                    commenter_name=comment_data["commenter_name"],
                    commenter_headline=comment_data["commenter_headline"],
                    post_id=post.id
                )
                db.add(comment)
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error saving comments for post {post.id}: {str(e)}")
            db.rollback()

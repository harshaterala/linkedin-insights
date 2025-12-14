from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class PageBase(BaseModel):
    page_id: str
    name: str
    url: Optional[str] = None
    linkedin_id: Optional[str] = None
    profile_picture_url: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    total_followers: int = 0
    head_count: Optional[int] = None
    specialities: Optional[List[str]] = None
    location: Optional[str] = None
    founded_year: Optional[int] = None
    company_type: Optional[str] = None


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    name: Optional[str] = None
    total_followers: Optional[int] = None
    head_count: Optional[int] = None
    description: Optional[str] = None


class PageInDB(PageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_scraped_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PageWithDetails(PageInDB):
    posts_count: Optional[int] = None
    employees_count: Optional[int] = None


class PageFilter(BaseModel):
    min_followers: Optional[int] = None
    max_followers: Optional[int] = None
    name: Optional[str] = None
    industry: Optional[str] = None
    page: int = 1
    size: int = 10


class PaginatedPages(BaseModel):
    items: List[PageInDB]
    total: int
    page: int
    size: int
    pages: int

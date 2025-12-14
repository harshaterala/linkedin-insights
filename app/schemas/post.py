from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    commenter_name: str
    commenter_profile_url: Optional[str] = None
    commenter_headline: Optional[str] = None


class CommentInDB(CommentBase):
    id: int
    post_id: int
    commented_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    linkedin_post_id: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    post_url: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0


class PostCreate(PostBase):
    page_id: int


class PostInDB(PostBase):
    id: int
    page_id: int
    posted_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PostWithComments(PostInDB):
    comments: List[CommentInDB] = []

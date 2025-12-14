from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    linkedin_post_id = Column(String(100), unique=True, index=True)
    content = Column(Text)
    image_url = Column(String(500))
    video_url = Column(String(500))
    post_url = Column(String(500))
    
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    page_id = Column(Integer, ForeignKey("pages.id"))
    
    posted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    page = relationship("Page", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Post {self.linkedin_post_id[:20]}...>"


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    linkedin_comment_id = Column(String(100), unique=True, index=True)
    content = Column(Text)
    
    commenter_name = Column(String(200))
    commenter_profile_url = Column(String(500))
    commenter_headline = Column(String(500))
    
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    commented_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment by {self.commenter_name}>"

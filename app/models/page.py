from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Page(Base):
    __tablename__ = "pages"
    
    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    url = Column(String(500))
    linkedin_id = Column(String(100), unique=True)
    profile_picture_url = Column(String(500))
    description = Column(Text)
    website = Column(String(500))
    industry = Column(String(200))
    total_followers = Column(Integer, default=0)
    head_count = Column(Integer)
    specialities = Column(JSON)
    location = Column(String(200))
    founded_year = Column(Integer)
    company_type = Column(String(100))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    posts = relationship("Post", back_populates="page", cascade="all, delete-orphan")
    employees = relationship("SocialMediaUser", back_populates="page")
    
    def __repr__(self):
        return f"<Page {self.name} ({self.page_id})>"


class SocialMediaUser(Base):
    __tablename__ = "social_media_users"
    
    id = Column(Integer, primary_key=True, index=True)
    linkedin_id = Column(String(100), unique=True, index=True)
    name = Column(String(200), nullable=False)
    profile_url = Column(String(500))
    profile_picture_url = Column(String(500))
    headline = Column(String(500))
    current_position = Column(String(200))
    
    page_id = Column(Integer, ForeignKey("pages.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    page = relationship("Page", back_populates="employees")
    
    def __repr__(self):
        return f"<SocialMediaUser {self.name}>"

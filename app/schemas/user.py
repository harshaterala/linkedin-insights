from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class SocialMediaUserBase(BaseModel):
    linkedin_id: Optional[str] = None
    name: str
    profile_url: Optional[str] = None
    profile_picture_url: Optional[str] = None
    headline: Optional[str] = None
    current_position: Optional[str] = None


class SocialMediaUserCreate(SocialMediaUserBase):
    page_id: int


class SocialMediaUserInDB(SocialMediaUserBase):
    id: int
    page_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

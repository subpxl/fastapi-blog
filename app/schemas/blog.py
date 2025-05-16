from typing import List
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from models import BlogStatus


class BlogBase(BaseModel):
    title:str
    description:str
    status:str=BlogStatus.draft
    schedule_publish_at:Optional[datetime]=None

class BlogCreate(BlogBase):
    pass


class BlogResponse(BlogBase):
    id:int
    # user_id:str
    user_id: Optional[str] = None

    class Config:   
        # orm_mode =True
        from_attributes = True 


class PaginatedBlogResponse(BaseModel):
    blogs: List[BlogResponse]
    total: int
    page: int
    size: int
    pages: int

import enum
from sqlalchemy import Column,DateTime,Integer,String,Enum

from database import Base

class BlogStatus(enum.Enum):
    draft ="draft"
    publish  = "publish"

class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(String(50))
    title=Column(String(50),unique =True)
    description=Column(String(255))
    status=Column(Enum(BlogStatus),default=BlogStatus.draft)
    created_at=Column(DateTime)
    schedule_publish_at=Column(DateTime)
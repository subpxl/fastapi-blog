from typing import List
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from models import  Blog
from database import get_db
from sqlalchemy import and_
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def publish_scheduled_blogs()-> None :
    try:
        logger.info("Checking for scheduled blogs to publish...")
        db = next(get_db())  
        now = datetime.utcnow()
        
        scheduled_blogs :List[Blog] = db.query(Blog).filter(
            and_(
                Blog.status == "draft",
                Blog.schedule_publish_at != None,
                Blog.schedule_publish_at <= now
            )
        ).all()
        
        count = 0
        for blog in scheduled_blogs:
            blog.status = "publish"
            count += 1
            logger.info(f"Publishing blog: {blog.title}")
        
        db.commit()
        logger.info(f"Published {count} blogs")
        
    except Exception as e:
        logger.error(f"Error in publish_scheduled_blogs: {str(e)}")
    finally:
        db.close()

def schedule_blog_publishing(blog_id :str, publish_at:any) -> None :
    job_id = f"publish_blog_{blog_id}_{publish_at.timestamp()}"
    
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    scheduler.add_job(
        publish_specific_blog,
        trigger=DateTrigger(run_date=publish_at),
        args=[blog_id],
        id=job_id,
        name=f"Publish blog {blog_id} at {publish_at}"
    )
    logger.info(f"Scheduled blog {blog_id} to be published at {publish_at}")

def publish_specific_blog(blog_id:str) -> None:
    try:
        db = next(get_db())  
        blog:Blog = db.query(Blog).filter(Blog.id == blog_id).first()
        
        if blog and blog.status == "draft":
            blog.status = "publish"
            db.commit()
            logger.info(f"Published blog {blog_id}: {blog.title}")
        else:
            logger.warning(f"Blog {blog_id} not found or not in draft status")
            
    except Exception as e:
        logger.error(f"Error publishing blog {blog_id}: {str(e)}")
    finally:
        db.close()

def start_scheduler() -> None:
    scheduler.add_job(
        publish_scheduled_blogs,
        'interval',
        minutes=1,
        id='check_scheduled_blogs',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Blog publishing scheduler started")

def shutdown_scheduler() -> None:
    scheduler.shutdown()
    logger.info("Blog publishing scheduler stopped")
from fastapi import APIRouter,Depends,status,Query,HTTPException
from sqlalchemy.orm import Session
from typing import  Optional
from scheduler import schedule_blog_publishing
from schemas.blog import   BlogCreate,BlogResponse,PaginatedBlogResponse
from sqlalchemy.exc import SQLAlchemyError

from database import get_db
from models import Blog,User,BlogStatus
from helper import get_current_user


router=APIRouter()

    
@router.get("/public", response_model=PaginatedBlogResponse)
async def get_blogs(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="search blogs by title"),
    page: int = Query(1, ge=1, description="page number"),
    size: int = Query(10, ge=1, le=100, description="items per page"),  
    status: Optional[BlogStatus] = Query(None, description="fiter blogs by status"),

):
    try:
        query = db.query(Blog)
        if status:
            query = query.filter(Blog.status == status)
        else:
            query = query.filter(Blog.status == BlogStatus.publish)

        if search:
            query = query.filter(Blog.title.ilike(f"%{search}%"))
    
        total: int = query.count()
        

        pages = (total + size - 1) // size if total > 0 else 0
        offset = (page - 1) * size
        
        blogs = query.offset(offset).limit(size).all()

        return {
            "blogs": blogs,  
            "total": total,
            "page": page,     
            "size": size,    
            "pages": pages   
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch blogs from the database. {e}"
        )
    


@router.get("/{blog_id}",response_model=BlogResponse)
def get_blog(blog_id: str, db:Session =Depends(get_db)):
    blog = db. query(Blog).filter(Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found"
        )
    return blog


@router.post("/",response_model=BlogResponse)
def create_blogs(blog:BlogCreate,
                 db:Session=Depends(get_db),
                 current_user:User= Depends(get_current_user)):

    blog_found  = db.query(Blog).filter(Blog.title==blog.title).first()
    if blog_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blog title already exists"
        )

    blogstatus =""
    if blog.schedule_publish_at != None:
        blogstatus = "draft"
    else:
        blogstatus = "publish"

    new_blog = Blog(
        title=blog.title,
        description=blog.description,
        # status=blog.status,
        status=blogstatus,
        # user_id="anonymous",  
        user_id=current_user.username,
        schedule_publish_at=blog.schedule_publish_at
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    if blog.schedule_publish_at and blog.status == "draft":
        schedule_blog_publishing(new_blog.id, blog.schedule_publish_at)
    return new_blog


@router.put("/{blog_id}",response_model=BlogResponse)
def update_blog(blog_id: str,
                blog:BlogCreate, 
                db:Session=Depends(get_db),
                current_user:User=Depends(get_current_user)
                ):
    
    found_blog = db.query(Blog).filter(Blog.id == int( blog_id)).first()
    if not found_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found"
        )
    
    if found_blog.user_id !=current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized "
        )
    
    found_blog.title = blog.title
    found_blog.description = blog.description
    found_blog.status = blog.status
    found_blog.schedule_publish_at = blog.schedule_publish_at
    
    db.commit()
    db.refresh(found_blog)
 
    if blog.schedule_publish_at and blog.status == "draft":
        try:
            schedule_blog_publishing(found_blog.id, blog.schedule_publish_at)
        except Exception as e:
            print(f"error scheduling blog",e)

    return found_blog    



@router.delete("/{blog_id}")
def delete_blog(blog_id: str,
                db :Session=Depends(get_db),
                current_user: User = Depends(get_current_user)
            ):

    found_blog = db.query(Blog).filter(Blog.id == int( blog_id)).first()
    if not found_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found"
        )
    
    if found_blog.user_id != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="unauthorized"
        )
        
    db.delete(found_blog)
    db.commit()

    return {"message":f"blog is  deleted {blog_id} "}


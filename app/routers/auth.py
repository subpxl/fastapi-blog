from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from helper import  get_user, verify_password,create_access_token,get_password_hast
from database import get_db
from models import User
from schemas  import  Token,UserCreate
from config import ACCESS_TOKEN_EXPIRE_MINUTES




router = APIRouter()

@router.post("/login",response_model=Token)
async def login(form_data:OAuth2PasswordRequestForm =Depends(),db:Session=Depends(get_db)):
    user = get_user(db,username=form_data.username)
    if not user or not verify_password(form_data.password,user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrenct username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(
        data={"sub":user.username},
        expires_delta=access_token_expires
    )

    return {"access_token":access_token,"token_type":"bearer"}


@router.post("/register",response_model=dict)
async def register(user:UserCreate,db:Session=Depends(get_db)):
    db_user = get_user(db,username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    email_exists = db.query(User).filter(User.email==user.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already registered"
        )
    
    hashed_password = get_password_hast(user.password)
    new_user = User(
        username=user.username,
        email = user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"user created successfully"}

@router.post("/logout")
async def logout():
    expired_token = create_access_token(
        data={"sub":"logout"},
        expires_delta=timedelta(seconds=0)
    )
    return JSONResponse(
        content={
            "message":"logged out successfully",
            "access_token":expired_token,
            "token_type":"bearer"
        }
    )
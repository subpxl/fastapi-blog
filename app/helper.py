# helper funcions auth
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError,jwt
from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
from database import get_db
from schemas import TokenData
from models import User
from config import ALGORITHM,SECRET_KEY


pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hast(password)->str:
    return pwd_context.hash(password)

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None) -> str:
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now()+expires_delta
    else:
        expire = datetime.now()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db:Session,username:str)-> (User | None):
    return db.query(User).filter(User.username==username).first()

async def  get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db))-> User:
    credentials_execption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credentials_execption
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_execption
    user = get_user(db,username=token_data.username)
    if user is None:
        raise credentials_execption
    return user
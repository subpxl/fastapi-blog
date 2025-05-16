from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:Optional[str]=None

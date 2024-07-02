from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    nama_user: str
    password: str
    
class TokenVerify(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    valid: bool
    
class TokenCreate(BaseModel):
    email: str
    password: str

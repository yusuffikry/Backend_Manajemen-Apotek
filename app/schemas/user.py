from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    nama_user: str
    role: int
    email: EmailStr
    alamat: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id_user: int
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nama_user: Optional[str] = None
    role: Optional[int] = None
    email: Optional[EmailStr] = None
    alamat: Optional[str] = None
    password: Optional[str] = None
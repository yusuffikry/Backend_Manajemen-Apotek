from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import User as UserModel
from ..database import get_db
from ..schemas.user import *
from sqlalchemy.orm import Session
from fastapi import Depends
from ..deps import get_current_user
from passlib.context import CryptContext
from icecream import ic


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = UserModel(**user.dict())
    db_user.password = pwd_context.hash(db_user.password)
    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[User],status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=User,status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User,status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Konversi model Pydantic ke objek yang dapat diubah (dict)
    ic(user)
    user_data = user.dict(exclude_unset=True)
    if user_data.get('password'):
        user_data['password'] = pwd_context.hash(user_data['password'])
    # ic(user_data)
    
    # Perbarui entri basis data
    db.query(UserModel).filter(UserModel.id_user == user_id).update(user_data)
    db.commit()
    
    # Perbarui objek db_user dengan nilai-nilai yang baru
    db_user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    return db_user

@router.delete("/{user_id}", response_model=User,status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
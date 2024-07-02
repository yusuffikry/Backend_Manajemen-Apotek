from datetime import datetime, timedelta

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError,PyJWTError
from passlib.context import CryptContext
# from .. import  models, database
from sqlalchemy.orm import Session
from typing import Optional
# from .. import oauth2_scheme
from ..schemas.auth import *
from ..schemas.user import *
from icecream import ic
from ..database import get_db
from ..models import User as UserModel, AkunToken as TokenModel
from ..deps import get_current_user

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "8cd040f551663c0d21f94dc02336bef65cbb51af6ebe71dc9768458b2dc01371"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ic(pwd_context.hash("password"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    # ic(username,password)
    user = db.query(UserModel).filter(UserModel.nama_user == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def authenticate_token(db: Session, email: str, password: str):
    user = db.query(TokenModel).filter(TokenModel.Email == email).first()
    if not user:
        return False
    if not verify_password(password, user.Password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# @router.post("/register", response_model=UserLogin,status_code=201)
# def register(user: UserLogin, db: Session = Depends(get_db)):
#     hashed_password = get_password_hash(user.password)
#     db_user = UserModel(nama_user=user.nama_user, password=hashed_password,role=1)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return user

@router.post("/login",status_code=status.HTTP_200_OK)
def login(form_data: UserLogin, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = authenticate_user(db, form_data.nama_user, form_data.password)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect email or password",
        )
    
    return user
    # return form_data
    # return db.query(UserModel).all()

@router.post("/token", status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_token(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.Email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.get("/me", response_model=None,status_code=status.HTTP_200_OK)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
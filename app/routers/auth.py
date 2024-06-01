from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError,PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing_extensions import Annotated
from .. import schemas, models, database
from sqlalchemy.orm import Session
from typing import Optional

from icecream import ic

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "8cd040f551663c0d21f94dc02336bef65cbb51af6ebe71dc9768458b2dc01371"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

password = pwd_context.hash("password")

ic(password)

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": password,
        "disabled": False,
    }
}

# ic(fake_users_db)







router = APIRouter()


def decode_token(token: str):
    try:
        # Decode the token using jwt.decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Assuming 'user_id' is the key in the payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        email = decode_token(token)
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.nama_user == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.UserBase)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token", response_model=schemas.TokenVerify)
def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        email = decode_token(token)
        if email is None:
            return {"email": None, "valid": False}
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            return {"email": None, "valid": False}
        return {"email": user.email,"username": user.nama_user, "valid": True}
    except PyJWTError:
        return {"email": None, "valid": False}
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from . import models
from .database import get_db
from .config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="auth/login",
)



def decode_token(token: str):
    try:
        # Decode the token using jwt.decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Assuming 'user_id' is the key in the payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
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
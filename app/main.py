from fastapi import FastAPI
# from fastapi.responses import JSONResponse
import uvicorn
# from app.auth import auth_exception_handler
from .database import SessionLocal, engine,get_db
from fastapi.security import OAuth2PasswordBearer
from .routers import obat,pemasok,transaksi,user,auth

# from .auth import router
import icecream as ic
from . import models
import logging

# logger = logging.getLogger('uvicorn.error')
models.Base.metadata.create_all(bind=engine)


# ic(router)

#Dependency
# def get_db():
#     db = SessionLocal()
#     try : 
#         yield db
#     finally:
#         db.close()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

origins = [
    # "http://localhost:3000",
    # "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Mengizinkan asal tertentu
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode HTTP
    allow_headers=["*"],  # Mengizinkan semua header
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(protected.router, prefix="/protected", tags=["protected"])
app.include_router(obat.router, prefix="/api/obat", tags=["obat"])
# app.include_router(pelanggan.router, prefix="/api/pelanggan", tags=["pelanggan"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(pemasok.router, prefix="/api/pemasok", tags=["pemasok"])
app.include_router(transaksi.router, prefix="/api/transaksi", tags=["transaksi"])

from sqlalchemy.orm import Session
from fastapi import Depends
@app.get("/create_token")
async def create_token_akun(db: Session = Depends(get_db)):

    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = pwd_context.hash("admin")
    tokens = models.AkunToken(Email="admin", Password=password)
    db.add(tokens)
    db.commit()
    db.refresh(tokens)
    return tokens

# create / endpoint for testing
@app.get("/")
def read_root():
    return {"Hello": "World"}




# # Add exception handler for JWT errors
# @app.exception_handler(auth_exception_handler)
# def authjwt_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


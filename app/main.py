from fastapi import FastAPI
# from fastapi.responses import JSONResponse
import uvicorn
# from app.auth import auth_exception_handler
from .database import SessionLocal, engine
from .routers import obat, auth, protected, pelanggan,user,pemasok,transaksi
from . import models
models.Base.metadata.create_all(bind=engine)

#Dependency
# def get_db():
#     db = SessionLocal()
#     try : 
#         yield db
#     finally:
#         db.close()

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(protected.router, prefix="/protected", tags=["protected"])
app.include_router(obat.router, prefix="/api/obat", tags=["obat"])
# app.include_router(pelanggan.router, prefix="/api/pelanggan", tags=["pelanggan"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(pemasok.router, prefix="/api/pemasok", tags=["pemasok"])
app.include_router(transaksi.router, prefix="/api/transaksi", tags=["transaksi"])

# # Add exception handler for JWT errors
# @app.exception_handler(auth_exception_handler)
# def authjwt_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


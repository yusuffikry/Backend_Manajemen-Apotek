# from fastapi import Depends, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from pydantic import BaseModel

# class Settings(BaseModel):
#     authjwt_secret_key: str = "secret"

# @AuthJWT.load_config
# def get_config():
#     return Settings()

# # Exception handler for auth errors
# def auth_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )

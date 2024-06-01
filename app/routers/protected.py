# from fastapi import APIRouter, Depends
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from fastapi import HTTPException, Security

# # Create a router object
# router = APIRouter()

# # Function to get the current user
# def get_current_user(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#     except AuthJWTException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.message)

#     current_user = Authorize.get_jwt_subject()
#     return current_user

# # Protected route
# @router.get('/protected')
# def protected(Authorize: AuthJWT = Depends()):
#     user = get_current_user(Authorize)
#     return {"user": user}

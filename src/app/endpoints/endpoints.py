from fastapi import APIRouter, HTTPException, status
from app.schemas.schemas import User
from app.core.service import AuthService

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(user: User):
    token = AuthService.registrate_user(user.login, user.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exist")
    return token


@auth_router.post("/auth", status_code=status.HTTP_200_OK)
async def authorize_user(user: User):
    token = AuthService.authorize_user(user.login, user.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return token

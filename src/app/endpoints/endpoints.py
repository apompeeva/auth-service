from fastapi import APIRouter, HTTPException, status

from app.core.service import AuthService
from app.schemas.schemas import AuthResponse, User

auth_router = APIRouter()


@auth_router.get('/check_token', status_code=status.HTTP_200_OK)
async def check_token(user_id: int):
    """Проверяет валидность токена для пользователя по id."""
    if not AuthService.is_token_exist(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Token not exist',
        )
    elif AuthService.is_token_expired(AuthService.get_token(user_id)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized',
        )


@auth_router.post(
    '/register', status_code=status.HTTP_200_OK, response_model=AuthResponse,
)
async def register_user(user: User):
    """Регистрация пользователя."""
    token = AuthService.registrate_user(user.login, user.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='User already exist',
        )
    return AuthResponse(access_token=token)


@auth_router.post('/auth', status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def authorize_user(user: User):
    """Авторизация пользователя."""
    token = AuthService.authorize_user(user.login, user.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found',
        )
    return AuthResponse(access_token=token)


@auth_router.get('/healthz/ready', status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка работоспособности сервиса."""
    return 'Ok'

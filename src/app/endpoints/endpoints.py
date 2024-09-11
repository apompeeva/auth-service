import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from opentracing import global_tracer
from redis import Redis

from app.core.service import AuthService
from app.metrics import READINESS_STATE
from app.producer.producer import producer
from app.redis import get_redis
from app.schemas.schemas import AuthResponse, User

auth_router = APIRouter()
UPLOAD_DIR = '/images'


@auth_router.get('/check_token', status_code=status.HTTP_200_OK)
async def check_token(user_id: int, redis: Redis = Depends(get_redis)):
    """Проверяет валидность токена для пользователя по id."""
    with global_tracer().start_active_span('check_token') as scope:
        scope.span.set_tag('user_id', user_id)
        if not AuthService.is_token_exist(user_id, redis):
            scope.span.set_tag('error', 'Token not exist')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Token not exist',
            )
        elif AuthService.is_token_expired(AuthService.get_token(user_id, redis)):
            scope.span.set_tag('error', 'User unauthorized')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized',
            )


@auth_router.post(
    '/register', status_code=status.HTTP_200_OK, response_model=AuthResponse,
)
async def register_user(user: User):
    """Регистрация пользователя."""
    with global_tracer().start_active_span('register_user') as scope:
        token = await AuthService.registrate_user(user.login, user.password)
        scope.span.set_tag('user_login', user.login)
        if token is None:
            scope.span.set_tag('error', 'User already exist')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='User already exist',
            )
        return AuthResponse(access_token=token)


@auth_router.post('/auth', status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def authorize_user(user: User, redis: Redis = Depends(get_redis)):
    """Авторизация пользователя."""
    with global_tracer().start_active_span('authorize_user') as scope:
        scope.span.set_tag('user_login', user.login)
        token = await AuthService.authorize_user(user.login, user.password, redis)
        if token is None:
            scope.span.set_tag('error', 'User not found')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found',
            )
        return AuthResponse(access_token=token)


@auth_router.get('/healthz/ready', status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка работоспособности сервиса."""
    if not await producer.health_check():
        READINESS_STATE.labels(
            service='auth',
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        ).set(0)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service unavailable',
        )
    else:
        READINESS_STATE.labels(service='auth', status=status.HTTP_200_OK).set(1)


@auth_router.post('/api/verify', status_code=status.HTTP_200_OK)
async def verify_user(user_id: int, file: UploadFile):
    """Верификация пользователя."""
    with global_tracer().start_active_span('verify_user') as scope:
        if not AuthService.is_token_exist(user_id):
            scope.span.set_tag('error', 'Token not exist')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Token not exist',
            )
        elif AuthService.is_token_expired(AuthService.get_token(user_id)):
            scope.span.set_tag('error', 'User unauthorized')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized',
            )
        else:
            new_filename = '_'.join(
                [str(user_id), str(datetime.datetime.now()), str(file.filename)],
            )
            file_location = Path(UPLOAD_DIR) / new_filename
            with open(file_location, 'wb') as buffer:
                buffer.write(await file.read())
                await producer.send_and_wait(f'{user_id}@{str(file_location)}')
                return {'message': 'File saved successfully'}

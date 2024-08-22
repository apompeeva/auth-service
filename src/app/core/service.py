import datetime
from dataclasses import asdict, dataclass

import jwt
from passlib.hash import pbkdf2_sha256

from app.config import EXPIRATION_TIME, SECRET  # type: ignore
from app.crud.users_crud import create_new_user, get_user_by_login


@dataclass
class User:
    """Данные пользователя."""

    login: str
    password: str
    is_verified: bool = False
    balance: int = 0

    def dict(self):
        """Возращает словарь."""
        return asdict(self)


class AuthService:
    """Cервис авторизации."""

    users: dict = {}
    token_storage: dict = {}
    users_by_id: dict = {}

    @classmethod
    def verify_user(cls, user_id: int):
        """Проставляет метку о верификации пользователя."""
        cls.users_by_id[user_id].verified = True
        login = cls.users_by_id[user_id].login
        cls.users[login].verified = True

    @staticmethod
    def create_token(login: str) -> str:
        """Возвращает сгенерированный jwt токен."""
        return jwt.encode(
            {
                'username': login,
                'exp': datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=EXPIRATION_TIME),
            },
            SECRET,
            algorithm='HS256',
        )

    @classmethod
    async def is_user_exist(cls, login: str) -> bool:
        """Проверяет, существует ли юзер с таким логином."""
        user = await get_user_by_login(login)
        return user is not None

    @classmethod
    def is_token_exist(cls, user_id: int):
        """Проверяет есть ли для юзера токен в хранилище."""
        return user_id in cls.token_storage

    @classmethod
    def get_token(cls, user_id: int):
        """Возвращает токен по user_id."""
        if user_id not in cls.token_storage:
            return None
        return cls.token_storage[user_id]

    @staticmethod
    def is_token_expired(token: str):
        """Проверяет не истек ли срок дейтвия токена."""
        try:
            jwt.decode(token, SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return True
        return False

    @classmethod
    async def registrate_user(cls, login: str, password: str) -> str | None:
        """Регистрация пользователя."""
        if not isinstance(login, str) or not isinstance(password, str):
            raise TypeError('String expected.')

        if await cls.is_user_exist(login):
            return None

        access_token = cls.create_token(login)
        # to be deleted
        user_id = len(cls.users) + 1
        new_user = User(login, pbkdf2_sha256.hash(password))
        cls.users[login] = new_user
        cls.users_by_id[user_id] = new_user
        # ---
        await create_new_user(new_user.dict())
        return access_token

    @classmethod
    async def authorize_user(cls, login: str, password: str) -> str | None:
        """Авторизация пользователя."""
        if not isinstance(login, str) or not isinstance(password, str):
            raise TypeError('String expected.')
        if not cls.is_user_exist(login):
            return None
        current_user = await get_user_by_login(login)
        if not pbkdf2_sha256.verify(password, current_user.password):
            return None
        if cls.is_token_exist(current_user.id):
            token = cls.token_storage[current_user.id]
            if cls.is_token_expired(token):
                token = cls.create_token(login)
                cls.token_storage[current_user.id] = token
        else:
            token = cls.create_token(login)
            cls.token_storage[current_user.id] = token
        return token

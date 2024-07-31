import datetime
from dataclasses import dataclass

import jwt
from passlib.hash import pbkdf2_sha256

from app.config import EXPIRATION_TIME, SECRET  # type: ignore


@dataclass
class User:
    """Данные пользователя."""

    id: int
    login: str
    password: str
    access_token: str | None = None


class AuthService:
    """Cервис авторизации."""

    users: dict = {}
    token_storage: dict = {}

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
    def is_user_exist(cls, login: str) -> bool:
        """Проверяет, существует ли юзер с таким логином."""
        return login in cls.users

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
    def registrate_user(cls, login: str, password: str) -> str | None:
        """Регистрация пользователя."""
        if not isinstance(login, str) or not isinstance(password, str):
            raise TypeError('String expected.')

        if login in cls.users:
            return None

        access_token = cls.create_token(login)
        user_id = len(cls.users) + 1
        new_user = User(user_id, login, pbkdf2_sha256.hash(password))
        cls.users[login] = new_user
        return access_token

    @classmethod
    def authorize_user(cls, login: str, password: str) -> str | None:
        """Авторизация пользователя."""
        if not isinstance(login, str) or not isinstance(password, str):
            raise TypeError('String expected.')
        if not cls.is_user_exist(login):
            return None
        current_user = cls.users[login]
        if not pbkdf2_sha256.verify(password, current_user.password):
            return None
        if cls.is_token_exist(current_user.id):
            if cls.is_token_expired(current_user.access_token):
                cls.users[login].access_token = cls.create_token(login)
                cls.token_storage[current_user.id] = cls.users[login].access_token
        else:
            cls.users[login].access_token = cls.create_token(login)
            cls.token_storage[current_user.id] = cls.users[login].access_token
        return cls.users[login].access_token

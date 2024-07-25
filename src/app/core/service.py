import datetime
from dataclasses import dataclass

import jwt
from passlib.hash import pbkdf2_sha256

from app.config import EXPIRATION_TIME, SECRET  # type: ignore


@dataclass
class User:
    """Данные пользователя."""

    login: str
    password: str
    access_token: str | None = None


class AuthService:
    """Cервис авторизации."""

    users: dict = {}

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
        if login not in cls.users:
            return False
        return True

    @classmethod
    def is_token_exist(cls, login: str):
        if cls.users[login].access_token is None:
            return False
        return True

    @staticmethod
    def is_token_expired(token: str):
        try:
            jwt.decode(token, SECRET, algorithms=["HS256"])
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
        new_user = User(login, pbkdf2_sha256.hash(password))
        cls.users[login] = new_user
        return access_token

    @classmethod
    def authorize_user(cls, login: str, password: str) -> str | None:
        """Авторизация пользователя."""
        if not isinstance(login, str) or not isinstance(password, str):
            raise TypeError('String expected.')
        if not cls.is_user_exist(login):
            return None
        if not pbkdf2_sha256.verify(password, cls.users[login].password):
            return None
        if cls.is_token_exist(login):
            if cls.is_token_expired(cls.users[login].access_token):
                cls.users[login].access_token = cls.create_token(login)
        else:
            cls.users[login].access_token = cls.create_token(login)
        return cls.users[login].access_token

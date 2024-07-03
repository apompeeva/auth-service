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
        """Возвращает сгенер рованный jwt токен."""
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
    def registrate_user(cls, login: str, password: str) -> str | None:
        """Регистрация пользователя."""
        if login in cls.users:
            return None

        access_token = cls.create_token(login)
        new_user = User(login, pbkdf2_sha256.hash(password))
        cls.users[login] = new_user
        return access_token

    @classmethod
    def authorize_user(cls, login: str, password: str) -> str | None:
        """Авторизация пользователя."""
        if login not in cls.users:
            return None
        current_user = cls.users[login]
        if not pbkdf2_sha256.verify(password, current_user.password):
            return None
        if current_user.access_token is None:
            current_user.access_token = cls.create_token(login)
        else:
            current_user.access_token = cls.create_token(login)
        return current_user.access_token

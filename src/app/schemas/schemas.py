from pydantic import BaseModel


class User(BaseModel):
    """Данные для регистрации и автоизации пользователя."""

    login: str
    password: str


class AuthResponse(BaseModel):
    """Токен."""

    access_token: str

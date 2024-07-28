from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str


class UserId(BaseModel):
    user_id: int


class AuthResponse(BaseModel):
    access_token: str

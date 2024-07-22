import pytest
import datetime
from app.service import AuthService, User
import jwt
from passlib.hash import pbkdf2_sha256

from app.config import EXPIRATION_TIME, SECRET  # type: ignore


@pytest.fixture(scope='session')
def auth_service():
    auth_service = AuthService()
    user_without_token = User('user_without',
                              pbkdf2_sha256.hash('password123'))
    user_with_token = User('user_with',
                           pbkdf2_sha256.hash('password567'),
                           jwt.encode(
                               {
                                   'username': 'user_with',
                                   'exp': datetime.datetime.now(datetime.UTC)
                                   + datetime.timedelta(minutes=EXPIRATION_TIME),
                               },
                               SECRET,
                               algorithm='HS256',
                           ))
    auth_service.users.update({user_without_token.login: user_without_token,
                               user_with_token.login: user_with_token})
    return auth_service

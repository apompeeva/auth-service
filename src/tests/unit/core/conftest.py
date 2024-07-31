import datetime

import jwt
import pytest
from passlib.hash import pbkdf2_sha256

from app.config import EXPIRATION_TIME, SECRET  # type: ignore
from app.core.service import AuthService, User


@pytest.fixture(scope='session')
def auth_service():
    auth_service = AuthService()
    user_without_token = User(0, 'user_without',
                              pbkdf2_sha256.hash('password123'))
    user_with_token = User(1, 'user_with',
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
    auth_service.token_storage.update({10: jwt.encode(
        {
            'username': 'user_with',
            'exp': datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(minutes=EXPIRATION_TIME),
        },
        SECRET,
        algorithm='HS256',
    ),
        11: jwt.encode(
        {
            'username': 'user_with',
            'exp': datetime.datetime.now(datetime.UTC)
            - datetime.timedelta(minutes=EXPIRATION_TIME),
        },
        SECRET,
        algorithm='HS256',
    )})
    return auth_service

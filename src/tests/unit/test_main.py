import pytest
import jwt

from app.config import EXPIRATION_TIME, SECRET  # type: ignore


def test_create_token(auth_service):
    access_token = auth_service.create_token('login')

    assert access_token is not None
    assert jwt.decode(access_token, SECRET, algorithms=[
                      "HS256"])['username'] == 'login'


@pytest.mark.parametrize('login, password, expected', (
    pytest.param('user_without', 'password123', None, id='existed_user'),
    pytest.param(1, 'password123', None, id='failed', marks=pytest.mark.xfail(
        raises=TypeError,
    )),
    pytest.param('user_without', [], None, id='failed', marks=pytest.mark.xfail(
        raises=TypeError,
    ))
))
def test_registrate_existed_user(auth_service, login, password, expected):
    assert auth_service.registrate_user(login, password) is expected


@pytest.mark.parametrize('login, password', (
    pytest.param('user_new', '123pass123', id='new_user'),
    pytest.param('user_new1', '123pass123', id='new_user')
))
def test_registrate_new_user(auth_service, login, password):

    access_token = auth_service.registrate_user(login, password)

    assert access_token is not None
    assert jwt.decode(access_token, SECRET, algorithms=[
                      "HS256"])['username'] == login


@pytest.mark.parametrize('login, password, expected', (
    pytest.param('user_newnew', '123pass123', None, id='new_user'),
    pytest.param('user_with', '123pass123', None, id='incorrect_password'),
    pytest.param(1, 'password123', None, id='failed', marks=pytest.mark.xfail(
        raises=TypeError,
    )),
    pytest.param('user_without', [], None, id='failed', marks=pytest.mark.xfail(
        raises=TypeError,
    ))

))
def test_authorize_incorrect_user(auth_service, login, password, expected):
    assert auth_service.authorize_user(login, password) is expected


@pytest.mark.parametrize('login, password', (
    pytest.param('user_with', 'password567', id='user_with_token'),
    pytest.param('user_without', 'password123', id='user_without_token')
))
def test_authorize_correct_user(auth_service, login, password):
    access_token = auth_service.authorize_user(login, password)

    assert access_token is not None
    assert jwt.decode(access_token, SECRET, algorithms=[
                      "HS256"])['username'] == login

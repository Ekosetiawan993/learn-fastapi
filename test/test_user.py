from pytest import fixture, mark
from jose import jwt
from .database import client, session
from app import schemas
from app.config import settings

# Fixture for create user, it's ok to depend on fixture, not test


# @fixture
# def create_user(client):
#     user_data = {'email': 'cobaaja@gmail.com', 'password': 'password123'}
#     response = client.post(
#         url='/users/', json=user_data)
#     assert response.status_code == 201
#     new_user = response.json()
#     new_user['password'] = user_data['password']
#     return new_user


# @fixture
# def app_index(client):
#     # returning index page
#     return client.get('/')


def test_app_index(app_index):
    assert app_index.status_code == 200


def test_app_index_message(app_index):
    assert app_index.json() == {'msg': 'halo dunia'}


def test_create_user(client):
    email = 'contoh7@gmail.com'
    response = client.post(
        url='/users/', json={'email': email, 'password': 'password123'})

    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == email


def test_user_login(client, create_user):
    # test_user = create_user
    response = client.post(
        url='/login', data={'username': create_user['email'], 'password': create_user['password']})

    login_response = schemas.Token(**response.json())

    payload = jwt.decode(login_response.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get('user_id')

    assert id == create_user['id']
    assert login_response.token_type == 'Bearer'

    assert response.status_code == 200


@mark.parametrize('username, password, status_code', [
    ('email', 'passaja', 403),
    ('salah@gmail.com', 'password123', 403),
    ('contoh7@gmail.com', 'salah', 403),
    (None, 'password123', 422),
    ('contoh7@gmail.com', None, 422)
])
def test_failed_login(create_user, client, username, password, status_code):
    response = client.post(
        url='/login', data={'username': username, 'password': password})

    assert response.status_code == status_code
    # assert response.json().get('detail') == 'Invalid Credentials'

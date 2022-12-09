from fastapi.testclient import TestClient
from app.main import app
from pytest import fixture, mark


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app import models, schemas

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:tatapjang@localhost:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False)

# Base.metadata.create_all(bind=engine)  # make table with ORM
# Base = declarative_base()


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# fixture for reusing code

@fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # Base.metadata.drop_all(bind=engine)
    # # code to run before test / create table
    # Base.metadata.create_all(bind=engine)
    # # yiled is same as return but no direct stop
    # yield TestClient(app)
    # drop table after test


@fixture
def create_user(client):
    user_data = {'email': 'cobaaja@gmail.com', 'password': 'password123'}
    response = client.post(
        url='/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@fixture
def create_user_2(client):
    user_data = {'email': 'cobaaja222@gmail.com', 'password': 'password123'}
    response = client.post(
        url='/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@fixture
def app_index(client):
    # returning index page
    return client.get('/')


# Fixture for authenticate login
@fixture
def token(create_user):
    return create_access_token({'user_id': create_user['id']})


@fixture
def authorized_client(token, client):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }

    return client


# @fixture
# def create_post(authorized_client):
#     post_data = {'title': 'titleeee111', 'content': 'content11111'}
#     response = authorized_client.post('/posts/', json=post_data)

#     assert response.status_code == 201


@fixture
def create_posts(create_user, session, create_user_2):
    post_data = [{
        'title': 'title 1111',
        'content': 'content 1111',
        'user_id': create_user['id']
    },
        {
        'title': 'title 2222',
        'content': 'content 2222',
        'user_id': create_user['id']
    },
        {
        'title': 'title 2222',
        'content': 'content 2222',
        'user_id': create_user_2['id']
    }]

    def create_post_model(posts):
        return models.Post(**posts)

    post_map = map(create_post_model, post_data)
    post_data_all = list(post_map)

    session.add_all(post_data_all)

    session.commit()

    posts = session.query(models.Post).all()
    return posts


@fixture
def create_posts_special_id(create_user_2, session):
    post_data = [{
        'title': 'title 1111',
        'content': 'content 1111',
        'user_id': create_user_2['id']
    },
        {
        'title': 'title 2222',
        'content': 'content 2222',
        'user_id': create_user_2['id']
    },
        {
        'title': 'title 2222',
        'content': 'content 2222',
        'user_id': create_user_2['id']
    }]

    def create_post_model(posts):
        return models.Post(**posts)

    post_map = map(create_post_model, post_data)
    post_data_all = list(post_map)

    session.add_all(post_data_all)

    session.commit()

    posts = session.query(models.Post).all()
    return posts

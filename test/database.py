from fastapi.testclient import TestClient
from app.main import app
from pytest import fixture


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base, get_db

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

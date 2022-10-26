
from fastapi import FastAPI, Depends
from fastapi.params import Body


from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# this for make a new table a.k.a migrations, command to generate the table without alembic
# models.Base.metadata.create_all(bind=engine)

# schema, we make a custom schema about what should the input data look like
app = FastAPI()

# CORS
# origins = [
#     'https://www.google.com',
#     'https://www.bing.com',
#     'https://www.duckduckgo.com'
# ]

# if api is public, every domain can access
origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# make schema for post


# Make a connection (had a failed potential)
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password='tatapjang',
#             cursor_factory=RealDictCursor       # for retrieving the table's column name
#         )
#         cursor = conn.cursor()
#         print('Database connect is successful')
#         break
#     except Exception as error:
#         print(f'fails to making a connection \nError: {error}')
#         print('Will reconnect in 5 second')
#         time.sleep(10)


@app.get("/")
def index():
    return "Hello fastapi, dari eko, 1234"


# Grab the router from routers folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# @app.get("/login")
# def login():
#     return 'Login oiiii111'

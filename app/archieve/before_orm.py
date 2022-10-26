from turtle import st
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models
from ..database import engine, SessionLocal, get_db

# this for make a new table a.k.a migrations
models.Base.metadata.create_all(bind=engine)

# schema, we make a custom schema about what should the input data look like
app = FastAPI()


# make schema for post


class Post(BaseModel):
    # number: int
    title: str
    content: str
    published: bool = True  # Optional property with default value = True
    rating: Optional[int] = None  # Optional with none value


# Make a connection (had a failed potential)
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='tatapjang',
            cursor_factory=RealDictCursor       # for retrieving the table's column name
        )
        cursor = conn.cursor()
        print('Database connect is successful')
        break
    except Exception as error:
        print(f'fails to making a connection \nError: {error}')
        print('Will reconnect in 5 second')
        time.sleep(10)


my_posts = [{'title': 'title no. 1', 'content': 'content no. 1', 'id': 1},
            {'title': 'favorit food', 'content': 'bakmi', 'id': 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id):
    for post_index, post in enumerate(my_posts):
        if post['id'] == id:
            return post_index


@app.get("/")
def index():
    return "Hello fastapi, dari eko, 1234"


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {'status': 'success'}


@app.get("/login")
def login():
    return 'Login oiiii111'


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()  # commiting changes to database
    # do it this way to prevent sql injection

    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    return {'data': new_post}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):  # convert id to integer
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    # post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail ': f'post with id: {id} was not found'}

    return {'data': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)),)
    deleted_post = cursor.fetchone()
    conn.commit()
    # post_idx = find_post_index(id)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'there is no post with id {id}')

    # my_posts.pop(post_idx)
    return {'detail': f'post with id {id} deleted'}


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    # print(post)
    # post_idx = find_post_index(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)),)

    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'there is no post with id {id}')

    # update_posting = post.dict()
    # update_posting['id'] = id

    # my_posts[post_idx] = update_posting

    return {'data': updated_post}


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {'new_post': f"title {payload['title']}, content : {payload['content']}"}

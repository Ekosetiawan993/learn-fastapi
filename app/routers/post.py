
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
)

# special case, model in list


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(limit)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by('Votes').filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostContent)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()  # commiting changes to database
    # # do it this way to prevent sql injection

    # # post_dict = post.dict()
    # # post_dict['id'] = randrange(0, 1000000)
    # # my_posts.append(post_dict)

    # models.Post(title=post.title, content=post.content, published=post.published) # this is hard coded

    new_post = models.Post(user_id=current_user.id, **
                           post.dict())  # unpack the dictionary

    db.add(new_post)
    db.commit()
    # fetch the new added post and put it on bew_post variable
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # convert id to integer
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by('Votes').filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail ': f'post with id: {id} was not found'}

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)),)
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # post_idx = find_post_index(id)
    post_query = db.query(models.Post).filter(
        models.Post.id == id)  # this just the raw query
    post = post_query.first()

    if post == None:  # run the query
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'there is no post with id {id}')

    if post.user_id != current_user.id:  # check if the current login user is the post owner
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'this post with id : {id} is not yourss!')
    print(post_query.first().user_id)

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(post_idx)

    return {'detail': f'post with id {id} deleted'}


@router.put('/{id}', response_model=schemas.PostContent)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post)
    # post_idx = find_post_index(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)),)

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()

    if old_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'there is no post with id {id}')

    if old_post.user_id != current_user.id:  # check the post owner
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'this post is not yourss')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    # update_posting = post.dict()
    # update_posting['id'] = id

    # my_posts[post_idx] = update_posting

    return post_query.first()

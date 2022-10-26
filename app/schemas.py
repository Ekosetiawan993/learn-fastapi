from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

# class Post(BaseModel):
#     # number: int
#     title: str
#     content: str
#     published: bool = True  # Optional property with default value = True
# rating: Optional[int] = None  # Optional with none value


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  # convert the orm model to dict
        orm_mode = True


class PostContent(PostBase):  # Pydantic model for response
    id: int  # str
    created_at: datetime
    user_id: int
    user: UserOut
    # title: str     # Inherited it form PostBase
    # content: str
    # published: bool

    class Config:  # convert the orm model to dict
        orm_mode = True


class PostVote(BaseModel):
    Post: PostContent
    Votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response for creating user


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  # convert the orm model to dict
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

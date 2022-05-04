import datetime as dt

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    base64_string: str


class User(UserBase):
    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    year: int
    average_rating: float
    count_ratings: int
    count_reviews: int


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    review: str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    movie: Movie
    user: User
    updated_at: dt.datetime

    class Config:
        orm_mode = True


class RatingBase(BaseModel):
    rating: int


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    movie: Movie
    user: User

    class Config:
        orm_mode = True

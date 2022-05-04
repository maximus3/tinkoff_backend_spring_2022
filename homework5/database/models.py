import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    id = sa.Column(
        sa.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = sa.Column(
        sa.DateTime, nullable=False, default=dt.datetime.now
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=dt.datetime.now,
        onupdate=dt.datetime.now,
    )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'


class User(BaseModel):
    __tablename__ = 'users'

    username = sa.Column(sa.String(), nullable=False, unique=True)
    base64_string = sa.Column(sa.String(), nullable=False)


class Movie(BaseModel):
    __tablename__ = 'movies'

    title = sa.Column(sa.String)
    year = sa.Column(sa.Integer)
    average_rating = sa.Column(sa.Float, default=0.0)
    count_ratings = sa.Column(sa.Integer, default=0)
    count_reviews = sa.Column(sa.Integer, default=0)


class Review(BaseModel):
    __tablename__ = 'reviews'

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    movie_id = sa.Column(
        sa.Integer, sa.ForeignKey('movies.id'), nullable=False
    )
    review = sa.Column(sa.String)

    user = sa.orm.relationship('User', backref='reviews')
    movie = sa.orm.relationship('Movie', backref='reviews')


class Rating(BaseModel):
    __tablename__ = 'ratings'

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    movie_id = sa.Column(
        sa.Integer, sa.ForeignKey('movies.id'), nullable=False
    )
    rating = sa.Column(sa.Integer)

    user = sa.orm.relationship('User', backref='ratings')
    movie = sa.orm.relationship('Movie', backref='ratings')

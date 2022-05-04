from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session as SessionType

from . import create_session
from .models import BaseModel, Movie, Rating, Review, User
from .schemas import BaseModel as SchemaBaseModel
from .schemas import Movie as SchemaMovie
from .schemas import Rating as SchemaRating
from .schemas import Review as SchemaReview
from .schemas import User as SchemaUser

BaseProxyType = TypeVar('BaseProxyType', bound='BaseProxy')
MovieProxyType = TypeVar('MovieProxyType', bound='MovieProxy')
ReviewProxyType = TypeVar('ReviewProxyType', bound='ReviewProxy')


class BaseProxy:
    BASE_MODEL: Type[BaseModel] = BaseModel
    SCHEMA_MODEL: Type[SchemaBaseModel] = SchemaBaseModel

    def __init__(self, model: BaseModel):
        self.id = model.id

    def __eq__(self: BaseProxyType, other: object) -> bool:
        if not isinstance(other, BaseProxy):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'

    @classmethod
    def get(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return cls.get(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one_or_none()
        if model:
            return cls(model)
        return None

    @classmethod
    def get_expect(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseProxyType:
        if session is None:
            with create_session() as new_session:
                return cls.get_expect(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls(model)

    @classmethod
    def get_model(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseModel:
        if session is None:
            with create_session() as new_session:
                return cls.get_model(new_session, **kwargs)
        return session.query(cls.BASE_MODEL).filter_by(**kwargs).one()

    @classmethod
    def get_schema_model(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> SchemaBaseModel:
        if session is None:
            with create_session() as new_session:
                return cls.get_schema_model(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls.SCHEMA_MODEL.from_orm(model)

    @classmethod
    def get_all(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> list[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return cls.get_all(new_session, **kwargs)
        data = []
        for model in session.query(cls.BASE_MODEL).filter_by(**kwargs).all():
            data.append(cls(model))
        return data

    @classmethod
    def create(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            with create_session() as new_session:
                return cls.create(new_session, **kwargs)
        model = cls.BASE_MODEL(**kwargs)
        session.add(model)
        return True

    def update(
        self: BaseProxyType,
        session: SessionType = None,
        **kwargs: Any,
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return self.update(new_session, **kwargs)
        model = (
            session.query(self.BASE_MODEL).filter_by(id=self.id).one_or_none()
        )
        if model is None:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key) and hasattr(self, key):
                setattr(model, key, value)
                setattr(self, key, value)
            else:
                return None
        session.add(model)
        return self


class UserProxy(BaseProxy):
    BASE_MODEL = User
    SCHEMA_MODEL = SchemaUser

    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.username = user.username
        self.base64_string = user.base64_string


class MovieProxy(BaseProxy):
    BASE_MODEL = Movie
    SCHEMA_MODEL = SchemaMovie
    PAGE_SIZE = 5

    def __init__(self, movie: Movie) -> None:
        super().__init__(movie)
        self.title = movie.title
        self.year = movie.year
        self.average_rating = movie.average_rating
        self.count_ratings = movie.count_ratings
        self.count_reviews = movie.count_reviews

    @classmethod
    def filter(
        cls: Type[MovieProxyType],
        page: int = 1,
        per_page: int = 5,
        **kwargs: Any,
    ) -> list[MovieProxyType]:
        with create_session() as session:
            filters = []
            if 'title' in kwargs and kwargs['title'] is not None:
                filters.append(Movie.title.like(f'%{kwargs["title"]}%'))
            if 'year' in kwargs and kwargs['year'] is not None:
                filters.append(Movie.year == kwargs['year'])
            query = (
                session.query(cls.BASE_MODEL)
                .filter(*filters)
                .order_by(Movie.average_rating.desc())
            )
            offset = (page - 1) * per_page
            query = query.offset(offset)
            query = query.limit(per_page)
            if 'top' in kwargs and kwargs['top'] is not None:
                query = query.limit(
                    min(max(kwargs['top'] - offset, 0), per_page)
                )
            data = []
            for model in query.all():
                data.append(cls(model))
            return data


class ReviewProxy(BaseProxy):
    BASE_MODEL = Review
    SCHEMA_MODEL = SchemaReview
    PAGE_SIZE = 5

    def __init__(self, review: Review) -> None:
        super().__init__(review)
        self.user = UserProxy(review.user)
        self.movie = MovieProxy(review.movie)
        self.review = review.review
        self.user_id = review.user_id
        self.movie_id = review.movie_id
        self.updated_at = review.updated_at

    @classmethod
    def filter(
        cls: Type[ReviewProxyType],
        page: int = 1,
        per_page: int = 5,
        **kwargs: Any,
    ) -> list[ReviewProxyType]:
        with create_session() as session:
            filters = []
            if 'movie_id' in kwargs and kwargs['movie_id'] is not None:
                filters.append(Review.movie_id == kwargs['movie_id'])
            query = (
                session.query(cls.BASE_MODEL)
                .filter(*filters)
                .order_by(Review.updated_at.desc())
            )
            query = query.offset((page - 1) * per_page)
            query = query.limit(per_page)
            data = []
            for model in query.all():
                data.append(cls(model))
            return data


class RatingProxy(BaseProxy):
    BASE_MODEL = Rating
    SCHEMA_MODEL = SchemaRating

    def __init__(self, rating: Rating) -> None:
        super().__init__(rating)
        self.user = UserProxy(rating.user)
        self.movie = MovieProxy(rating.movie)
        self.rating = rating.rating
        self.user_id = rating.user_id
        self.movie_id = rating.movie_id

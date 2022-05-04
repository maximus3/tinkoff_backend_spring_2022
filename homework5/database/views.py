from typing import Optional, Type, Union

from sqlalchemy.orm import Session as SessionType

from database.schemas import RatingBase, ReviewBase

from . import create_session
from .proxy import MovieProxy, RatingProxy, ReviewProxy, UserProxy
from .status import Status, StatusException


def _update_or_create(
    session: SessionType,
    proxy_class: Union[Type[RatingProxy], Type[ReviewProxy]],
    user_id: int,
    movie_id: int,
    data: Union[RatingBase, ReviewBase],
) -> tuple[Status, Union[RatingProxy, ReviewProxy, None]]:
    if isinstance(data, RatingBase):
        if data.rating < 0 or data.rating > 10:
            return Status.WRONG_RATING, None

    movie = MovieProxy.get(session=session, id=movie_id)
    if movie is None:
        return Status.MOVIE_NOT_FOUND, None

    proxy_instance = proxy_class.get(
        session=session, user_id=user_id, movie_id=movie_id
    )
    is_create = False
    if proxy_instance:
        if isinstance(proxy_instance, RatingProxy):
            was_rating = proxy_instance.rating
        proxy_instance = proxy_instance.update(**data.dict())
    else:
        proxy_class.create(
            session=session,
            user_id=user_id,
            movie_id=movie_id,
            user=UserProxy.get_model(session=session, id=user_id),
            movie=MovieProxy.get_model(session=session, id=movie_id),
            **data.dict(),
        )
        proxy_instance = proxy_class.get(
            session=session, user_id=user_id, movie_id=movie_id
        )
        is_create = True
    if proxy_instance is None:
        return Status.INSTANCE_CREATE_FAILED, None

    if isinstance(proxy_instance, ReviewProxy):
        movie = movie.update(
            count_reviews=movie.count_reviews
            + (is_create if proxy_instance.review else 0)
        )
    else:
        if is_create:
            movie = movie.update(
                average_rating=(
                    movie.average_rating * movie.count_ratings
                    + proxy_instance.rating
                )
                / (movie.count_ratings + 1),
                count_ratings=movie.count_ratings + 1,
            )
        else:
            movie = movie.update(
                average_rating=(
                    movie.average_rating * movie.count_ratings
                    - was_rating
                    + proxy_instance.rating
                )
                / (movie.count_ratings)
            )

    if movie is None:
        return Status.MOVIE_UPDATE_FAILED, None

    return Status.OK, proxy_instance


def update_or_create(
    user_id: int,
    movie_id: int,
    proxy_class: Union[Type[RatingProxy], Type[ReviewProxy]],
    data: Union[RatingBase, ReviewBase],
) -> tuple[Status, Union[RatingProxy, ReviewProxy, None]]:
    try:
        with create_session() as session:
            status, return_data = _update_or_create(
                session, proxy_class, user_id, movie_id, data
            )
            if status:
                raise StatusException(status)
            return status, return_data
    except StatusException as exc:
        return exc.status, None


def update_or_create_review(
    user_id: int, movie_id: int, data: ReviewBase
) -> tuple[Status, Optional[ReviewProxy]]:
    status, result = update_or_create(user_id, movie_id, ReviewProxy, data)
    if not isinstance(result, ReviewProxy):
        return status, None
    return status, result


def update_or_create_rating(
    user_id: int, movie_id: int, data: RatingBase
) -> tuple[Status, Optional[RatingProxy]]:
    status, result = update_or_create(user_id, movie_id, RatingProxy, data)
    if not isinstance(result, RatingProxy):
        return status, None
    return status, result

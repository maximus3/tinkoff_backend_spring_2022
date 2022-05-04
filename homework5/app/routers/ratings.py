from fastapi import APIRouter, Depends, HTTPException

from database.proxy import RatingProxy, UserProxy
from database.schemas import Rating as RatingSchema
from database.schemas import RatingBase
from database.status import Status
from database.views import update_or_create_rating

from ..utils.auth import get_current_user

router = APIRouter(
    prefix='/ratings',
    tags=['ratings'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/{movie_id}', response_model=RatingSchema)
def add_rating(
    movie_id: int,
    data: RatingBase,
    user: UserProxy = Depends(get_current_user),
) -> RatingProxy:
    status, rating = update_or_create_rating(
        user_id=user.id, movie_id=movie_id, data=data
    )
    if status or rating is None:
        if status == Status.MOVIE_NOT_FOUND:
            raise HTTPException(status_code=404, detail='Movie not found')
        if status == Status.WRONG_RATING:
            raise HTTPException(
                status_code=422, detail='Wrong rating parameter'
            )
        raise HTTPException(status_code=500, detail='Something was wrong')
    return rating

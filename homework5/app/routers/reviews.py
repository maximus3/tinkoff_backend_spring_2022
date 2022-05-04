from fastapi import APIRouter, Depends, HTTPException

from database.proxy import ReviewProxy, UserProxy
from database.schemas import Review as ReviewSchema
from database.schemas import ReviewBase
from database.status import Status
from database.views import update_or_create_review

from ..utils.auth import get_current_user

router = APIRouter(
    prefix='/reviews',
    tags=['reviews'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/{movie_id}', response_model=list[ReviewSchema])
def get_reviews(
    movie_id: int, page: int = 1, per_page: int = 10
) -> list[ReviewProxy]:
    reviews: list[ReviewProxy] = ReviewProxy.filter(
        movie_id=movie_id, page=page, per_page=per_page
    )
    return reviews


@router.post('/{movie_id}', response_model=ReviewSchema)
def add_review(
    movie_id: int,
    data: ReviewBase,
    user: UserProxy = Depends(get_current_user),
) -> ReviewProxy:
    status, review = update_or_create_review(
        user_id=user.id, movie_id=movie_id, data=data
    )
    if status or review is None:
        if status == Status.MOVIE_NOT_FOUND:
            raise HTTPException(status_code=404, detail='Movie not found')
        raise HTTPException(status_code=500, detail='Something was wrong')

    return review

from typing import Optional

from fastapi import APIRouter, HTTPException

from database.proxy import MovieProxy
from database.schemas import Movie as MovieSchema

router = APIRouter(
    prefix='/movies',
    tags=['movies'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[MovieSchema])
def get_movies(
    title: Optional[str] = None,
    year: Optional[int] = None,
    top: Optional[int] = None,
    page: int = 1,
    per_page: int = 5,
) -> list[MovieProxy]:
    return MovieProxy.filter(
        title=title, year=year, top=top, page=page, per_page=per_page
    )


@router.get('/{movie_id}', response_model=MovieSchema)
def get_movie_by_id(movie_id: int) -> MovieProxy:
    movie = MovieProxy.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail='Not found')
    return movie

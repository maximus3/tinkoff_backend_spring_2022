from fastapi import APIRouter, Depends

from database.proxy import UserProxy
from database.schemas import User as UserSchema

from ..utils.auth import get_current_user, register_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/', response_model=UserSchema)
def create_user(user: UserProxy = Depends(register_user)) -> UserProxy:
    return user


@router.get('/', response_model=UserSchema)
def get_user(user: UserProxy = Depends(get_current_user)) -> UserProxy:
    return user

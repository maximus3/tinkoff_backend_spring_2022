from fastapi import APIRouter

from app.schema import User as UserSchema
from app.schema import UserBase as UserBaseSchema
from app.user import User

router = APIRouter(
    prefix='/login',
    tags=['login'],
    responses={404: {'description': 'Not found'}},
)


@router.post('', response_model=UserSchema, status_code=201)
async def register_user(username: UserBaseSchema) -> UserSchema:
    user = await User.register(username.username)
    return UserSchema(username=user.username, id=user.user_id)

import base64
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database.proxy import UserProxy

security = HTTPBasic()


def base64_to_password(base64_string: str) -> str:
    try:
        _, password = base64.b64decode(base64_string).decode().split(':')
    except ValueError:
        return ''
    return password


def make_base64_string(username: str, password: str) -> str:
    return base64.b64encode(f'{username}:{password}'.encode()).decode()


def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> UserProxy:
    user = UserProxy.get(username=credentials.username)
    if user:
        correct_password = secrets.compare_digest(
            credentials.password, base64_to_password(user.base64_string)
        )
        if correct_password:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Basic'},
    )


def register_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> UserProxy:
    user = UserProxy.get(username=credentials.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists',
            headers={'WWW-Authenticate': 'Basic'},
        )
    UserProxy.create(
        username=credentials.username,
        base64_string=make_base64_string(
            credentials.username, credentials.password
        ),
    )
    user = UserProxy.get(username=credentials.username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Create new user failed',
        headers={'WWW-Authenticate': 'Basic'},
    )

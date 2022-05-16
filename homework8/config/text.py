from pydantic import BaseModel


class TextDataClass(BaseModel):
    ALREADY_LOGGED: str = 'You have already logged in'
    SMTH_ERROR: str = 'Something was wrong'
    LOGIN_REQU: str = 'Please log in to access this page.'
    LOGIN_FAILED: str = 'Please check your login details and try again.'
    USER_EXISTS: str = 'User with this login already exists'


TextData = TextDataClass()

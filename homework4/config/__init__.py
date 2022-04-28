from pathlib import Path
from typing import Optional

from pydantic import BaseModel, BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigData(BaseSettings):
    DATABASE_FILENAME: Optional[str] = Field(
        'data.db', env='DATABASE_FILENAME'
    )
    DATABASE_ENGINE: str = Field('sqlite:///data.db', env='DATABASE_ENGINE')
    money_name: str = Field('money', env='money_name')
    default_money: str = Field('1000.0', env='default_money')
    default_curs: list[str] = Field(
        ['rtc', 'uth', 'zrp', 'cate', 'zlm'], env='default_curs'
    )

    class Config:
        env_file: Path = BASE_DIR / '.env'


class TextDataClass(BaseModel):
    ALREADY_LOGGED: str = 'You have already logged in'
    SMTH_ERROR: str = 'Something was wrong'
    LOGIN_REQU: str = 'Login required'
    GET_MONEY_ERROR: str = 'Something was wrong with balance'
    COUNT_NOT_NUM: str = 'count is not num'
    OPERATION_OK: str = 'Operation OK'
    RATE_UPDATED: str = 'Rate updated, try again'
    NO_ENOUGH_MONEY: str = 'You don\'t have enough value'


cfg = ConfigData()
TextData = TextDataClass()

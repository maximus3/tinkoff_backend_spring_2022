from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigData(BaseSettings):
    DATABASE_ENGINE: str = Field('sqlite:///data.db', env='DATABASE_ENGINE')
    DATABASE_NAME: str = Field('data.db', env='DATABASE_NAME')

    class Config:
        env_file: Path = BASE_DIR / '.env'


cfg = ConfigData()

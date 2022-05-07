from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigData(BaseSettings):
    REDIS_URL = 'redis://localhost:6379'
    MAIN_CHANNEL_NAME = 'main'
    DEBUG = True

    class Config:
        env_file: Path = BASE_DIR / '.env'


cfg = ConfigData()

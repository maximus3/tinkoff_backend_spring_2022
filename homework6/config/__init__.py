import logging
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
logging.basicConfig(level=logging.INFO)


class ConfigData(BaseSettings):
    allowed_sizes = ['original', '32', '64']
    REDIS_URL = 'redis://localhost:6379'


cfg = ConfigData()

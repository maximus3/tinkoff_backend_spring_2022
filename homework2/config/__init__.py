from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigDataClass(BaseSettings):
    SITE: str = Field(None, env='SITE')

    class Config:
        env_file: Path = BASE_DIR / '.env'


class TextDataClass(BaseModel):
    WEATHER_TEXT: str = 'Current weather in {}: {}'
    ERROR_404: str = 'City {} not found.'
    ERROR: str = 'Something was wrong with connection. Try again later.'
    STATUS_NOT_FOUND: str = 'Something was wrong. Try again later.'
    PARSE_ERROR: str = 'Something was wrong with page. Try again later.'


TextData = TextDataClass()
ConfigData = ConfigDataClass()

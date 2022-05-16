import logging
from pathlib import Path

from pydantic import BaseSettings, Field

logging_format = (
    '%(filename)s %(funcName)s [LINE:%(lineno)d]# '
    '%(levelname)-8s [%(asctime)s] %(name)s: %(message)s'
)

logging.basicConfig(
    format=logging_format,
    level=logging.INFO,
    filename='app.log',
)

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigData(BaseSettings):
    DATABASE_ENGINE: str = Field('sqlite:///data.db', env='DATABASE_ENGINE')
    DATABASE_NAME: str = Field('data.db', env='DATABASE_NAME')
    REDIS_URL: str = Field('redis://localhost:6379', env='REDIS_URL')
    debug: bool = Field(True, env='DEBUG')
    contests_dir: Path = Field(BASE_DIR / 'data/contests', env='CONTESTS_DIR')
    problems_dir: Path = Field(BASE_DIR / 'data/problems', env='PROBLEMS_DIR')
    checker_dir: Path = Field(BASE_DIR / 'data/checker', env='CHECKER_DIR')

    input_name: str = Field('input.txt', env='INPUT_NAME')
    output_name: str = Field('output.txt', env='OUTPUT_NAME')
    solution_name_templ: str = Field('solution_{}.py', env='SOLUTION_NAME')

    class Config:
        env_file: Path = BASE_DIR / '.env'


cfg = ConfigData()
cfg.contests_dir.mkdir(parents=True, exist_ok=True)
cfg.problems_dir.mkdir(parents=True, exist_ok=True)
cfg.checker_dir.mkdir(parents=True, exist_ok=True)

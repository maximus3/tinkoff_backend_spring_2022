import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from config import BASE_DIR
from database.models import Base

from . import tmp_database_engine, tmp_database_name

engine = sa.create_engine(tmp_database_engine)
Session = scoped_session(sessionmaker(bind=engine))


def prepare_db():
    Base.metadata.create_all(engine)


def remove_db():
    if (BASE_DIR / tmp_database_name).exists():
        (BASE_DIR / tmp_database_name).unlink()

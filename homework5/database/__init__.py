from contextlib import contextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import scoped_session, sessionmaker

from config import BASE_DIR, cfg
from config.movies_data import movie_data
from database.models import Base, Movie

engine = sa.create_engine(cfg.DATABASE_ENGINE)
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def create_session(**kwargs: Any) -> SessionType:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


def create_all() -> None:
    if not (BASE_DIR / cfg.DATABASE_NAME).exists():
        Base.metadata.create_all(engine)

        with create_session() as session:
            for title, year in movie_data:
                session.add(Movie(title=title, year=year))

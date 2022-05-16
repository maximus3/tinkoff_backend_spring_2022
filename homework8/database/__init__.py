from contextlib import contextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import scoped_session, sessionmaker

from config.config import BASE_DIR, cfg
from database.models import Base

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


def create_all() -> bool:
    if not (BASE_DIR / cfg.DATABASE_NAME).exists():
        Base.metadata.create_all(engine)
        return True
    return False

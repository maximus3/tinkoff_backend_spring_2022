from contextlib import contextmanager
from typing import Any
import datetime as dt
import os

import sqlalchemy as sa
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import sessionmaker

from . import tmp_database_name
from config import cfg, BASE_DIR
from database.models import Base, Currency

engine = sa.create_engine('sqlite:///' + tmp_database_name)
Session = sessionmaker(bind=engine)


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


def prepare_db():
    Base.metadata.create_all(engine)
    with create_session() as session:
        created_at = dt.datetime.now()
        session.add(
            Currency(
                created_at=created_at,
                updated_at=created_at,
                name=cfg.money_name,
            )
        )

        for name in cfg.default_curs:
            session.add(
                Currency(
                    created_at=created_at,
                    updated_at=created_at,
                    name=name,
                    rate='100.0',
                )
            )


def remove_db():
    if (BASE_DIR / tmp_database_name).exists():
        os.remove(BASE_DIR / tmp_database_name)

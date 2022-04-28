import datetime as dt
from contextlib import contextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import sessionmaker

from config import BASE_DIR, cfg

from .models import Base, Currency

engine = sa.create_engine(cfg.DATABASE_ENGINE)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


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


if cfg.DATABASE_FILENAME and not (BASE_DIR / cfg.DATABASE_FILENAME).exists():
    # Create default currencies
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

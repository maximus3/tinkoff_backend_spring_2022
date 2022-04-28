import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    id = sa.Column(
        sa.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = sa.Column(sa.TIMESTAMP, nullable=False)
    updated_at = sa.Column(sa.TIMESTAMP, nullable=False)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'


class Currency(BaseModel):
    __tablename__ = 'currency'

    name = sa.Column(sa.String(), unique=True)
    rate = sa.Column(sa.String())


class User(BaseModel):
    __tablename__ = 'user'

    login = sa.Column(sa.String(), unique=True)


class UserCurrency(BaseModel):
    __tablename__ = 'user_currency'

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    currency_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('currency.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    count = sa.Column(sa.String())


class Operation(BaseModel):
    __tablename__ = 'operation'

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )
    currency_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('currency.id', ondelete='CASCADE'),
        nullable=False,
    )
    type = sa.Column(sa.String())
    count = sa.Column(sa.String())
    rate = sa.Column(sa.String())
    money = sa.Column(sa.String())

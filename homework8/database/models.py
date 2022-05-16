import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from database.problem_status import ProblemStatus

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
    created_at = sa.Column(
        sa.DateTime, nullable=False, default=dt.datetime.now
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=dt.datetime.now,
        onupdate=dt.datetime.now,
    )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'


class User(BaseModel):
    __tablename__ = 'user'

    username = sa.Column(sa.String)
    password = sa.Column(sa.String)


class Contest(BaseModel):
    __tablename__ = 'contest'

    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    path = sa.Column(sa.String, default='')


class Problem(BaseModel):
    __tablename__ = 'problem'

    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    input = sa.Column(sa.String)
    output = sa.Column(sa.String)
    path = sa.Column(sa.String, default='')


class TestCase(BaseModel):
    __tablename__ = 'testcase'

    problem_id = sa.Column(sa.Integer, sa.ForeignKey('problem.id'))
    path = sa.Column(sa.String, default='')

    problem = sa.orm.relationship('Problem')


class ContestProblem(BaseModel):
    __tablename__ = 'contest_problem'

    contest_id = sa.Column(sa.Integer, sa.ForeignKey('contest.id'))
    problem_id = sa.Column(sa.Integer, sa.ForeignKey('problem.id'))
    order = sa.Column(sa.Integer)

    contest = sa.orm.relationship('Contest')
    problem = sa.orm.relationship('Problem')


class UserContest(BaseModel):
    __tablename__ = 'user_contest'

    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    contest_id = sa.Column(sa.Integer, sa.ForeignKey('contest.id'))
    score = sa.Column(sa.Integer, default=0)

    user = sa.orm.relationship('User')
    contest = sa.orm.relationship('Contest')


class UserContestProblem(BaseModel):
    __tablename__ = 'user_contest_problem'

    user_contest_id = sa.Column(sa.Integer, sa.ForeignKey('user_contest.id'))
    contest_problem_id = sa.Column(
        sa.Integer, sa.ForeignKey('contest_problem.id')
    )
    problem_id = sa.Column(sa.Integer, sa.ForeignKey('problem.id'))
    status = sa.Column(sa.String, default=ProblemStatus.WAITING)
    score = sa.Column(sa.Integer, default=0)

    user_contest = sa.orm.relationship('UserContest')
    contest_problem = sa.orm.relationship('ContestProblem')
    problem = sa.orm.relationship('Problem')


class UserContestProblemSolution(BaseModel):
    __tablename__ = 'user_contest_problem_solution'

    user_contest_problem_id = sa.Column(
        sa.Integer, sa.ForeignKey('user_contest_problem.id')
    )
    status = sa.Column(sa.String, default=ProblemStatus.WAITING)
    score = sa.Column(sa.Integer, default=0)
    path = sa.Column(sa.String, default='')

    user_contest_problem = sa.orm.relationship('UserContestProblem')

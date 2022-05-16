import datetime as dt
from pathlib import Path
from typing import Any, Optional, Type, TypeVar, Union

from flask_login import UserMixin
from sqlalchemy.orm import Session as SessionType

from config.config import cfg
from database import create_session
from database.models import (
    BaseModel,
    Contest,
    ContestProblem,
    Problem,
    TestCase,
    User,
    UserContest,
    UserContestProblem,
    UserContestProblemSolution,
)

BaseProxyType = TypeVar('BaseProxyType', bound='BaseProxy')
BaseContestProblemProxyType = TypeVar(
    'BaseContestProblemProxyType', bound='BaseContestProblemProxy'
)
TestCaseProxyType = TypeVar('TestCaseProxyType', bound='TestCaseProxy')
UserContestProblemSolutionProxyType = TypeVar(
    'UserContestProblemSolutionProxyType',
    bound='UserContestProblemSolutionProxy',
)


class BaseProxy:
    BASE_MODEL: Type[BaseModel] = BaseModel

    def __init__(self, model: BaseModel):
        self.id = model.id

    def __eq__(self: BaseProxyType, other: object) -> bool:
        if not isinstance(other, BaseProxy):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'

    @classmethod
    def get(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return cls.get(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one_or_none()
        if model:
            return cls(model)
        return None

    @classmethod
    def get_expect(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseProxyType:
        if session is None:
            with create_session() as new_session:
                return cls.get_expect(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls(model)

    @classmethod
    def get_model(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseModel:
        if session is None:
            with create_session() as new_session:
                return cls.get_model(new_session, **kwargs)
        return session.query(cls.BASE_MODEL).filter_by(**kwargs).one()

    @classmethod
    def get_all(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> list[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return cls.get_all(new_session, **kwargs)
        data = []
        for model in session.query(cls.BASE_MODEL).filter_by(**kwargs).all():
            data.append(cls(model))
        return data

    @classmethod
    def create(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            with create_session() as new_session:
                return cls.create(new_session, **kwargs)
        model = cls.BASE_MODEL(**kwargs)
        session.add(model)
        return True

    def update(
        self: BaseProxyType,
        session: SessionType = None,
        **kwargs: Any,
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return self.update(new_session, **kwargs)
        model = (
            session.query(self.BASE_MODEL).filter_by(id=self.id).one_or_none()
        )
        if model is None:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key) and hasattr(self, key):
                setattr(model, key, value)
                setattr(self, key, value)
            else:
                return None
        session.add(model)
        return self


class UserProxy(BaseProxy, UserMixin):
    BASE_MODEL = User

    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.username = user.username
        self.password = user.password
        self.active = True


class BaseContestProblemProxy(BaseProxy):
    DIR_PATH: Path = Path()

    def __init__(self, model: Union[Contest, Problem]) -> None:
        super().__init__(model)
        self.name = model.name
        self.description = model.description
        self.path = Path(model.path)

    @classmethod
    def create(
        cls: Type[BaseContestProblemProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is not None:
            return False
        with create_session() as new_session:
            if not super().create(new_session, **kwargs):
                return False
        with create_session() as new_session:
            model = cls.get(new_session, **kwargs)
            if model is None:
                return False
            dir_name = cls.DIR_PATH / f'{model.id}'
            dir_name.mkdir(parents=True)
            model.update(new_session, path=str(dir_name.absolute()))
            return True


class ContestProxy(BaseContestProblemProxy):
    BASE_MODEL = Contest
    DIR_PATH = cfg.contests_dir

    def __init__(self, contest: Contest) -> None:
        super().__init__(contest)


class ProblemProxy(BaseContestProblemProxy):
    BASE_MODEL = Problem
    DIR_PATH = cfg.problems_dir

    def __init__(self, problem: Problem) -> None:
        super().__init__(problem)
        self.input = problem.input
        self.output = problem.output


class TestCaseProxy(BaseProxy):
    BASE_MODEL = TestCase

    def __init__(self, test_case: TestCase) -> None:
        super().__init__(test_case)
        self.problem_id = test_case.problem_id
        self.path = Path(test_case.path)

        self.problem = ProblemProxy(test_case.problem)

    @classmethod
    def create(
        cls: Type[TestCaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is not None:
            return False
        input_data, output_data = kwargs.pop('input'), kwargs.pop('output')
        kwargs['created_at'] = dt.datetime.now()
        with create_session() as new_session:
            if not super().create(session=new_session, **kwargs):
                return False
        with create_session() as new_session:
            kwargs['path'] = ''
            test_case = cls.get(new_session, **kwargs)
            if test_case is None:
                return False
            dir_name = test_case.problem.path / f'{test_case.id}'
            dir_name.mkdir(parents=True)
            test_case.update(new_session, path=str(dir_name.absolute()))
            with open(dir_name / cfg.input_name, 'w', encoding='utf-8') as f:
                f.write(input_data)
            with open(dir_name / cfg.output_name, 'w', encoding='utf-8') as f:
                f.write(output_data)
            return True


class ContestProblemProxy(BaseProxy):
    BASE_MODEL = ContestProblem

    def __init__(self, contest_problem: ContestProblem) -> None:
        super().__init__(contest_problem)
        self.contest_id = contest_problem.contest_id
        self.problem_id = contest_problem.problem_id
        self.order = contest_problem.order

        self.contest = ContestProxy(contest_problem.contest)
        self.problem = ProblemProxy(contest_problem.problem)


class UserContestProxy(BaseProxy):
    BASE_MODEL = UserContest

    def __init__(self, user_contest: UserContest) -> None:
        super().__init__(user_contest)
        self.user_id = user_contest.user_id
        self.contest_id = user_contest.contest_id
        self.score = user_contest.score

        self.user = UserProxy(user_contest.user)
        self.contest = ContestProxy(user_contest.contest)


class UserContestProblemProxy(BaseProxy):
    BASE_MODEL = UserContestProblem

    def __init__(self, user_contest_problem: UserContestProblem) -> None:
        super().__init__(user_contest_problem)
        self.user_contest_id = user_contest_problem.user_contest_id
        self.contest_problem_id = user_contest_problem.contest_problem_id
        self.problem_id = user_contest_problem.problem_id
        self.status = user_contest_problem.status
        self.score = user_contest_problem.score

        self.user_contest = UserContestProxy(user_contest_problem.user_contest)
        self.contest_problem = ContestProblemProxy(
            user_contest_problem.contest_problem
        )
        self.problem = ProblemProxy(user_contest_problem.problem)


class UserContestProblemSolutionProxy(BaseProxy):
    BASE_MODEL = UserContestProblemSolution

    def __init__(
        self, user_contest_problem_solution: UserContestProblemSolution
    ) -> None:
        super().__init__(user_contest_problem_solution)
        self.user_contest_problem_id = (
            user_contest_problem_solution.user_contest_problem_id
        )
        self.status = user_contest_problem_solution.status
        self.score = user_contest_problem_solution.score
        self.path = Path(user_contest_problem_solution.path)

        self.user_contest_problem = UserContestProblemProxy(
            user_contest_problem_solution.user_contest_problem
        )

    @classmethod
    def create(
        cls: Type[UserContestProblemSolutionProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is not None:
            return False
        code = kwargs.pop('code')
        with create_session() as new_session:
            if not super().create(session=new_session, **kwargs):
                return False
        with create_session() as new_session:
            ucp_solution = cls.get(new_session, **kwargs)
            if ucp_solution is None:
                return False
            dir_name = (
                cfg.contests_dir
                / f'{ucp_solution.user_contest_problem.user_contest.contest.id}'
                f'/{ucp_solution.user_contest_problem.user_contest.user.id}'
                f'/{ucp_solution.user_contest_problem.problem.id}'
            )
            dir_name.mkdir(parents=True, exist_ok=True)
            filename = dir_name / cfg.solution_name_templ.format(
                ucp_solution.id
            )
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            ucp_solution.update(new_session, path=str(filename.absolute()))
            return True

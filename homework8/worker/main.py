import logging
import os
import pathlib
import shutil
import subprocess
from typing import Any

import rq
import rq.timeouts

from config.config import cfg
from database.problem_status import ProblemStatus
from database.proxy import UserContestProblemSolutionProxy

logger = logging.getLogger(__name__)


def process_code(ucp_solution: UserContestProblemSolutionProxy) -> None:
    logger.info('Got %s to check', ucp_solution)

    was_status = ucp_solution.user_contest_problem.status
    was_score = ucp_solution.user_contest_problem.score

    ucp_solution.update(status=ProblemStatus.TESTING)

    was_dir = pathlib.Path().absolute()
    os.chdir(cfg.checker_dir)

    shutil.copy(ucp_solution.path, 'solution.py')

    for dir_name in ucp_solution.user_contest_problem.problem.path.iterdir():
        shutil.copy(dir_name / 'input.txt', 'input.txt')
        shutil.copy(dir_name / 'output.txt', 'output.txt')
        with open('input.txt', 'r', encoding='utf-8') as fin, open(
            'output.txt', 'r', encoding='utf-8'
        ) as fout:
            right = fout.read().strip()
            logger.info('Checking test case %s', dir_name)
            out = subprocess.check_output(['python', 'solution.py'], stdin=fin)
            if out.decode('utf-8').strip() != right:
                logger.info('WA Test case %s', dir_name)
                ucp_solution.update(status=ProblemStatus.WRONG_ANSWER)
                if was_status != ProblemStatus.OK:
                    ucp_solution.user_contest_problem.update(
                        status=ProblemStatus.WRONG_ANSWER
                    )
                break
            logger.info('OK test case %s', dir_name)
    else:
        ucp_solution.update(status=ProblemStatus.OK, score=100)
        ucp_solution.user_contest_problem.update(
            status=ProblemStatus.OK, score=100
        )
        ucp_solution.user_contest_problem.user_contest.update(
            score=ucp_solution.user_contest_problem.user_contest.score
            - was_score
            + 100
        )

    os.chdir(was_dir)


def process_code_failure(
    job: rq.job.Job, _: Any, error_type: Any, __: Any, ___: Any
) -> None:
    ucp_solution = job.args[0]

    if issubclass(error_type, rq.timeouts.JobTimeoutException):
        new_status = ProblemStatus.TIME_LIMIT
    else:
        new_status = ProblemStatus.RUNTIME_ERROR

    ucp_solution.update(status=new_status)
    if ucp_solution.user_contest_problem.status != ProblemStatus.OK:
        ucp_solution.user_contest_problem.update(status=new_status)

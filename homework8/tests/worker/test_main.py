import rq.timeouts

from database import proxy
from worker.main import process_code, process_code_failure


def test_process_code_wa(user_with_all, ucp_solution_getter):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        _,
    ) = ucp_solution_getter('wa')
    process_code(ucp_solution)

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'WA'
    assert ucp_solution.status == 'WA'
    assert uc_problem.score == 0
    assert ucp_solution.score == 0
    assert user_contest.score == 0


def test_process_code_wa_status_was_ok(user_with_all, ucp_solution_getter):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('wa', 'ok')
    process_code(ucp_solution)

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'OK'
    assert ucp_solution.status == 'WA'
    assert uc_problem.score == 100
    assert ucp_solution.score == 0
    assert user_contest.score == 100


def test_process_code_wa_score_was_50(user_with_all, ucp_solution_getter):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('wa', 'ok50')
    process_code(ucp_solution)

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'WA'
    assert ucp_solution.status == 'WA'
    assert uc_problem.score == 50
    assert ucp_solution.score == 0
    assert user_contest.score == 50


def test_process_code_ok(user_with_all, ucp_solution_getter):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('ok')
    process_code(ucp_solution)

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'OK'
    assert ucp_solution.status == 'OK'
    assert uc_problem.score == 100
    assert ucp_solution.score == 100
    assert user_contest.score == 100


def test_process_code_ok_score_was_50(user_with_all, ucp_solution_getter):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('ok', 'ok50')
    process_code(ucp_solution)

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'OK'
    assert ucp_solution.status == 'OK'
    assert uc_problem.score == 100
    assert ucp_solution.score == 100
    assert user_contest.score == 100


def test_process_code_failure_tl(
    user_with_all, ucp_solution_getter, job_getter
):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('wa')
    process_code_failure(
        job_getter(ucp_solution),
        None,
        rq.timeouts.JobTimeoutException,
        None,
        None,
    )

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'TL'
    assert ucp_solution.status == 'TL'
    assert uc_problem.score == 0
    assert ucp_solution.score == 0
    assert user_contest.score == 0


def test_process_code_failure_tl_was_ok(
    user_with_all, ucp_solution_getter, job_getter
):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('wa', 'ok')
    process_code_failure(
        job_getter(ucp_solution),
        None,
        rq.timeouts.JobTimeoutException,
        None,
        None,
    )

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'OK'
    assert ucp_solution.status == 'TL'
    assert uc_problem.score == 100
    assert ucp_solution.score == 0
    assert user_contest.score == 100


def test_process_code_failure_re(
    user_with_all, ucp_solution_getter, job_getter
):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('wa')
    process_code_failure(
        job_getter(ucp_solution), None, ValueError, None, None
    )

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'RE'
    assert ucp_solution.status == 'RE'
    assert uc_problem.score == 0
    assert ucp_solution.score == 0
    assert user_contest.score == 0


def test_process_code_failure_re_was_ok(
    user_with_all, ucp_solution_getter, job_getter
):
    (
        ucp_solution,
        kwargs,
        contest,
        user_contest,
        c_problem,
        uc_problem,
    ) = ucp_solution_getter('wa', 'ok')
    process_code_failure(
        job_getter(ucp_solution), None, ValueError, None, None
    )

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'OK'
    assert ucp_solution.status == 'RE'
    assert uc_problem.score == 100
    assert ucp_solution.score == 0
    assert user_contest.score == 100

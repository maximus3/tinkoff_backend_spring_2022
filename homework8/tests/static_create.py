from database import proxy


def create_data(user=None):
    proxy.ProblemProxy.create(
        name='Sum',
        description='Sum two numbers',
        input='Two numbers',
        output='The sum of the two numbers',
    )
    proxy.ProblemProxy.create(
        name='Sub',
        description='Subtraction of two numbers',
        input='Two numbers',
        output='Subtraction of two numbers',
    )
    proxy.ProblemProxy.create(
        name='Mul',
        description='Multiplication of two numbers',
        input='Two numbers',
        output='Multiplication of two numbers',
    )

    proxy.ContestProxy.create(name='Contest 1', description='Contest 1')
    proxy.ContestProxy.create(name='Contest 2', description='Contest 2')

    proxy.ContestProblemProxy.create(contest_id=1, problem_id=1, order=1)
    proxy.ContestProblemProxy.create(contest_id=1, problem_id=2, order=2)
    proxy.ContestProblemProxy.create(contest_id=2, problem_id=1, order=1)
    proxy.ContestProblemProxy.create(contest_id=2, problem_id=3, order=2)

    proxy.TestCaseProxy.create(problem_id=1, input='1 2', output='3')
    proxy.TestCaseProxy.create(problem_id=1, input='2 3', output='5')
    proxy.TestCaseProxy.create(problem_id=1, input='4 3', output='7')

    proxy.TestCaseProxy.create(problem_id=2, input='1 2', output='-1')
    proxy.TestCaseProxy.create(problem_id=2, input='2 3', output='-1')
    proxy.TestCaseProxy.create(problem_id=2, input='4 3', output='1')

    proxy.TestCaseProxy.create(problem_id=3, input='1 2', output='2')
    proxy.TestCaseProxy.create(problem_id=3, input='2 3', output='6')
    proxy.TestCaseProxy.create(problem_id=3, input='4 3', output='12')

    if user is None:
        return None

    contest = proxy.ContestProxy.get(name='Contest 1')
    if contest is None:
        return None
    proxy.UserContestProxy.create(user_id=user.id, contest_id=contest.id)
    user_contest = proxy.UserContestProxy.get(
        user_id=user.id, contest_id=contest.id
    )
    if user_contest is None:
        return None
    for c_problem in proxy.ContestProblemProxy.get_all(contest_id=contest.id):
        proxy.UserContestProblemProxy.create(
            user_contest_id=user_contest.id,
            problem_id=c_problem.problem.id,
            contest_problem_id=c_problem.id,
        )

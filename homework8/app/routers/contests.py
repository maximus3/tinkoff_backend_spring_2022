import datetime as dt
import logging
from typing import Any

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.utils import login_required
from config.redis import redis_queue
from config.text import TextData
from database.proxy import (
    ContestProblemProxy,
    ContestProxy,
    UserContestProblemProxy,
    UserContestProblemSolutionProxy,
    UserContestProxy,
)
from worker.main import process_code, process_code_failure

bp = Blueprint('contests', __name__)
logger = logging.getLogger(__name__)


@bp.route('/contests', methods=['GET'])
@login_required
def index() -> Any:
    contests = ContestProxy.get_all()
    return render_template('contests.html', contests=contests)


@bp.route('/contests/<int:contest_id>', methods=['GET'])
@login_required
def contest_by_id(contest_id: int) -> Any:
    contest = ContestProxy.get(id=contest_id)
    if contest is None:
        return render_template('404.html'), 404
    user_contest = UserContestProxy.get(
        user_id=current_user.id, contest_id=contest.id
    )
    uc_problems = (
        UserContestProblemProxy.get_all(user_contest_id=user_contest.id)
        if user_contest
        else []
    )
    return render_template(
        'contest_by_id.html',
        contest=contest,
        user_contest=user_contest,
        uc_problems=uc_problems,
    )


@bp.route('/contests/<int:contest_id>/registration', methods=['POST'])
@login_required
def registration(contest_id: int) -> Any:
    contest = ContestProxy.get(id=contest_id)
    if contest is None:
        return render_template('404.html'), 404
    user_contest = UserContestProxy.get(
        user_id=current_user.id, contest_id=contest.id
    )
    if user_contest is not None:
        return redirect(
            url_for('contests.contest_by_id', contest_id=contest.id)
        )
    if not UserContestProxy.create(
        user_id=current_user.id, contest_id=contest.id
    ):
        flash(TextData.SMTH_ERROR)
        logger.info('failed create UserContestProxy')
        return redirect(
            url_for('contests.contest_by_id', contest_id=contest.id)
        )
    user_contest = UserContestProxy.get(
        user_id=current_user.id, contest_id=contest.id
    )
    if user_contest is None:
        flash(TextData.SMTH_ERROR)
        logger.info('failed get UserContestProxy')
        return redirect(
            url_for('contests.contest_by_id', contest_id=contest.id)
        )
    for c_problem in ContestProblemProxy.get_all(contest_id=contest.id):
        UserContestProblemProxy.create(
            user_contest_id=user_contest.id,
            problem_id=c_problem.problem.id,
            contest_problem_id=c_problem.id,
        )
    return redirect(url_for('contests.contest_by_id', contest_id=contest.id))


@bp.route('/contests/<int:contest_id>/<int:order>', methods=['GET'])
@login_required
def task_by_id(contest_id: int, order: int) -> Any:
    contest = ContestProxy.get(id=contest_id)
    if contest is None:
        return render_template('404.html'), 404
    user_contest = UserContestProxy.get(
        user_id=current_user.id, contest_id=contest.id
    )
    if user_contest is None:
        return redirect(
            url_for('contests.contest_by_id', contest_id=contest.id)
        )
    c_problem = ContestProblemProxy.get(contest_id=contest.id, order=order)
    if c_problem is None:
        return render_template('404.html'), 404
    uc_problem = UserContestProblemProxy.get(
        user_contest_id=user_contest.id,
        problem_id=c_problem.problem.id,
        contest_problem_id=c_problem.id,
    )
    if uc_problem is None:
        flash(TextData.SMTH_ERROR)
        logger.info('failed get UserContestProblemProxy')
        return redirect(
            url_for('contests.contest_by_id', contest_id=contest.id)
        )
    all_uc_problems = UserContestProblemProxy.get_all(
        user_contest_id=user_contest.id
    )
    ucp_solutions = UserContestProblemSolutionProxy.get_all(
        user_contest_problem_id=uc_problem.id
    )
    return render_template(
        'task_by_id.html',
        contest=contest,
        user_contest=user_contest,
        uc_problem=uc_problem,
        ucp_solutions=ucp_solutions,
        all_uc_problems=all_uc_problems,
    )


@bp.route('/contests/<int:contest_id>/<int:order>/submit', methods=['POST'])
@login_required
def submit(contest_id: int, order: int) -> Any:
    contest = ContestProxy.get(id=contest_id)
    if contest is None:
        return render_template('404.html'), 404
    user_contest = UserContestProxy.get(
        user_id=current_user.id, contest_id=contest.id
    )
    if user_contest is None:
        return redirect(
            url_for('contests.contest_by_id', contest_id=contest.id)
        )
    c_problem = ContestProblemProxy.get(contest_id=contest.id, order=order)
    if c_problem is None:
        return render_template('404.html'), 404

    uc_problem = UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    if uc_problem is None:
        flash(TextData.SMTH_ERROR)
        logger.info('failed get uc_problem')
        return redirect(
            url_for('contests.task_by_id', contest_id=contest.id, order=order)
        )
    kwargs = {
        'created_at': dt.datetime.now(),
        'user_contest_problem_id': uc_problem.id,
        'code': request.form.get('code'),
    }
    if not UserContestProblemSolutionProxy.create(**kwargs):
        flash(TextData.SMTH_ERROR)
        logger.info('failed create ucp_solution')
        return redirect(
            url_for('contests.task_by_id', contest_id=contest.id, order=order)
        )
    kwargs.pop('code')
    ucp_solution = UserContestProblemSolutionProxy.get(**kwargs)
    redis_queue.enqueue(
        process_code,
        job_timeout='1s',
        on_failure=process_code_failure,
        args=(ucp_solution,),
    )

    return redirect(
        url_for('contests.task_by_id', contest_id=contest.id, order=order)
    )

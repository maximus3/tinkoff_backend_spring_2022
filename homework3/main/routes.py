import logging
from typing import Any, Dict

from flask import Blueprint, redirect, render_template, request

from .task import Task, TaskType

logger = logging.getLogger(__name__)

list_of_tasks: Dict[str, Dict[int, Task]] = {
    TaskType.NEW: {},
    TaskType.DONE: {},
}
CURRENT_TASK_ID = 0

bp = Blueprint('app', __name__)


@bp.route('/')
def index() -> Any:
    return redirect('/tasks')


@bp.route('/tasks')
def tasks() -> Any:
    status = request.args.get('status')
    if status is None or status == TaskType.ALL:
        return render_template(
            'tasks.html',
            list_name=TaskType.ALL,
            tasks=list_of_tasks[TaskType.NEW] | list_of_tasks[TaskType.DONE],
        )
    return render_template(
        'tasks.html', list_name=status, tasks=list_of_tasks[status]
    )


@bp.route('/add_task', methods=['POST'])
def add_task() -> Any:
    task_name = request.form.get('task_name')
    if task_name is None or task_name == '':
        logger.warning('task_name is None or empty')
        return (
            render_template('error.html', msg='task_name is None or empty'),
            500,
        )
    global CURRENT_TASK_ID
    task_id = CURRENT_TASK_ID
    CURRENT_TASK_ID += 1
    list_of_tasks[TaskType.NEW][task_id] = Task(task_name, task_id)
    logger.info('New task %s added', task_name)
    return redirect('/tasks')


@bp.route('/complete', methods=['POST'])
def complete() -> Any:
    task_complete = request.form.get('complete_btn')
    if task_complete is None:
        logger.warning('complete_btn is None')
        return render_template('error.html', msg='complete_btn is None'), 500
    task_id = int(task_complete)
    if task_id not in list_of_tasks[TaskType.NEW]:
        logger.warning('No such task_id')
        return render_template('error.html', msg='No such task_id'), 404
    list_of_tasks[TaskType.NEW][task_id].finish()
    list_of_tasks[TaskType.DONE][task_id] = list_of_tasks[TaskType.NEW].pop(
        task_id
    )
    logger.info(
        'Task %s completed', list_of_tasks[TaskType.DONE][task_id].name
    )
    return redirect('/tasks')

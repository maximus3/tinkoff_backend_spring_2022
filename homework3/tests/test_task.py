from main.task import Task


def test_finish():
    task = Task('task', 0)
    assert task.is_finished is False
    task.finish()
    assert task.is_finished

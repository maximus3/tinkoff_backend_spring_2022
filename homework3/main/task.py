class Task:
    def __init__(self, name: str, task_id: int) -> None:
        self.name = name
        self.is_finished = False
        self.task_id = task_id

    def finish(self) -> None:
        self.is_finished = True


class TaskType:
    ALL = 'all'
    NEW = 'active'
    DONE = 'finished'

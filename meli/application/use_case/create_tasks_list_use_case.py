from meli.infra.repository.connection import SessionLocal
from meli.infra.repository.task_repository import get_tasks, TaskRepository
from meli.infra.repository.url_scrappe_repository import create_url


class CreateTaskListUseCase:

    def __init__(self, db: SessionLocal):
        self.db = db

    def execute(self):
        tasks = get_tasks(self.db)
        for task in tasks:
            create_url(self.db, task.url, 'list')

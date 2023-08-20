from meli.infra.repository.connection import SessionLocal
from meli.infra.repository.task_repository import get_tasks
from meli.infra.repository.url_scrappe_repository import create_url


class CreateTaskListUseCase:
    """Class providingFunction to create task to scrape list in database"""

    def __init__(self, db_connection: SessionLocal):
        self.db_connection = db_connection

    def execute(self):
        tasks = get_tasks(self.db_connection)
        for task in tasks:
            create_url(self.db_connection, task.url, 'list')

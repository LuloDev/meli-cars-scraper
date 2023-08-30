from sqlalchemy.exc import DatabaseError, IntegrityError


from meli.infra.repository.connection import SessionLocal
from meli.infra.repository.task_repository import get_tasks
from meli.infra.repository.url_scrappe_repository import create_url


class CreateTaskListUseCase:
    """Class providingFunction to create task to scrape list in database"""

    def __init__(self, db_connection: SessionLocal):
        self.db_connection = db_connection

    def execute(self):
        try:
            tasks = get_tasks(self.db_connection)
            for task in tasks:
                self.save_url(task.url)
        except IntegrityError as e:
            print(e)
            self.db_connection.rollback()
        except DatabaseError as e:
            print(e)
            self.db_connection.rollback()

    def save_url(self, url_task: str):
        create_url(self.db_connection, url_task, 'list')

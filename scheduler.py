from sqlalchemy.orm import Session
from rocketry import Rocketry

from meli.infra.repository import car_repository
from meli.infra.repository import history_price_repository
from meli.infra.repository import url_scrappe_repository
from meli.infra.repository import task_repository
from meli.infra.repository.connection import db_connection, engine
from meli.application.use_case.create_tasks_list_use_case import CreateTaskListUseCase
from meli.application.use_case.execute_next_task_use_case import ExecuteNextTaskUseCase

car_repository.Base.metadata.create_all(bind=engine)
history_price_repository.Base.metadata.create_all(bind=engine)
task_repository.Base.metadata.create_all(bind=engine)
url_scrappe_repository.Base.metadata.create_all(bind=engine)


app = Rocketry(execution="async")


@app.task('every 1 day')
def create_task_scrape():
    db: Session = db_connection
    task_use_case = CreateTaskListUseCase(db)
    task_use_case.execute()


@app.task('every 20 minute')
def execute_next_task():
    db: Session = db_connection
    task_use_case = ExecuteNextTaskUseCase(db)
    task_use_case.execute_list()


@app.task('every 1 minute')
def execute_task_item():
    db: Session = db_connection
    task_use_case = ExecuteNextTaskUseCase(db)
    task_use_case.execute_item()


if __name__ == "__main__":
    app.run()

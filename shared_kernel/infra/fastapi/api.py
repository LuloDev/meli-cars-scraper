from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from shared_kernel.infra.schedule.scheduler import app as app_rocketry

from meli.infra.repository import car_repository
from meli.infra.repository import history_price_repository
from meli.infra.repository import url_scrappe_repository
from meli.infra.repository import task_repository
from meli.infra.repository.connection import get_db, engine
from meli.application.use_case.create_tasks_list_use_case import CreateTaskListUseCase

car_repository.Base.metadata.create_all(bind=engine)
history_price_repository.Base.metadata.create_all(bind=engine)
task_repository.Base.metadata.create_all(bind=engine)
url_scrappe_repository.Base.metadata.create_all(bind=engine)


app = FastAPI()
session = app_rocketry.session


@app.get("/tasks")
async def get_tasks():
    return session.tasks


@app.get("/execute/task/list", response_model=None)
async def execute_task():
    task = session['execute_next_task_list']
    await task.execute()


@app.get("/execute/task/items", response_model=None)
async def execute_task_item():
    task = session['execute_task_item']
    await task.execute()


@app.get("/create/task", response_model=None)
def create_task(db_connection: Session = Depends(get_db)):
    task_use_case = CreateTaskListUseCase(db_connection)
    task_use_case.execute()


if __name__ == "__main__":
    app.run()

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
# from rocketry import Rocketry

from meli.infra.repository import car_repository
from meli.infra.repository import history_price_repository
from meli.infra.repository import url_scrappe_repository
from meli.infra.repository import task_repository
from meli.infra.repository.connection import get_db, engine
from meli.application.use_case.create_tasks_list_use_case import CreateTaskListUseCase
from meli.application.use_case.execute_next_task_use_case import ExecuteNextTaskUseCase

car_repository.Base.metadata.create_all(bind=engine)
history_price_repository.Base.metadata.create_all(bind=engine)
task_repository.Base.metadata.create_all(bind=engine)
url_scrappe_repository.Base.metadata.create_all(bind=engine)


app = FastAPI()
# sheduler = Rocketry()


""" @sheduler.task('every 1 day')
def create_task_scrape(db: Session = Depends(get_db)):
    task_use_case = CreateTaskListUseCase(db)
    task_use_case.execute()


@sheduler.task('every 20 minute')
def execute_next_task(db: Session = Depends(get_db)):
    task_use_case = ExecuteNextTaskUseCase(db)
    task_use_case.execute_list() """


@app.get("/execute/task", response_model=None)
def read_users(db: Session = Depends(get_db)):
    task_use_case = ExecuteNextTaskUseCase(db)
    task_use_case.execute_list()


@app.get("/execute/task/items", response_model=None)
def read_users(db: Session = Depends(get_db)):
    task_use_case = ExecuteNextTaskUseCase(db)
    task_use_case.execute_item()


@app.get("/create/task", response_model=None)
def read_users(db: Session = Depends(get_db)):
    task_use_case = CreateTaskListUseCase(db)
    task_use_case.execute()

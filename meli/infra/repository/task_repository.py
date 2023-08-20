import datetime
import dataclasses
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


@dataclasses.dataclass
class TaskRepository(Base):
    """Class orm map table for task to schedule scrappe"""
    __tablename__ = 'tasks'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    url = sqlalchemy.Column(sqlalchemy.String(
        length=1000), unique=True, nullable=False)
    date_last_attempt = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=True, default=datetime.datetime.utcnow)
    error = sqlalchemy.Column(sqlalchemy.String(length=1000), nullable=True)
    create_at = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)


def create_task(db_connection: Session, url_task: str):
    db_task = TaskRepository()
    db_task.url = url_task
    db_connection.add(db_task)
    db_connection.commit()
    db_connection.refresh(db_task)
    return db_task


def get_tasks(db_connection: Session):
    return db_connection.query(TaskRepository).all()

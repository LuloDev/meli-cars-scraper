import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class TaskRepository(Base):
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


def create_task(db: Session, url: str):
    db_task = TaskRepository()
    db_task.url = url
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session):
    return db.query(TaskRepository).all()

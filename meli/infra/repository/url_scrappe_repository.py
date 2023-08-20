import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class UrlRepository(Base):
    __tablename__ = 'urls'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    type_url = sqlalchemy.Column(sqlalchemy.String(length=200), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String(
        length=1000), unique=True, nullable=False)
    attempts = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date_last_attempt = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=True, default=datetime.datetime.utcnow)
    error = sqlalchemy.Column(sqlalchemy.String(length=1000), nullable=True)
    create_at = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)


def create_url(db: Session, url: str, type_url: str):
    db_url = UrlRepository()
    db_url.type_url = type_url
    db_url.url = url
    db_url.attempts = 0
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def delete_url(db: Session, url: str):
    db.query(UrlRepository).filter(UrlRepository.url == url).delete()
    db.commit()


def error_on_scrape(db: Session, id: int, error: str):
    error_trunc = (error[:1000]) if len(error) > 1000 else error
    db.query(UrlRepository).filter(UrlRepository.id == id).update(
        {UrlRepository.error: error_trunc,
         UrlRepository.attempts: UrlRepository.attempts + 1,
         UrlRepository.date_last_attempt: datetime.datetime.now(),
         UrlRepository.update_at: datetime.datetime.now()})
    db.commit()


def get_next_url(db: Session, type_url: str):
    return db.query(UrlRepository).filter(
        UrlRepository.type_url == type_url).first()

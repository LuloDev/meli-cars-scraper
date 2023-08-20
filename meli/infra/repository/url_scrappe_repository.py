import datetime
import dataclasses
import sqlalchemy


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


@dataclasses.dataclass
class UrlRepository(Base):
    """Class orm map table for url list to scrappe"""
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


def create_url(db_connection: Session, url_to_scrappe: str, type_url: str):
    db_url = UrlRepository()
    db_url.type_url = type_url
    db_url.url = url_to_scrappe
    db_url.attempts = 0
    db_connection.add(db_url)
    db_connection.commit()
    db_connection.refresh(db_url)
    return db_url


def delete_url(db_connection: Session, url_to_scrappe: str):
    db_connection.query(UrlRepository).filter(
        UrlRepository.url == url_to_scrappe).delete()
    db_connection.commit()


def error_on_scrape(db_connection: Session, id_url: int, error_text: str):
    error_trunc = (error_text[:1000]) if len(error_text) > 1000 else error_text
    db_connection.query(UrlRepository).filter(UrlRepository.id == id_url).update(
        {UrlRepository.error: error_trunc,
         UrlRepository.attempts: UrlRepository.attempts + 1,
         UrlRepository.date_last_attempt: datetime.datetime.now(),
         UrlRepository.update_at: datetime.datetime.now()})
    db_connection.commit()


def get_next_url(db_connection: Session, type_url: str):
    return db_connection.query(UrlRepository).filter(
        UrlRepository.type_url == type_url).first()

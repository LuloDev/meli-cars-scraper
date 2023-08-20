import datetime
import dataclasses
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


@dataclasses.dataclass
class PriceHistoryRepository(Base):
    """Class orm map table for hitory prices"""
    __tablename__ = 'price_history'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    id_car = sqlalchemy.Column(
        sqlalchemy.Integer, index=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    create_at = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)


def create_price(db_connection: Session, id_car: int, price_car: float):
    db_price = PriceHistoryRepository()
    db_price.id_car = id_car
    db_price.price = price_car
    db_connection.add(db_price)
    db_connection.commit()
    db_connection.refresh(db_price)
    return db_price

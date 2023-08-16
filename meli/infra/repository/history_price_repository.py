import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


from meli.domain.entity.product_meli import MeliItem


Base = declarative_base()


class PriceHistoryRepository(Base):
    __tablename__ = 'price_history'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    id_car = sqlalchemy.Column(
        sqlalchemy.Integer, index=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    create_at = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
def create_price(db: Session, id_car: int, price: float):
    db_price = PriceHistoryRepository()
    db_price.id_car = id_car
    db_price.price = price
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
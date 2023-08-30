import datetime
import dataclasses
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


from shared_kernel.domain.value_object import TypeFuel, TypeTransmission
from meli.domain.entity.product_meli import MeliItem


Base = declarative_base()


@dataclasses.dataclass
class CarRepository(Base):
    """Class orm map table for cars"""
    __tablename__ = 'cars'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=200), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String(
        length=200), unique=True, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    create_at = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.String(length=100), nullable=True)
    engine = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    brand = sqlalchemy.Column(sqlalchemy.String(length=200), nullable=True)
    model = sqlalchemy.Column(sqlalchemy.String(length=200), nullable=True)
    version = sqlalchemy.Column(sqlalchemy.String(length=200), nullable=True)
    type_fueld = sqlalchemy.Column(sqlalchemy.Enum(TypeFuel))
    transmission = sqlalchemy.Column(
        sqlalchemy.Enum(TypeTransmission), nullable=True)
    kilometers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date_published = sqlalchemy.Column(sqlalchemy.Date, nullable=True)


def create_car(db_connection: Session, car_item: MeliItem):
    db_car = CarRepository()
    db_car.title = car_item.title
    db_car.url = car_item.url
    db_car.year = car_item.year
    db_car.price = car_item.price
    db_connection.add(db_car)
    db_connection.commit()
    db_connection.refresh(db_car)
    return db_car


def update_price(db_connection: Session, car_item: MeliItem, id_car: int):
    db_connection.query(CarRepository).filter(CarRepository.id == id_car).update(
        {CarRepository.price: car_item.price, CarRepository.update_at: datetime.datetime.now()})
    db_connection.commit()


def complete_data(db_connection: Session, car_item: MeliItem, id_car: int):
    db_connection.query(CarRepository).filter(
        CarRepository.id == id_car).update({CarRepository.price: car_item.price,
                                            CarRepository.color: car_item.color,
                                            CarRepository.engine: car_item.engine,
                                            CarRepository.brand: car_item.brand,
                                            CarRepository.model: car_item.model,
                                            CarRepository.version: car_item.version,
                                            CarRepository.type_fueld: car_item.type_fueld,
                                            CarRepository.transmission: car_item.transmission,
                                            CarRepository.kilometers: car_item.kilometers,
                                            CarRepository.date_published: car_item.date_published,
                                            CarRepository.update_at: datetime.datetime.now()})
    db_connection.commit()


def get_first_by_url(db_connection: Session, url_search: str):
    return db_connection.query(CarRepository).filter(CarRepository.url == url_search).first()

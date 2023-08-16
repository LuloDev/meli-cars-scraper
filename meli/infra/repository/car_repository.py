import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


from shared_kernel.domain.value_object import TypeFuel, TypeTransmission
from meli.domain.entity.product_meli import MeliItem


Base = declarative_base()


class CarRepository(Base):
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


def create_car(db: Session, car: MeliItem):
    db_car = CarRepository()
    db_car.title = car.title
    db_car.url = car.url
    db_car.year = car.year
    db_car.price = car.price
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_price(db: Session, car: MeliItem, id: int):
    db.query(CarRepository).filter(CarRepository.id == id).update(
        {CarRepository.price: car.price, CarRepository.update_at: datetime.datetime.now()})
    db.commit()


def complete_data(db: Session, car: MeliItem, id: int):
    db.query(CarRepository).filter(CarRepository.id == id).update({CarRepository.price: car.price,
                                                                   CarRepository.color: car.color,
                                                                   CarRepository.engine: car.engine,
                                                                   CarRepository.brand: car.brand,
                                                                   CarRepository.model: car.model,
                                                                   CarRepository.version: car.version,
                                                                   CarRepository.type_fueld: car.typeFueld,
                                                                   CarRepository.transmission: car.transmission,
                                                                   CarRepository.kilometers: car.kilometers,
                                                                   CarRepository.date_published: car.date_published,
                                                                   CarRepository.update_at: datetime.datetime.now()})
    db.commit()


def get_first_by_url(db: Session, url: str):
    return db.query(CarRepository).filter(CarRepository.url == url).first()

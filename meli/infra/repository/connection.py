from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://admin:password@192.168.31.200:3306/MELICARS?charset=utf8mb4"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
db_connection = SessionLocal()


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

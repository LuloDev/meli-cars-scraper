from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from meli.infra.repository import car_repository
from meli.infra.repository import history_price_repository
from meli.infra.repository.connection import get_db, engine
from meli.domain.entity.product_meli import MeliItem
from meli.application.use_case.scrape_list_use_case import ScrapeListUseCase
from meli.application.use_case.scrape_item_use_case import ScrapeItemUseCase

car_repository.Base.metadata.create_all(bind=engine)
history_price_repository.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/getlist/", response_model=list[MeliItem])
def read_users(db: Session = Depends(get_db)):
    scrape_list_use_case = ScrapeListUseCase(db)
    scrape_list_use_case.execute()
    return list()


@app.get("/getitem/", response_model=None)
def read_users(db: Session = Depends(get_db)):
    scrape_item_use_case = ScrapeItemUseCase(
        db, 'https://carro.mercadolibre.com.co/MCO-1786303240-ford-ranger-32-limited-_JM')
    return scrape_item_use_case.execute()

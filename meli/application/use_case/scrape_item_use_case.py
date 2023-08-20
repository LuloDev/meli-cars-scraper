from datetime import datetime
from sqlalchemy.orm import Session


from meli.infra.repository.connection import SessionLocal, db
from meli.infra.repository.car_repository import complete_data, get_first_by_url, Base
from meli.infra.repository.url_scrappe_repository import delete_url
from meli.infra.scrappers.scrappe import MeliScrappe
from meli.infra.queue.connection import q
from meli.infra.repository.connection import engine


class ScrapeItemUseCase:

    def __init__(self, db: SessionLocal, url: str) -> None:
        self.db = db
        self.url = url

    def execute(self):
        self.enqueue_scrape_item()

    def enqueue_scrape_item(self):
        q.enqueue(scrape_item, self.url)


def scrape_item(url: str):
    Base.metadata.create_all(bind=engine)
    scrape = MeliScrappe()
    item = scrape.scrape_data_item(url)
    prev_car = get_first_by_url(db, url)
    if (prev_car is not None):
        complete_data(db, item, prev_car.id)
        if any([item.brand, item.color, item.engine, item.model, item.typeFueld, item.transmission, item.version]):
            delete_url(db, url)

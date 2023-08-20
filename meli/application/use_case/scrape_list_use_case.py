from meli.infra.repository.connection import SessionLocal
from meli.infra.scrappers.scrappe import MeliScrappe
from meli.domain.entity.product_meli import MeliItem
from meli.infra.repository.car_repository import create_car, get_first_by_url, update_price
from meli.infra.repository.url_scrappe_repository import create_url, delete_url


class ScrapeListUseCase:

    def __init__(self, db: SessionLocal, url: str) -> None:
        self.db = db
        self.scrape = MeliScrappe()
        self.url = url

    def execute(self):
        meliScrappe = MeliScrappe()
        result = meliScrappe.scrape_list(self.url)
        next_url: str | None = result[1]
        items: [MeliItem] = result[0]
        for value in items:
            self.saveItem(value)
        if next_url is not None:
            create_url(self.db, next_url, 'list')
        delete_url(self.db, self.url)

    def saveItem(self, item: MeliItem):
        prev_car = get_first_by_url(self.db, item.url)
        if prev_car is None:
            create_car(self.db, item)
            create_url(self.db, item.url, 'item')
        else:
            update_price(self.db, item, prev_car.id)

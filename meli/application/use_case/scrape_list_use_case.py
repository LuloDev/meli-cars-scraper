from meli.infra.repository.connection import SessionLocal
from meli.infra.scrappers.scrappe import MeliScrappe
from meli.domain.entity.product_meli import MeliItem
from meli.infra.repository.car_repository import create_car, get_first_by_url, update_price
from meli.infra.repository.url_scrappe_repository import create_url, delete_url
from meli.infra.repository.history_price_repository import create_price


class ScrapeListUseCase:
    """Class providingFunction to scrappe list items data and save data"""

    def __init__(self, db_connection: SessionLocal, url: str) -> None:
        self.db_connection = db_connection
        self.scrape = MeliScrappe()
        self.url = url

    def execute(self):
        meli_scrappe = MeliScrappe()
        result = meli_scrappe.scrape_list(self.url)
        next_url: str | None = result[1]
        items: [MeliItem] = result[0]
        for value in items:
            self.save_item(value)
        if next_url is not None:
            create_url(self.db_connection, next_url, 'list')
        delete_url(self.db_connection, self.url)

    def save_item(self, item: MeliItem):
        prev_car = get_first_by_url(self.db_connection, item.url)
        if prev_car is None:
            car = create_car(self.db_connection, item)
            create_price(self.db_connection, car.id, car.price)
            create_url(self.db_connection, item.url, 'item')
        else:
            update_price(self.db_connection, item, prev_car.id)
            if prev_car.price != item.price:
                create_price(self.db_connection, car.id, car.price)

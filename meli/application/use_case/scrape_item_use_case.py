from meli.infra.repository.connection import SessionLocal, db_connection
from meli.infra.repository.car_repository import complete_data, get_first_by_url, Base
from meli.infra.repository.url_scrappe_repository import delete_url, error_on_scrape
from meli.infra.scrappers.scrappe import MeliScrappe
from meli.infra.repository.connection import engine
from shared_kernel.domain.exception import IncompleteDataException


class ScrapeItemUseCase:
    """Class providingFunction to scrappe one item data and save data"""

    def __init__(self, db_connection_session: SessionLocal, url: str):
        self.db_connection = db_connection_session
        self.url = url

    def execute(self):
        self.enqueue_scrape_item()

    def enqueue_scrape_item(self):
        try:
            Base.metadata.create_all(bind=engine)
            scrape = MeliScrappe()
            item = scrape.scrape_data_item(self.url)
            if item is None:
                delete_url(db_connection, self.url)
                return
            prev_car = get_first_by_url(db_connection, self.url)
            if prev_car is not None:
                complete_data(db_connection, item, prev_car.id)
                if any([item.brand, item.color, item.engine,
                        item.model, item.type_fueld, item.transmission, item.version]):
                    delete_url(db_connection, self.url)
                else:
                    error_text = 'Not found data on page, maybe is a deleted item or a invalid url'
                    error_on_scrape(
                        db_connection, self.url, error_text)
                    raise IncompleteDataException()
        except IncompleteDataException as e:
            print('Not found data on page, maybe is a deleted item or a invalid url')
            raise e
        except Exception as e:
            print(e)
            error_on_scrape(
                db_connection, self.url, str(e))
            raise e

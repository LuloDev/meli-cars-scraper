from meli.infra.repository.connection import SessionLocal
from meli.infra.repository.url_scrappe_repository import get_next_url, UrlRepository
from meli.application.use_case.scrape_list_use_case import ScrapeListUseCase
from meli.application.use_case.scrape_item_use_case import ScrapeItemUseCase


class ExecuteNextTaskUseCase:
    """Class providingFunction execute next task scrappe"""

    def __init__(self, db_connection: SessionLocal):
        self.db_connection = db_connection

    def execute_list(self):
        url: UrlRepository = get_next_url(self.db_connection, 'list')
        if url is not None:
            scrape_list_use_case = ScrapeListUseCase(
                self.db_connection, url.url)
            scrape_list_use_case.execute()

    def execute_item(self):
        url: UrlRepository = get_next_url(self.db_connection, 'item')
        if url is not None:
            scrape_item_use_case = ScrapeItemUseCase(
                self.db_connection, url.url)
            scrape_item_use_case.execute()

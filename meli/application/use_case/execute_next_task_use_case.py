from meli.infra.repository.connection import SessionLocal
from meli.infra.repository.url_scrappe_repository import get_next_url, UrlRepository
from meli.application.use_case.scrape_list_use_case import ScrapeListUseCase
from meli.application.use_case.scrape_item_use_case import ScrapeItemUseCase


class ExecuteNextTaskUseCase:

    def __init__(self, db: SessionLocal):
        self.db = db

    def execute_list(self):
        url: UrlRepository = get_next_url(self.db, 'list')
        if (url is not None):
            scrape_list_use_case = ScrapeListUseCase(self.db, url.url)
            scrape_list_use_case.execute()

    def execute_item(self):
        url: UrlRepository = get_next_url(self.db, 'item')
        if (url is not None):
            scrape_item_use_case = ScrapeItemUseCase(self.db, url.url)
            scrape_item_use_case.execute()

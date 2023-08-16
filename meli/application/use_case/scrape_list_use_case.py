from meli.infra.repository.connection import SessionLocal
from meli.infra.scrappers.scrappe import MeliScrappe
from meli.domain.entity.product_meli import MeliItem


class ScrapeListUseCase:

    def __init__(self, db: SessionLocal) -> None:
        self.db = db
        self.scrape = MeliScrappe()

    def execute(self):
        meliScrappe = MeliScrappe()
        result = meliScrappe.scrape_list(
            "https://carros.mercadolibre.com.co/ford/ranger/ford-ranger_NoIndex_True")
        return result

import re
import requests

from bs4 import BeautifulSoup, Tag

from meli.domain.entity.product_meli import MeliItem
from shared_kernel.domain.value_object import TypeFuel, TypeTransmission


class MeliScrappe():
    """Class providingFunction to scrappe and parse data from meli site"""

    def get(self, url: str):
        return requests.get(url, timeout=10)

    def scrape_list(self, url: str):
        data = self.get(url)
        soup = BeautifulSoup(data.text, 'lxml')
        items = soup.find_all('li', class_='ui-search-layout__item')
        next_links = soup.find_all('a', {'title': 'Siguiente'})
        if next_links:
            next_url = next_links[0]['href']
        else:
            next_url = None
        return [map(self.get_data_item, items), next_url]

    def sanetize_url(self, url: str):
        return url.split('#')[0]

    def get_data_item(self, item: Tag):
        url = self.sanetize_url(item.div.div.div.section.div
                                .next_sibling.div.div.div.a['href'])
        title = item.div.div.div.section.div.next_sibling.div.div.div.a['title']
        div_data = item.div.div.div.next_sibling.div.div
        price = div_data.div.div.div.span.span.next_sibling.next_sibling.text
        year = div_data.next_sibling.ul.li.text
        item_data = MeliItem()
        item_data.title = title
        item_data.url = url
        item_data.price = float(price.replace(".", ""))
        item_data.year = int(year)
        return item_data

    def scrape_data_item(self, url: str) -> MeliItem:
        item_data = MeliItem()
        result = self.get(url)
        item_data.url = url
        soup = BeautifulSoup(result.text, 'lxml')
        title = soup.find('h1', class_='ui-pdp-title')
        if title is None:
            return None
        item_data.title = title.text
        item_data.price = float(
            soup.find('span', class_='andes-money-amount__fraction').text.replace(".", ""))
        item_data.brand = self.extract_row_by_header(result.text, 'Marca')
        item_data.year = self.extract_row_by_header(result.text, 'Año')
        item_data.color = self.extract_row_by_header(result.text, 'Color')
        engine = self.extract_row_by_header(result.text, 'Motor')
        if engine is not None:
            item_data.engine = float(engine.replace(".", ""))
        kilometers = self.extract_row_by_header(
            result.text, 'Kilómetros')
        if kilometers is not None:
            item_data.kilometers = int(re.search(
                r'\d+', kilometers).group()) if re.search(r'\d+', kilometers) else None
        item_data.model = self.extract_row_by_header(result.text, 'Modelo')
        transmission = self.extract_row_by_header(
            result.text, 'Transmisión')
        if transmission is not None:
            if transmission == 'Automática':
                item_data.transmission = TypeTransmission.AUTOMATIC.value
            else:
                item_data.transmission = TypeTransmission.MECANIC.value

        type_fueld = self.extract_row_by_header(
            result.text, 'Tipo de combustible')
        if type_fueld is not None:
            if type_fueld == 'Diésel':
                item_data.type_fueld = TypeFuel.DIESEL.value
            else:
                item_data.type_fueld = TypeFuel.GASOLINE.value

        item_data.version = self.extract_row_by_header(result.text, 'Versión')
        return item_data

    def extract_row_by_header(self, html_content: str, header_name: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        target_row = None
        for row in soup.find_all('tr', class_='andes-table__row'):
            th_content = row.find('th', class_='andes-table__header--left')
            if th_content and th_content.text.strip() == header_name:
                target_row = row
                break
        if target_row:
            target_celd = target_row.find(
                'td', class_='andes-table__column--left')
            if target_celd:
                value = target_celd.find(
                    'span', class_='andes-table__column--value').text
                return value
        else:
            return None

from abc import ABC

from scrapy.loader import ItemLoader
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup


class Articulo(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    caracteristicas = Field()


class MercadoLibreCrawler(CrawlSpider, ABC):
    name = "Mercado Libre"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5',
        'CLOSESPIDER_PAGEOUNT': 5000,
        'ROBOTSTXT_OBEY': 'False'
    }

    download_delay = 1

    allowed_domains = ['autos.mercadolibre.com.mx', 'auto.mercadolibre.com.mx']
    start_urls = ['https://autos.mercadolibre.com.mx']
    handle_httpstatus_list = [403]
    rules = (
                # paginacion
        Rule(
            LinkExtractor(
            allow=r'/_Desde_'
            ), follow=True
            ),

        # vertical
        Rule(
            LinkExtractor(
                allow=r'/MLM-'
            ), follow=True, callback='parse_articulo'

        )


    )

    def parse_articulo(self, response):
        soup = BeautifulSoup(response.body)
        nombre = soup.find("h1").text
        precio = soup.find(class_="andes-money-amount__fraction").text
        descripcion = soup.find(class_="ui-pdp-description__content").text

        # get all the caracteristic name and value
        caract = [x.get_text() for x in soup.find_all(class_="andes-table__column--value")]
        tcaracteristicas = [x.get_text() for x in soup.find_all(class_="andes-table__header andes-table__"
                                                                       "header--left ui-pdp-specs__table__column "
                                                                       "ui-pdp-specs__table__column-title")]
        # convert to dict in order to use it on json
        cardict = dict(zip(tcaracteristicas, caract))

        item = ItemLoader(Articulo(), response.body)
        item.add_value("nombre", nombre)
        item.add_value('precio', precio)
        item.add_value('descripcion', descripcion)
        item.add_value('caracteristicas', cardict)
        yield item.load_item()





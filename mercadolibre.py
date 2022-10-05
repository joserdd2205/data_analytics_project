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
    marca = Field()
    modelo = Field()
    año = Field()
    color = Field()
    tipo_combustible = Field()
    kilometraje = Field()


class MercadoLibreCrawler(CrawlSpider, ABC):
    name = "Mercado Libre"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    download_delay = 1

    allowed_domains = ['auto.mercadolibre.com.mx', 'listado.mercadolibre.com.mx']
    start_urls = ['https://listado.mercadolibre.com.mx/autos']
    handle_httpstatus_list = [403]
    rules = (
        # paginacion
        Rule(
            LinkExtractor(
                allow=r'_Desde_'
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
        #TODO: Solve irregularities within table "caracteristicas" - some have 6 rows while others have 7 or more
        caracteristicas = [x.get_text() for x in soup.find_all(class_="andes-table__column--value")]


        marca, modelo, año, color, Tipo_combustible, kilometraje = caracteristicas

        item = ItemLoader(Articulo(), response.body)
        item.add_value("nombre", nombre)
        item.add_value('precio', precio)
        item.add_value('descripcion', descripcion)
        item.add_value('marca', marca)
        item.add_value('modelo', modelo)
        item.add_value('año', año)
        item.add_value('color', color)
        item.add_value('tipo_combustible', Tipo_combustible)
        item.add_value('kilometraje', kilometraje)
        yield item.load_item()

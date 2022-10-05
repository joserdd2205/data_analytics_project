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


class Articulo(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    marca = Field()
    modelo= Field()
    año=Field()
    color= Field()
    Tipo_combustible= Field()
    kilometraje = Field()


class MercadoLibreCrawler(CrawlSpider, ABC):
    name = "Mercado Libre"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    download_delay = 1

    allowed_domains = ['articulo.mercadolibre.com.mx', 'listado.mercadolibre.com.mx']
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
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)
        item.add_xpath('nombre', '//div[@id="header"]//h1/text()')
        item.add_xpath('precio', '//meta[@itemprop="price"]/@content')
        item.add_xpath('descripcion', '//p[@class="ui-pdp-description__content"]/text()')

        yield item.load_item()



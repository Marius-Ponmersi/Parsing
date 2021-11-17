import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_parser.items import LeroymerlinParserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://barnaul.leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()  # возвращается первое значение из списка
        if next_page:  # если кнопки "дальше" нет, метод get вернет None
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.good_parse)


    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[@itemprop='image'][1]/@srcset")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('specifications', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('values_specifications', "//dd[@class='def-list__definition']/text()")
        yield loader.load_item()

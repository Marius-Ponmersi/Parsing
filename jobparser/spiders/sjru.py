import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel = 'next']/@href").get()  # возвращается первое значение из списка
        if next_page:  # если кнопки "дальше" нет, метод get вернет None
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            "//div[@class = 'f-test-search-result-item']//a[contains(@href, 'vakansii')]/@href").getall()  # конвертируем список объектов в сптсок элеиентов
        for link in links:
            yield response.follow(link,
                                  callback=self.vacancy_parse)  # выполняет get-запрос на link, работает только в текущей сессии; callback = не ждет ответа от сервера, а работает дальше; yield - сохраняет сотояние нашего метода(не схлапывает его как return)

    def vacancy_parse(self, response: HtmlResponse):  # метод принимает ответы с get-запросов
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[contains(@class, 'f-test-vacancy-base-info')]//div/span[@class]/span/span[@class]/text()").getall()
        url = response.url  # та ссылка, на которой мы находимся
        yield JobparserItem(name=name, salary=salary, url=url)

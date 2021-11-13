import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1&experience=between1And3&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1&experience=between3And6&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1&experience=noExperience&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1&experience=moreThan6&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=2&industry=7&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=2&industry=15&industry=36&industry=50&industry=45&industry=51&industry=52&industry=19&industry=48&industry=24&industry=39&industry=47&industry=37&industry=5&industry=27&industry=388&industry=41&industry=29&industry=11&industry=13&industry=9&industry=42&industry=33&industry=389&industry=44&industry=49&industry=43&industry=34&industry=8&industry=46&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1217&area=1932&area=1008&area=1505&area=1817&area=1828&area=1716&area=1511&area=1739&area=1844&area=1941&area=1192&area=1754&area=1124&area=1463&area=1020&area=1859&area=1943&area=1471&area=1229&area=1661&area=1771&area=1438&area=1146&area=1308&area=1880&area=145&area=1890&area=2019&area=1061&area=1679&area=1051&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1202&area=1249&area=1563&area=1898&area=1575&area=1317&area=1948&area=1090&area=1422&area=1216&area=1347&area=1118&area=1424&area=1434&area=1553&area=1077&area=1041&area=2114&area=1620&area=1556&area=1174&area=1475&area=1624&area=1169&area=1187&area=1530&area=1704&search_field=description&search_field=company_name&search_field=name',
                  'https://barnaul.hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&area=1586&area=1596&area=1960&area=1261&area=1103&area=1481&area=1905&area=1783&area=1255&area=1913&area=1342&area=1646&area=1614&area=1975&area=1368&area=1384&area=1500&area=1652&area=1414&area=1806&search_field=description&search_field=company_name&search_field=name'
                  ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get() #возвращается первое значение из списка
        if next_page: #если кнопки "дальше" нет, метод get вернет None
            yield response.follow(next_page, callback=self.parse) #

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()  #конвертируем список объектов в сптсок элеиентов
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse) # выполняет get-запрос на link, работает только в текущей сессии; callback = не ждет ответа от сервера, а работает дальше; yield - сохраняет сотояние нашего метода(не схлапывает его как return)


    def vacancy_parse(self, response: HtmlResponse): # метод принимает ответы с get-запросов
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@class='vacancy-salary']/span/text()").getall()
        url = response.url #та ссылка, на которой мы находимся
        yield JobparserItem(name=name, salary=salary, url=url)

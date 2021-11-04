import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('127.0.0.1', 27017)
db = client['news']
yandex = db.yandex

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
response = requests.get('https://yandex.ru/news/') # headers=headers при указании заголовков - происходит пустая выдача
dom = html.fromstring(response.text)

items = dom.xpath("//article")
news = []

for item in items:
    novelty = {}

    source = item.xpath(".//a[@class = 'mg-card__source-link']/text()")
    name = item.xpath(".//a[@class='mg-card__link']//text()")
    link = item.xpath(".//a[@class='mg-card__link']/@href")
    date = item.xpath(".//span[@class = 'mg-card-source__time']/text()")

    novelty['source'] = source[0]
    novelty['name'] = name[0].replace('\xa0', ' ')
    novelty['link'] = link[0]
    novelty['date'] = date[0]
    novelty['_id'] = link[0]

    news.append(novelty)

    try:
        yandex.insert_one(novelty)
    except dke:
        print(f"Документ с id = {yandex}['_id'] уже существует в базе")

pprint(news)

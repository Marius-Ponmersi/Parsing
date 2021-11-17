# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from scrapy.utils.python import to_bytes

class LeroymerlinParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['lerua']

    def process_item(self, item, spider):
        _id = item['url']
        name = item['name']
        url = item['url']
        price = item['price']
        photos = item['photos']
        features = dict(zip(item['specifications'], item['values_specifications']))
        good_item = {'_id': _id, 'name': name, 'price': price, 'url': url, 'features': features, 'photos': photos}

        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(good_item)
        except dke:
            print(f"Документ с id = {collection}['_id'] уже существует в базе")
        return item

class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{item['name']}/{image_guid}.jpeg"

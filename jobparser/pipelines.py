# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import re
from unicodedata import normalize

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies1111']


    def process_item(self, item, spider):
        if item['salary']:
            item['salary'] = self.process_salary(item['salary'])
            salary_min = item['salary'][0]
            salary_max = item['salary'][1]
            valuta = item['salary'][2]

        _id = item['url']
        name = item['name']
        url = item['url']
        vacancy_item = {'_id': _id, 'name': name, 'salary_min': salary_min, 'salary_max': salary_max, 'valuta': valuta, 'url': url}
        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(vacancy_item)
        except dke:
            print(f"Документ с id = {collection}['_id'] уже существует в базе")

        return vacancy_item


    def process_salary(self, salary):
        salary = ' '.join(salary)
        salary = salary.replace("\xa0", "")
        nums = re.findall(r'\d+', salary)
        nums = [float(i) for i in nums]
        valuta = re.findall(r'\D+$', salary)[0]
        valuta = normalize('NFKD', valuta)

        if len(nums) == 2:
            salary_min = nums[0]
            salary_max = nums[1]
            valuta = valuta
        elif len(nums) == 1 and salary.find('от') == -1:
            salary_min = None
            salary_max = nums[0]
            valuta = valuta
        elif len(nums) == 1 and salary.find('до') == -1:
            salary_min = nums[0]
            salary_max = None
            valuta = valuta
        else:
            salary_min  = None
            salary_max = None
            valuta = valuta
        result = [salary_min, salary_max, valuta]
        return result




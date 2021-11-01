from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['jobs0111']
hh = db.hh
salary = float(input("Введите значение зарплаты: "))

def search_vacantion_salary(collection):
    for item in collection.find({'$or': [{'salary_min': {'$gt': salary}},
                                 {'salary_min': 'None', 'salary_max': {'$gt': salary}}]
                         }):
        pprint(item)

search_vacantion_salary(hh)

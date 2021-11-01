from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
from unicodedata import normalize

client = MongoClient('127.0.0.1', 27017)
db = client['jobs0111']
hh = db.hh

job = input("Введите профессию: ")
url = 'https://barnaul.hh.ru/search/vacancy'
page = 0
params = {'text': job,
          'clusters': 'true',
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'salary': '',
          'page': page}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def add_to_collection(collection):
    while True:
        response = requests.get(url, params=params, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacantions = dom.find_all('div', {'class': 'vacancy-serp-item'})

        if response.ok and vacantions:
            for vacantion in vacantions:
                vacantion_data = {}
                info = vacantion.find('a', {'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})
                link = info['href']
                name = info.string
                vacantion_data['name'] = name
                vacantion_data['link'] = link
                vacantion_data['_id'] = re.findall(r'\d+', link)[0]

                try:
                    salary_info = vacantion.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                    salary = salary_info.text
                    stroka = salary.replace("\u202f", "")
                    nums = re.findall(r'\d+', stroka)
                    nums = [float(i) for i in nums]
                    valuta = re.findall(r'\D+$', stroka)[0]
                    valuta = normalize('NFKD', valuta)

                    if len(nums) == 2:
                        vacantion_data['salary_min'] = nums[0]
                        vacantion_data['salary_max'] = nums[1]
                        vacantion_data['valuta'] = valuta

                    elif len(nums) == 1 and stroka.find('от') == -1:
                        vacantion_data['salary_min'] = None
                        vacantion_data['salary_max'] = nums[0]
                        vacantion_data['valuta'] = valuta
                    elif len(nums) == 1 and stroka.find('до') == -1:
                        vacantion_data['salary_min'] = nums[0]
                        vacantion_data['salary_max'] = None
                        vacantion_data['valuta'] = valuta
                    else:
                        vacantion_data['salary_min'] = None
                        vacantion_data['salary_max'] = None
                        vacantion_data['valuta'] = valuta
                except:
                    vacantion_data['salary_min'] = None
                    vacantion_data['salary_max'] = None
                    vacantion_data['valuta'] = None

                try:
                    collection.insert_one(vacantion_data)
                except dke:
                    print(f"Документ с id = {vacantion_data['_id']} уже существует в базе")

            print(f"{params['page']} pages processed")
            params['page'] += 1

        else:
            break

add_to_collection(hh)

for item in hh.find({}):
    pprint(item)

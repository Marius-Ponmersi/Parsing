import requests
import json

USERNAME = 'Marius-Ponmersi'

req = requests.get(f'https://api.github.com/users/{USERNAME}/repos')

data = req.text
with open('data_1.1.json', 'w') as write_f:
    json.dump(data, write_f)

data = json.loads(data)

for i in range(0, len(data)):
    print(f'Project Number: {i+1}')
    print(f'Project Name: {data[i]["name"]}')
    print(f'Project URL: {data[i]["svn_url"]}\n')

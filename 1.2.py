import requests
import json
from tok import tok

url = 'https://api.vk.com/method/groups.get?user_id=11245524&v=5.81'
my_params = {'access_token': tok,
             'extended': 1}

req = requests.get(url, params=my_params)
data = req.text

with open('groups_1_2.json', 'w') as write_f:
    json.dump(data, write_f)

data = json.loads(data)
group_list = []

for ind, i in enumerate(data.get('response').get('items'), 1):   # Только названме группы и Id
    print(f'{ind}. {i["name"]}, ID группы: {i["id"]}')
    group_list.append(f'{ind}. {i["name"]}, ID группы: {i["id"]}')

with open('groups_list_1_2.json', 'w') as write_f:
    json.dump(group_list, write_f)

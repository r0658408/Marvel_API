import datetime
import hashlib
import json
import requests

import pandas as pd

# Requirements
with open('key.json') as json_file:
    data = json.load(json_file)

public_key = data['public_key']
private_key = data['private_key']
ts = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')

# md5 hash processing
hash_md5 = hashlib.md5()
hash_md5.update('{}{}{}'.format(ts, private_key, public_key).encode('utf-8'))
hashed_params = hash_md5.hexdigest()

all_characters = []
offset = 0
total = 0
while True:
    print('Getting characters range {}-{} of {}'.format(offset + 1, offset + 100, total))
    params = {
        'ts': ts,
        'apikey': public_key,
        'hash': hashed_params,
        'limit': 100,
        'offset': offset
    }
    res = requests.get('https://gateway.marvel.com/v1/public/characters', params=params)
    json_res = res.json()
    results = json_res['data']['results']
    total = json_res['data']['total']
    for result in results:
        dict_data = {
            'id': result['id'],
            'name': result['name']
        }
        all_characters.append(dict_data)

    offset += 100
    if offset > total:
        break

df = pd.DataFrame(all_characters)
df.to_excel('characters.xlsx', index=False)

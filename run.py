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


def get_id(name):
    df = pd.read_excel('characters.xlsx')
    list_data = df.values.tolist()
    dict_data = {}
    for data in list_data:
        dict_data[data[1]] = data[0]
    return dict_data[name]


def get_comics(name, id):
    print('getting comics for {}'.format(name))
    all_results = []
    offset = 0
    total = 0
    while True:
        #print('Getting comics range {}-{} of {}'.format(offset + 1, offset + 100, total))
        params = {
            'ts': ts,
            'apikey': public_key,
            'hash': hashed_params,
            'limit': 100,
            'offset': offset
        }
        res = requests.get('https://gateway.marvel.com/v1/public/characters/{}/comics'.format(id), params=params)
        json_res = res.json()
        results = json_res['data']['results']
        total = json_res['data']['total']

        for result in results:
            dict_data = {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
                'isbn': result['isbn'],
                'format': result['format'],
                'page count': result['pageCount']

            }
            all_results.append(dict_data)

        offset += 100
        if offset > total:
            break

    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(all_results)
    blankIndex = [''] * len(df)
    df.index = blankIndex

    print('----------------------------------------------------------------')
    print(df)
    print('----------------------------------------------------------------')


def run():
    name = input('Getting details of comicbook character: ')
    try:
        id = get_id(name)
        get_comics(name, id)
    except KeyError:
        print('Sorry, "{}" not found'.format(name))


if __name__ == '__main__':
    run()

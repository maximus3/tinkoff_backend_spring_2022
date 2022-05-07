import base64
import time
from io import BytesIO
from PIL import Image

import requests


def get_task_json():
    with open('tests/data/big_original_base64.txt', 'r') as f:
        return {
            'data': f.read()
        }


def get_normal_task_json():
    with open('tests/data/normal_original_base64.txt', 'r') as f:
        return {
            'data': f.read()
        }


def get_broken_task_json():
    with open('tests/data/image_broken_base64.txt', 'r') as f:
        return {
            'data': f.read()
        }


data = [
    {'func': get_task_json, 'status': 'finished'},
{'func': get_broken_task_json, 'status': 'failed'},
    {'func': get_normal_task_json, 'status': 'finished'},
]


def main():

    for json_data in data:
        print(json_data)

        r = requests.post('http://localhost:8090/tasks/', json=json_data['func']())
        print(r, r.json())

        r = requests.get(f'http://localhost:8090/tasks/{r.json()["id"]}')
        print(r, r.json())

        while r.json()['status'] != json_data['status']:
            time.sleep(1)
            r = requests.get(f'http://localhost:8090/tasks/{r.json()["id"]}')
            print(r, r.json())

        if json_data['status'] != 'failed':
            task_id = r.json()['id']

            r = requests.get(f'http://localhost:8090/tasks/{task_id}/image?size=original')
            Image.open(BytesIO(base64.b64decode(r.json()))).show()

            r = requests.get(f'http://localhost:8090/tasks/{task_id}/image?size=32')
            Image.open(BytesIO(base64.b64decode(r.json()))).show()

            r = requests.get(f'http://localhost:8090/tasks/{task_id}/image?size=64')
            Image.open(BytesIO(base64.b64decode(r.json()))).show()

        print('Sleeping for 10sec...')
        time.sleep(10)


if __name__ == '__main__':
    main()

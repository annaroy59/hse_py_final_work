import json
import time
import requests


class GenerateImage:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model=None, images=1, width=1024, height=1024):
        print('Запускаем генерацию изображения')
        if model is None:
            model = self.get_model()
        params = {
            'style': 'ANIME',
            'type': 'GENERATE',
            'numImages': images,
            'width': width,
            'height': height,
            'generateParams': {
                'query': f'{prompt}'
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        max_attempts = attempts
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print(f'Попытка {max_attempts - attempts + 1}/{max_attempts}: статус {data['status']}')
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

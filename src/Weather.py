import requests
from datetime import datetime
from GenerateImage import GenerateImage
import base64
import os
from PIL import Image


def get_env_var(variable):
    env_res = os.getenv(variable)
    if env_res is None:
        print(f'Не найдена переменная окружения {variable}')
        exit()
    return env_res


def get_temp(city_name):
    weather_appid = get_env_var('weather_appid')
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': city, 'units': 'metric', 'APPID': weather_appid})
    data = res.json()
    if data['count'] == 0:
        print(f'Не удалось получить температуру по городу {city}')
        exit(0)
    res_temp = round(data['list'][0]['main']['temp'])
    print(f'В городе {city_name} сейчас {res_temp} градусов Цельсия')
    return res_temp


def create_pic(str_action):
    pic_apikey = get_env_var('pic_apikey')
    pic_secretkey = get_env_var('pic_secretkey')

    api = GenerateImage('https://api-key.fusionbrain.ai/', pic_apikey, pic_secretkey)
    uuid = api.generate(str_action)
    images = api.check_generation(uuid)

    if images is None:
        print('Не удалось сгенерировать изображение')
        exit()

    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    res_file_name = f"{os.getcwd()}/pics/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{pet}_{city}_{temp}.jpg"

    with open(res_file_name, "wb") as file:
        file.write(image_data)
    return res_file_name


def get_season():
    season = {12: "зимой", 1: "зимой", 2: "зимой",
              3: "весной", 4: "весной", 5: "весной",
              6: "летом", 7: "летом", 8: "летом",
              9: "осенью", 10: "осенью", 11: "осенью"}
    month = datetime.now().month
    return season[month]


# Начало
city = input('Введите город: ')
temp = get_temp(city)
pet = input('Введите животное: ')

action = f'{pet} гуляет в городе {city} при {temp} градусах Цельсия в национальном костюме {get_season()}'
print(action)

file_name = create_pic(action)

Image.open(file_name).show()
import os
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


URL = 'https://api.vk.com/method/'
VK_TOKEN = os.getenv("TOKEN")
USER_INPUT = input("Введите ссылку:")

def shorten_link(user_input, vk_token):
    method = 'utils.getShortLink'
    param = {
        'access_token': vk_token,
        'url': user_input,
        'v': '5.199'
    }
    response = requests.post(f'{URL}{method}', params=param)
    response.raise_for_status()
    short_link = response.json()
    if 'error' in short_link:
        error = short_link['error']['error_code']
        raise HTTPError(error)
    return short_link['response']['short_url']
    
def count_clicks(user_input, vk_token):
    method = 'utils.getLinkStats'
    param = {
        'access_token': vk_token,
        'key': urlparse(user_input).path[1:],
        'interval': 'week',
        'v': '5.199'
    }
    response = requests.post(f'{URL}{method}', params=param)
    response.raise_for_status()
    try:
        count = response.json()['response']['stats'][0]['views']
        return count
    except IndexError:
        return 0

    
def is_shorten_link(user_input, vk_token):
    if urlparse(user_input).netloc == 'vk.cc' and urlparse(user_input).path:
        utils = 'utils.getLinkStats'
        param = {
            'access_token': vk_token,
            'key': urlparse(user_input).path[1:],
            'v': '5.199'
        }
        response = requests.post(f'{URL}{utils}', params=param)
        response.raise_for_status()
        if 'error' in response.json():
            raise HTTPError('ссылка не действительна')
        return True
    return False

def main():
    try:
        if is_shorten_link(USER_INPUT, VK_TOKEN):
            print(f'Кол-во переходов:{count_clicks(USER_INPUT, VK_TOKEN)}')
        else:
            print('Сокращенная ссылка:', shorten_link(USER_INPUT, VK_TOKEN))
    except HTTPError as http_error:
        print(f'Ошибка ссылки: {http_error}')
    except KeyError:
        print('Ошибка в ссылке.')
    

if __name__ == '__main__':
  main()
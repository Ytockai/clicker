import os
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


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
    return response

    
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
            try:
                count = count_clicks(USER_INPUT, VK_TOKEN).json()['response']['stats'][0]['views']
            except IndexError:
                count = 0
            print(f'Кол-во переходов:{count}')
        else:
            print('Сокращенная ссылка:', shorten_link(USER_INPUT, VK_TOKEN))
    except HTTPError as http_error:
        print(f'Ошибка ссылки: {http_error}')
    except KeyError:
        print('Ошибка в ссылке.')
    

if __name__ == '__main__':
    URL = 'https://api.vk.com/method/'
    VK_TOKEN = os.environ["TOKEN"]
    USER_INPUT = input("Введите ссылку:")
    main()
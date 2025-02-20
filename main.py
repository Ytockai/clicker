import os
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse


URL = 'https://api.vk.com/method/'
VK_TOKEN = '56de17aa56de17aa56de17aad955f7babe556de56de17aa31738e30f4178c16c87b6474'

def shorten_link(user_input, VK_TOKEN):
    utils = 'utils.getShortLink'
    param = {
        'access_token': VK_TOKEN,
        'url': user_input,
        'v': '5.199'
    }
    response = requests.post(f'{URL}{utils}', params=param)
    response.raise_for_status()
    short_link = response.json()
    if 'error' in short_link:
        error = short_link['error']['error_code']
        raise HTTPError(error)
    return short_link['response']['short_url']
    
def count_clicks(flag, VK_TOKEN):
    utils = 'utils.getLinkStats'
    param = {
        'access_token': VK_TOKEN,
        'key': flag,
        'interval': 'forever',
        'v': '5.199'
    }
    response = requests.post(f'{URL}{utils}', params=param)
    response.raise_for_status()
    short_link = response.json()
    return short_link

    
def is_shorten_link(user_input, VK_TOKEN):
    if urlparse(user_input).netloc == 'vk.cc' and urlparse(user_input).path:
        utils = 'utils.getLinkStats'
        param = {
            'access_token': VK_TOKEN,
            'key': urlparse(user_input).path[1:],
            'v': '5.199'
        }
        response = requests.post(f'{URL}{utils}', params=param)
        response.raise_for_status()
        short_link = response.json()
        print(short_link)
        if 'error' in short_link:
            raise HTTPError('ссылка не действительна')
        elif urlparse(user_input).path:
            return urlparse(user_input).path[1:]
    return False

def main():
    user_input = input("Введите ссылку:")
    try:
        flag = is_shorten_link(user_input, VK_TOKEN)
        if not flag:
            link = shorten_link(user_input, VK_TOKEN)
            print('Сокращенная ссылка:', link)
        else:
            link = count_clicks(flag, VK_TOKEN)
            try:
                count = link['response']['stats'][0]['views']
                print('Количество переходов по ссылке:', count)
            except IndexError:
                print('Количество переходов по ссылке: 0')
    except HTTPError as http_error:
        print(f'Ошибка ссылки: {http_error}')
    except KeyError:
        print('Ошибка в ссылке.')
    

if __name__ == '__main__':
  main()
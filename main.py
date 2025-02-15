import os
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse


URL = 'https://api.vk.com/method/'
TOKEN = os.environ['TOKEN']

def shorten_link(user_input):
    utils = 'utils.getShortLink'
    param = {
        'access_token': TOKEN,
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
    
def count_clicks(flag):
    utils = 'utils.getLinkStats'
    param = {
        'access_token': TOKEN,
        'key': flag,
        'interval': 'forever',
        'v': '5.199'
    }
    response = requests.post(f'{URL}{utils}', params=param)
    response.raise_for_status()
    try:
        short_link = response.json()['response']['stats'][0]['views']
        return short_link
    except:
        return 0

    
def identify_link(user_input):
    if urlparse(user_input).netloc == 'vk.cc':
        path = urlparse(user_input).path[1:]
        return path
    return True

def main():
    user_input = input("Введите ссылку:")
    try:
        flag = identify_link(user_input)
        if flag == True:
            link = shorten_link(user_input)
            print('Сокращенная ссылка:', link)
        else:
            link = count_clicks(flag)
            print('Количество переходов по ссылке:', link)
    except HTTPError as http_error:
        print(f'Ошибка ссылки {http_error}')
    except KeyError:
        print('Ошибка в ссылке.')
    

if __name__ == '__main__':
  main()
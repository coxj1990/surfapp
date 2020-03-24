import requests
from os import environ

msw_key = environ['MSW_KEY']
msw_secret = environ['MSW_SECRET']

el_porto_id = 2677

def get_forecasts():
    params = {'spot_id': el_porto_id}
    base_url = 'http://magicseaweed.com/api/'
    url = base_url + msw_key + '/forecast/'
    r = requests.get(url, params)
    return r.json()

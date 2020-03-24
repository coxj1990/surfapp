import requests
from os import environ
from collections import namedtuple

LatLng = namedtuple('LatLng', 'lat lng')

msw_key = environ['MSW_KEY']
msw_secret = environ['MSW_SECRET']
world_tides_key = environ['WORLD_TIDES_KEY']

el_porto_id = 2677
el_porto_latlng = LatLng(lat=33.885090, lng=-118.409714)

meters_to_feet = 3.28084
world_tides_offset_ft = 2.75  # no idea why this is needed

def get_forecasts():
    base_url = 'http://magicseaweed.com/api/'
    url = base_url + msw_key + '/forecast/'
    params = {'spot_id': el_porto_id}
    r = requests.get(url, params)
    return r.json()

def get_tide(timestamp):
    url = 'https://worldtides.info/api?heights'
    params = {'lat': el_porto_latlng.lat,
              'lon': el_porto_latlng.lng,
              'start': timestamp,
              'key': world_tides_key}
    r = requests.get(url, params)
    height_m = r.json()['heights'][0]['height']
    return height_m * meters_to_feet + world_tides_offset_ft

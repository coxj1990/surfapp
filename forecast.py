import requests
import pytz
import datetime as dt
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

def get_forecast(timestamp):
    forecasts = get_forecasts()
    for idx, forecast in enumerate(forecasts):
        if forecast['timestamp'] > timestamp:
            return forecasts[idx - 1]

def get_tide(timestamp):
    url = 'https://worldtides.info/api?heights'
    params = {'lat': el_porto_latlng.lat,
              'lon': el_porto_latlng.lng,
              'start': timestamp,
              'key': world_tides_key}
    r = requests.get(url, params)
    height_m = r.json()['heights'][0]['height']
    return height_m * meters_to_feet + world_tides_offset_ft

def get_dawn_from_api(date_str):
    url = 'https://api.sunrise-sunset.org/json?'
    params = {'lat': el_porto_latlng.lat,
              'lng': el_porto_latlng.lng,
              'date': date_str}
    r = requests.get(url, params)
    dawn_str = r.json()['results']['civil_twilight_begin']
    return dt.datetime.strptime(date_str + " " + dawn_str,
                                "%Y-%m-%d %I:%M:%S %p")

def get_dawn():
    pacific = pytz.timezone('US/Pacific')
    tomorrow = dt.datetime.now(pacific) + dt.timedelta(days=1)
    dawn_utc = get_dawn_from_api(tomorrow.strftime("%Y-%m-%d"))
    timestamp = (dawn_utc - dt.datetime(1970, 1, 1)).total_seconds()
    dawn_pacific = pytz.utc.localize(dawn_utc).astimezone(pacific)
    return timestamp, dawn_pacific.strftime("%I:%M %p")

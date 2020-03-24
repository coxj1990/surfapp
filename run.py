import time
import pytz
import datetime as dt
from forecast import get_forecasts
from notify import send_message

too_much_swell_msg = "It's pumpin' tomorrow. Sleep in."
too_much_wind_msg = "Gonna be blown out tomorrow. Do some yoga instead."
success_msg = "Surf's up tomorrow."

def get_dawn_timestamp():
    pacific = pytz.timezone('US/Pacific')
    tomorrow = dt.datetime.now(pacific) + dt.timedelta(days=1)
    t = dt.time(hour=6, minute=0)
    dawn_time = dt.datetime.combine(tomorrow, t)
    pacific.localize(dawn_time).astimezone(pytz.utc)
    return time.mktime(dawn_time.timetuple())

def get_dawn_forecast():
    forecasts = get_forecasts()
    dawn_timestamp = get_dawn_timestamp()
    for idx, forecast in enumerate(forecasts):
        if forecast['timestamp'] > dawn_timestamp:
            return forecasts[idx - 1]

def under_swell_threshold(forecast, max_height_ft=4):
    return forecast['swell']['maxBreakingHeight'] <= max_height_ft

def under_wind_threshold(forecast, wind_speed_mph=5):
    return forecast['wind']['speed'] <= wind_speed_mph

def send_success_message(forecast):
    min_height_ft = str(forecast['swell']['minBreakingHeight'])
    max_height_ft = str(forecast['swell']['maxBreakingHeight'])
    wind_speed_mph = str(forecast['wind']['speed'])
    msg = success_msg + " Waves are " + min_height_ft + " to " + max_height_ft + \
        " feet with " + wind_speed_mph + " mile per hour winds."
    send_message(msg)

def main():
    forecast = get_dawn_forecast()
    if not under_swell_threshold(forecast):
        send_message(too_much_swell_msg)
    elif not under_wind_threshold(forecast):
        send_message(too_much_wind_msg)
    else:
        send_success_message(forecast)

if __name__ == '__main__':
    main()

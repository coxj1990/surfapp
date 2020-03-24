import time
import pytz
import datetime as dt
from forecast import get_forecasts, get_tide
from notify import send_message

too_much_swell_msg = "It's pumpin' tomorrow. Sleep in."
too_much_wind_msg = "Gonna be blown out tomorrow. Do some yoga instead."
too_high_tide_msg = "No surf tomorrow. Tide's too high."
success_msg = "Surf's up tomorrow."

def get_dawn_timestamp():
    pacific = pytz.timezone('US/Pacific')
    tomorrow = dt.datetime.now(pacific) + dt.timedelta(days=1)
    t = dt.time(hour=6, minute=0)
    dawn_time = dt.datetime.combine(tomorrow, t)
    pacific.localize(dawn_time).astimezone(pytz.utc)
    return time.mktime(dawn_time.timetuple())

def get_dawn_forecast(dawn_timestamp):
    forecasts = get_forecasts()
    for idx, forecast in enumerate(forecasts):
        if forecast['timestamp'] > dawn_timestamp:
            return forecasts[idx - 1]

def under_swell_threshold(forecast, max_height_ft=4):
    return forecast['swell']['maxBreakingHeight'] <= max_height_ft

def under_wind_threshold(forecast, wind_speed_mph=5):
    return forecast['wind']['speed'] <= wind_speed_mph

def under_tide_threshold(tide, max_height_ft=4):
    return tide <= max_height_ft

def send_success_message(forecast, tide):
    min_height_ft = str(forecast['swell']['minBreakingHeight'])
    max_height_ft = str(forecast['swell']['maxBreakingHeight'])
    wind_speed_mph = str(forecast['wind']['speed'])
    tide = str(round(tide, 1))
    msg = success_msg + " Waves are " + min_height_ft + " to " + \
            max_height_ft + " feet with " + wind_speed_mph + \
            " mile per hour winds. Tide is " + tide + " feet."
    send_message(msg)

def main():
    dawn_timestamp = get_dawn_timestamp()
    forecast = get_dawn_forecast(dawn_timestamp)
    tide = get_tide(dawn_timestamp)
    if not under_swell_threshold(forecast):
        send_message(too_much_swell_msg)
    elif not under_wind_threshold(forecast):
        send_message(too_much_wind_msg)
    elif not under_tide_threshold(tide):
        send_message(too_high_tide_msg)
    else:
        send_success_message(forecast, tide)

if __name__ == '__main__':
    main()

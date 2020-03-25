from forecast import get_dawn, get_forecast, get_tide
from notify import send_message

too_much_swell_msg = "It's pumpin' tomorrow. Sleep in."
too_much_wind_msg = "Gonna be blown out tomorrow. Do some yoga instead."
too_high_tide_msg = "No surf tomorrow. Tide's too high."
success_msg = "Surf's up tomorrow."

def under_swell_threshold(forecast, max_height_ft=4):
    return forecast['swell']['maxBreakingHeight'] <= max_height_ft

def under_wind_threshold(forecast, wind_speed_mph=5):
    return forecast['wind']['speed'] <= wind_speed_mph

def under_tide_threshold(tide, max_height_ft=4):
    return tide <= max_height_ft

def send_success_message(dawn_str, forecast, tide):
    min_height_ft = str(forecast['swell']['minBreakingHeight'])
    max_height_ft = str(forecast['swell']['maxBreakingHeight'])
    wind_speed_mph = str(forecast['wind']['speed'])
    tide_str = str(round(tide, 1))
    msg = success_msg + " Waves are " + min_height_ft + " to " + \
            max_height_ft + " feet with " + wind_speed_mph + \
            " mile per hour winds. Tide is " + tide_str + " feet. " + \
            "First light is at " + dawn_str + "."
    send_message(msg)

def main():
    dawn, dawn_str = get_dawn()
    forecast = get_forecast(dawn)
    tide = get_tide(dawn)
    if not under_swell_threshold(forecast):
        send_message(too_much_swell_msg)
    elif not under_wind_threshold(forecast):
        send_message(too_much_wind_msg)
    elif not under_tide_threshold(tide):
        send_message(too_high_tide_msg)
    else:
        send_success_message(dawn_str, forecast, tide)

if __name__ == '__main__':
    main()

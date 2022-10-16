import requests
import json

# Author: Renel Jean-Baptiste
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import config


class NoSuchLocation(Exception):
    pass


secret = config.key
api = config.api_key


def get_location():
    # Only accept numbers and length
    while True:

        try:
            zip_code = input("Please enter your Zip Code: ")
        except ValueError:

            # raise NoSuchLocation()
            print("Must be a five digit zip code...")
            continue

        else:

            if len(zip_code) == 5:
                location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                               f'postalcodes/search?apikey={secret}&q={zip_code}'

                response = requests.get(location_url)
                key = response.json()[0].get('Key')
                break

    return key


# display current conditions based on key

def get_conditions(key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/' \
                     f'?apikey={api}'.format(key)
    response = requests.get(conditions_url)
    json_version = response.json()
    print("Current Conditions: {}".format(json_version[0].get('WeatherText')))


# Get five day forecast

def get_5day_forecast(key):
    fivedayforecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' \
                          f'{key}?apikey={secret}'
    response = requests.get(fivedayforecast_url)
    json_version = response.json()

    # days_info = json_version.get("DailyForecasts")
    # Loops through json for temp info for each day
    for forecast in json_version["DailyForecasts"]:
        print("Weather Forecast for " + forecast["Date"])
        print("The minimum temperature(F) " + str(forecast["Temperature"]["Minimum"]["Value"]))
        print("The maximum temperature(F) " + str(forecast["Temperature"]["Maximum"]["Value"]))
        print("###################################################")


# method calls to get user input and store in key for further use

try:
    location_key = get_location()
    get_5day_forecast(location_key)

    # get_conditions(location_key)
except NoSuchLocation:
    print("Unable to get the location")

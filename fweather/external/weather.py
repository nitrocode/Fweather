import dotenv
import os
import requests
from urllib.parse import urlencode
import statistics as s


URL = 'https://api.worldweatheronline.com/premium/v1/weather.ashx?{}'
PARAMS = {
    'key': os.getenv('wwo'),
    # monthly climate average
    'mca': 'yes',
    # disable hourly weather data
    'fx': 'no',
    # obvious
    'format': 'json',
}


def search(query):
    """Hit endpoint and retrieve data

    :param query: typically zip code
    :return: json data in a dictionary
    """
    params = PARAMS.copy()
    params['q'] = query
    res = requests.get(URL.format(urlencode(params)))
    return res.json()['data']


def get_monthly_average_temps(data, celsius=False):
    """Return the monthly average temps from stored data.

    :return: monthly average temps
    """
    min_temp = 'avgMinTemp_F'
    max_temp = 'absMaxTemp_F'
    # drop the last 2 chars in the keys to get celsius
    if celsius:
        min_temp = min_temp[:-2]
        max_temp = max_temp[:-2]
    return [
        (float(month[min_temp]) + float(month[max_temp])) / 2.0
        for month in data['ClimateAverages'][0]['month']
    ]


def get_yearly_average_temp(data, celsius=False):
    """Return the yearly average temp from stored data.

    :return: yearly average temp
    """
    return s.mean(get_monthly_average_temps(data, celsius))


def get_current_temp(data, celsius=False):
    """Get the current temperature

    :return:
    """
    if not celsius:
        return float(data['current_condition'][0]['temp_F'])
    else:
        return float(data['current_condition'][0]['temp_C'])


def get_current_weather_desc(data):
    """Get the current weather description. These values are undocumented.

    :param data:
    :return: e.g. 'Partly Cloudy', 'Light Rain'
    """
    return data['current_condition'][0]['weatherDesc'][0]['value']


def is_raining(data):
    """Check if it's raining.

    :param data:
    :return:
    """
    return 'rain' in get_current_weather_desc(data).lower()


def get_current_weather_icon(data):
    """Get WWO's weather icon.

    :param data:
    :return: image to include in the email
    """
    return data['current_condition'][0]['weatherIconUrl'][0]['value']


if __name__ == '__main__':
    # load env vars
    dotenv.read_dotenv()

    zip_code = '20001'

    w_data = search(zip_code)
    mean = get_yearly_average_temp(w_data)
    current = get_current_temp(w_data)

    print('Weather for {} is {}'.format(zip_code, current))
    print('mean temp is {}'.format(mean))

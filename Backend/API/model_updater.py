import joblib
from source.isw.isw_requester import ISWRequester
from source.weather.weather_collector import WeatherCollector





def get_weather_data():
    weather_collector = WeatherCollector()
    weather_data = weather_collector.weather_data
    return weather_data

def get_isw():
    isw = ISWRequester()
    return isw.data_vect

def

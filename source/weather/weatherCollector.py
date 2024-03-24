import requests
from datetime import datetime

class WeatherCollector:
    def __init__(self, date_range: tuple, api_key: str):
        self.start_date = date_range[0]
        self.end_date = date_range[1]
        self.api_key = api_key



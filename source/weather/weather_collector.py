from datetime import datetime, timedelta
import requests
import os
import csv

class WeatherCollector:
    def __init__(self, date):
        self.__vector = None
        self.__key = self.read_key()
        # self._data = self.make_request()
        self.__date = date
        # self.__url =  f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{date1}/{date2}?key={key}"
        self.__locations =  ["Kyiv", "Rivne", "Lutsk", "Lviv", "Zhytomyr",
                 "Chernivtsi", "Ivano-Frankivsk", "Ternopil", "Khmelnytskyi",
                 "Uzhhorod", "Vinnytsia", "Cherkasy", "Poltava", "Chernihiv",
                 "Sumy", "Kharkiv", "Kropyvnytskyi", "Dnipro", "Mykolaiv",
                 "Kharkiv", "Luhansk", "Donetsk", "Odesa", "Chernihiv",
                 "Kherson"]
        self.__responses = self.request()
        self.__data = self.get_data()

    @property
    def vector(self):
        return self.__vector

    @vector.setter
    def vector(self, vector):
        self.__vector = vector

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def date(self):
        return self.__date

    @property
    def locations(self):
        return self.__locations

    @property
    def response(self):
        return self.

    @staticmethod
    def read_key():
        with open("api_key.txt", "r") as f:
            api_key = f.readline()

    def request(self):
        next_day = self.date + timedelta(days=1)
        result = []
        for location in self.locations:
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{self.date.strftime("%Y-%m-%d")}/{next_day.strftime("%Y-%m-%d")}?key={self.key}"
            r = requests.get(url)
            result.append(r.json())

    def get_data(self):
        for data in self.response:
            if 'days' in data:
                with open(output_file, "w", encoding="utf-8") as :


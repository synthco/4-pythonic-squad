from datetime import datetime, timedelta
import requests
import os
import pandas as pd

class WeatherCollector:
    def __init__(self, date):
        self.__key = self.read_key()
        self.__date = date
        self.__locations = ["Kyiv", "Rivne", "Lutsk", "Lviv", "Zhytomyr",
                            "Chernivtsi", "Ivano-Frankivsk", "Ternopil", "Khmelnytskyi",
                            "Uzhhorod", "Vinnytsia", "Cherkasy", "Poltava", "Chernihiv",
                            "Sumy", "Kharkiv", "Kropyvnytskyi", "Dnipro", "Mykolaiv",
                            "Kharkiv", "Luhansk", "Donetsk", "Odesa", "Chernihiv",
                            "Kherson"]
        self.__weather_data = None
        self.__data = self.fetch_weather_data()

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
    def data(self):
        return self.__data

    @property
    def weather_data(self):
        return self.__weather_data

    @staticmethod
    def read_key():
        with open("api_key.txt", "r") as f:
            api_key = f.readline()
        return api_key.strip()



    def fetch_weather_data(self, location):
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{date1}/{date2}?key={key}"
        response = requests.get(url)
        data = response.json()
    def fetch_weather_data(self):
        try:
            next_day = self.date + timedelta(days=1)
            weather_data = pd.DataFrame()
            for location in self.locations:
                new_data = self.clear_df(location, self.key, self.date.strftime("%Y-%m-%d"), next_day.strftime("%Y-%m-%d"))
                if new_data is not None:
                    weather_data = pd.concat([weather_data, new_data], ignore_index=True)
            self.__weather_data = weather_data
            return weather_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def clear_df(self, location, key, date1, date2):
        try:
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{date1}/{date2}?key={key}"
            response = requests.get(url)
            data = response.json()
            if 'days' in data:
                daily_data = data['days']
                hour_keys = set()

                for day_data in daily_data:
                    hourly_data = day_data.get('hours', [])
                    for hour_data in hourly_data:
                        hour_keys.update(hour_data.keys())

                weather_df = pd.DataFrame(columns=list(data.keys()) + list(daily_data[0].keys()) + list(hour_keys))
                for day in daily_data:
                    day_values = [day.get(key, "") for key in daily_data[0].keys()]
                    for hour in day["hours"]:
                        hour_values = [hour.get(key, "") for key in hour_keys]
                        row = {**data, **dict(zip(daily_data[0].keys(), day_values)), **hour}
                        print(weather_df)
                        print('-'*12)
                        weather_df = pd.concat([weather_df, pd.DataFrame([row])])

                weather_df.reset_index(drop=True, inplace=True)  # Resetting index
                return weather_df
            else:
                return None
        except Exception as e:
            print(f"An error occurred while processing data for {location}: {e}")
            return None


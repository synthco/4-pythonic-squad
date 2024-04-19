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

    def fetch_weather_data(self):
        try:
            next_day = self.__date + timedelta(days=1)
            weather_data = pd.DataFrame()
            for location in self.__locations:
                print(f"Processing location: {location}")
                new_data = self.clear_df(location)
                if new_data is not None:
                    weather_data = pd.concat([weather_data, new_data], ignore_index=True)
                    self.__weather_data = weather_data
                    self.correction()
            return weather_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def clear_df(self, location):
        try:
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{self.__date.strftime('%Y-%m-%d')}/{(self.__date + timedelta(days=1)).strftime('%Y-%m-%d')}?key={self.__key}"
            response = requests.get(url)
            data = response.json()

            if 'days' in data:
                daily_data = data['days']
                hourly_data = []

                for day_data in daily_data:
                    hourly_data.extend(day_data.get('hours', []))

                others = {key: data[key] for key in
                          ['latitude', 'longitude', 'resolvedAddress', 'address', 'timezone', 'tzoffset']}

                rows = []

                for day in daily_data:
                    day_values = {k: day.get(k, '') for k in day.keys()}

                    for hour in day["hours"]:
                        hour_values = {f"{key}_hourly": hour.get(key, '') for key in hour.keys()}

                        row = {**others, **day_values, **hour_values}
                        rows.append(row)

                weather_df = pd.DataFrame(rows)
                return weather_df
            else:
                return None
        except Exception as e:
            print(f"An error occurred while processing data for {location}: {e}")
            return None

    def find_datetime(self, time):
        # splitting the time input and finding the int value of current hour and return it
        current = int(time.split("-")[0])
        for hour in range(24):
            if hour == current:
                return hour
        return 0

    def correction(self):
        try:
            # current time
            current_time = datetime.now()

            # end time (current time + 12 hours)
            end_time = current_time + timedelta(hours=12)

            self.__weather_data['datetime_hourly'] = pd.to_datetime(self.__weather_data['datetime_hourly'])
            corrected_data = pd.DataFrame()

            # аpply correction for each group (location)
            for location, group in self.__weather_data.groupby('address'):
                timecut = current_time.strftime("%H-00-00")
                cut = self.find_datetime(timecut)
                filtered_group = group.iloc[(cut-1):cut + 11]

                # сonverting temperature values
                columns_convert = ['tempmax', 'temp', 'tempmin', 'feelslike', 'feelslikemax', 'feelslikemin']
                filtered_group[columns_convert] = (filtered_group[columns_convert] - 32) * (5 / 9)

                # сhanging names for hourly columns
                filtered_group.rename(columns=lambda col: col.replace(".1", "_hourly"), inplace=True)

                filtered_group = filtered_group.fillna(0)
                columns_to_drop = ["sunsetEpoch_hourly", "moonphase_hourly", "sunrise_hourly", "sunset_hourly",
                                   "sunriseEpoch_hourly", "hours"]
                filtered_group = filtered_group.drop(columns_to_drop, axis=1, errors='ignore')
                corrected_data = pd.concat([corrected_data, filtered_group], ignore_index=True)

            self.__weather_data = corrected_data

            print("Correction applied successfully.")
        except Exception as e:
            print(f"An error occurred while applying correction: {e}")

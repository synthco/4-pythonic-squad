import numpy as np
from sklearn.preprocessing import OneHotEncoder
from source.isw.isw_requester import ISWRequester
from source.weather.weather_collector import  WeatherCollector
from datetime import datetime
import pandas as pd
import pickle
import joblib



class Dfender:
    """
    Date in format YYYY-MM-DD or in Datetime object
   """

    def __init__(self, date=None):

        # Date processing
        if date is None:
            self.__date = datetime.now()
        elif type(date) is not datetime:
            try:
                self.__date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError as e:
                print(f"Date format not valid: {e}")
                print("Date in format YYYY-MM-DD or in Datetime object")

        self.__isw_vector = self.request_isw()

        # self.__weather_vector = pd.read_csv("Weather.csv")
        self.__weather_vector = self.request_weather()
#
        self.city_id_map = {
            'Вінниця': 2,
            'Луцьк': 3,
            'Дніпро': 4,
            'Донецьк': 5,
            'Житомир': 6,
            'Ужгород': 7,
            'Запоріжжя': 8,
            'Івано-Франківськ': 9,
            'Київ': 10,
            'Кропивницький': 11,
            'Луганськ': 12,
            'Львів': 13,
            'Миколаїв': 14,
            'Одеса': 15,
            'Полтава': 16,
            'Рівне': 17,
            'Суми': 18,
            'Тернопіль': 19,
            'Харків': 20,
            'Херсон': 21,
            'Хмельницька область': 22,
            'Черкаси': 23,
            'Чернівці': 24,
            'Чернігів': 25}
        self.weather_data_exclude = ['resolvedAddress',
                                'datetimeEpoch',
                                'feelslikemax',
                                'feelslikemin',
                                'feelslike',
                                'sunriseEpoch',
                                'sunsetEpoch',
                                'moonphase',
                                'description',
                                'icon',
                                'stations',
                                'source',
                                'datetime_hourly',
                                'datetimeEpoch_hourly',
                                'feelslike_hourly',
                                'source_hourly',
                                'stations_hourly',
                                'icon_hourly',
                                'sunrise',
                                'sunset',
                                'latitude',
                                'longitude',
                                'resolvedAddress',
                                'address',
                                'timezone',
                                'tzoffset',
                                'precipprob',
                                'preciptype',
                                'snow',
                                'snowdepth',
                                'windgust',
                                'windspeed',
                                'winddir',
                                'pressure',
                                'cloudcover',
                                'visibility',
                                'severerisk',
                                'conditions',
                                'conditions_hourly'
                                ]
        self.precip_type_mapping = {
    "['snow']": 1,
    0: 0,
    "['rain']": 2,
    "['rain', 'snow']": 3,
    "['freezingrain']": 4,
    "['ice']": 5
}


        self.__vector = self.full_merge()

        self.__result = self.predict()

    @property
    def date(self):
        return self.__date

    @property
    def isw_vector(self):
        return self.__isw_vector

    @property
    def weather_vector(self):
        return self.__weather_vector

    @property
    def vector(self):
        return self.__vector

    @property
    def result(self):
        return self.__result


    def __repr__(self):
        res = {
            "date": self.date,
            "isw": self.isw_vector,
            "weather": self.weather_vector
        }
        return str(res)

    @staticmethod
    def request_isw():
        requester = ISWRequester()
        return requester.data_vect

    def request_weather(self):
        weather_requester = WeatherCollector(self.date)
        return weather_requester.weather_data

    def full_merge(self, xgb=None):
        weather = self.weather_vector
        isw = self.isw_vector

        weather['resolvedAddress'] = weather['resolvedAddress'].str.split(',').str[0]
        weather.insert(loc=3, column='region_id', value=weather['resolvedAddress'].map(self.city_id_map).astype(int))
        weather = weather.drop(self.weather_data_exclude, axis=1)
        weather['preciptype_hourly'] = weather['preciptype_hourly'].replace(self.precip_type_mapping)
        weather['solarradiation_hourly'] = weather['solarradiation_hourly'].fillna(-1)
        weather['solarenergy_hourly'] = weather['solarenergy_hourly'].fillna(-1)
        weather['uvindex_hourly'] = weather['uvindex_hourly'].fillna(-1)
        weather = weather.rename(columns={'datetime': 'date'})
        weather['date'] = pd.to_datetime(weather['date'])

        isw['date'] = pd.to_datetime(isw['date'])
        isw['date'] += pd.Timedelta(days=1)

        isw['key'] = 1
        weather['key'] = 1

        merged_df = pd.merge(weather, isw, on='key')
        merged_df.drop(columns=['key', "date_x", "date_y", "preciptype_hourly"], inplace=True)
        columns_to_drop = ['windgust_hourly', 'dew', 'humidity_hourly', 'temp_hourly',
                           'snow_hourly', 'temp', 'pressure_hourly', 'dew_hourly', 'solarenergy_hourly',
                           'visibility_hourly', 'cloudcover_hourly', 'severerisk_hourly', 'solarenergy',
                           'solarradiation', 'snowdepth_hourly', 'precip', 'precip_hourly',
                           'precipprob_hourly', 'winddir_hourly', 'humidity', 'tempmax', 'uvindex',
                           'solarradiation_hourly', 'uvindex_hourly', 'precipcover', 'tempmin',
                           'windspeed_hourly']

        merged_df.drop(columns=columns_to_drop, inplace=True)

        grid_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        # grid_df = pd.DataFrame({'region_id': grid_values})
        encoder = OneHotEncoder(sparse_output=False, categories=[grid_values])

        one_hot_encoded = encoder.fit_transform(merged_df[['region_id']])

        encoded_df_oh = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(['region_id']))

        missing_values_df = pd.DataFrame(0, index=np.arange(len(merged_df)),
                                         columns=[f'region_id_{value}' for value in grid_values])

        encoded = pd.concat([merged_df, encoded_df_oh], axis=1)

        for value in grid_values:
            if f'region_id_{value}' not in encoded.columns:
                encoded[f'region_id_{value}'] = 0
        encoded = encoded.drop(['region_id', "region_id_12"], axis=1)

        columns_to_create = ['hour_humidity', 'hour_precipprob', 'hour_severerisk', 'day_temp',
                             'day_solarenergy', 'day_precipcover', 'hour_windgust', 'day_humidity',
                             'hour_dew', 'hour_windspeed', 'hour_solarradiation', 'day_dew',
                             'hour_solarenergy', 'hour_snow', 'day_precip', 'hour_pressure',
                             'day_tempmin', 'hour_visibility', 'hour_uvindex', 'hour_snowdepth',
                             'hour_winddir', 'hour_precip', 'day_solarradiation', 'hour_preciptype',
                             'day_tempmax', 'hour_cloudcover', 'day_uvindex', 'hour_temp']

        # Create columns and fill them with 0
        for col in columns_to_create:
            encoded[col] = 0


        with open("/Users/ivantyshchenko/Documents/GitHub/4-pythonic-squad/Backend/API/ordered_keys.pkl", 'rb+') as f:
            ordered_keys = pickle.load(f)
            print('Keys loaded')


        pred_data2_ordered = {k: encoded[k] for k in ordered_keys if k in encoded}
        pred_data2_ordered_df = pd.DataFrame(pred_data2_ordered)

        # dtest = xgb.DMatrix(pred_data2_ordered_df)

        return pred_data2_ordered_df

    def predict(self):
        # xgboost = pickle.load(open('XGBoost_model_v3.pkl', 'wb'))
        with open("/Users/ivantyshchenko/Documents/GitHub/4-pythonic-squad/Backend/API/XGBoost_model.pkl", 'rb+') as f:
            try:
                model = joblib.load(f)
                print('Model loaded')
            except FileNotFoundError:
                print("XGBoost model file not found.")

        prediction = model.predict(self.vector)
        print(type(prediction))
        return prediction




# from dfender import Dfender
# import subprocess
#
#
# def test_dfender():
#     dfender = Dfender()
#     # df1 = dfender.isw_vector
#     df2 = dfender.weather_vector
#     #
#     # df1.to_csv("ISW.csv", index=False)
#     # df2.to_csv("Weather.csv", index=False)
#     df = dfender.vector
#     # df.to_csv('predict_vector.csv')
#     print(dfender.result)
#
#     # print(dfender)
#
#
# if __name__ == '__main__':
#     # Виконати команду pip для встановлення пакету xgboost
#     subprocess.run(["pip", "install", "xgboost"])
#
#     print("XGBoost successfully installed!")
#     test_dfender()

import os
os.system('pip install flask')
import datetime
from flask import Flask, jsonify, request
from Backend.API.dfender import Dfender
import requests
import json



app = Flask(__name__)
#enter your custom token here
API_TOKEN = "123"

#endpoint
@app.route("/predict", methods=['POST'])
def predict():
    json_data = request.get_json()

    if json_data is None:
        raise InvalidUsage("Request data is missing or not in JSON format", status_code=400)

    locations = json_data.get("locations")
    if locations is None:
        raise InvalidUsage("Locations are required fields", status_code=400)

    token = json_data.get("token")
    if token != API_TOKEN:
        raise InvalidUsage("Wrong API token", status_code=403)
    dfender = Dfender()
    prediction_array = dfender.result

    city_id_map = [
        'Vinnytsia',
        'Lutsk',
        'Dnipro',
        'Donetsk',
        'Zhytomyr',
        'Uzhhorod',
        'Zaporizhzhia',
        'Ivano-Frankivsk',
        'Kyiv',
        'Kropyvnytskyi',
        'Lviv',
        'Mykolaiv',
        'Odesa',
        'Poltava',
        'Rivne',
        'Sumy',
        'Ternopil',
        'Kharkiv',
        'Kherson',
        'Khmelnytskyi Oblast',
        'Cherkasy',
        'Chernivtsi',
        'Chernihiv'
    ]

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    result = {}

    for loc in locations:
        if loc in city_id_map:
            cut = city_id_map.index(loc)
            delta = 12 * (cut - 1)
            alarm_data = prediction_array[delta:(delta + 11)]
            is_alarm = [True if value != 0 else False for value in alarm_data]
            result[loc] = {
                "from time": current_time,
                "is_alarm": is_alarm
            }
    # print(result)
    return result

    # creating right output format via our data
    # data = output_rows(dfender)

    # return dfender
    #

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA team 4: API Alarms.</h2></p>"


if __name__ == "__main__":
    app.run(debug=True)
    # predict()
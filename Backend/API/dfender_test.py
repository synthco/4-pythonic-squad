
import os
os.system('pip install flask')
import datetime
from flask import Flask, jsonify, request
from Backend.API.dfender import Dfender
import requests
import json
import pandas as pd


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

    df = pd.read_csv("predictions.csv")

    for loc in locations:
        if loc in city_id_map:
            alarms = {}
            for index, row in df.iterrows():
                time = row['hour_datetime']
                date = row['date']
                key = date + " " + time
                is_alarm = row[loc] != 0
                alarms[key] = is_alarm
            result[loc] = alarms

    print(result)
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

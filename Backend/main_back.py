from flask import Flask, jsonify, request
from Backend.API.dfender import Dfender
import requests
import json



app = Flask(__name__)
#enter your custom token here
API_TOKEN = "123"
#your personal key here
key = "9AJTDWYQN4BA9QE8BD2U3A7QQ"

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

    city_id_map = {
        'Vinnytsia': 2,
        'Lutsk': 3,
        'Dnipro': 4,
        'Donetsk': 5,
        'Zhytomyr': 6,
        'Uzhhorod': 7,
        'Zaporizhzhia': 8,
        'Ivano-Frankivsk': 9,
        'Kyiv': 10,
        'Kropyvnytskyi': 11,
        'Lviv': 13,
        'Mykolaiv': 14,
        'Odesa': 15,
        'Poltava': 16,
        'Rivne': 17,
        'Sumy': 18,
        'Ternopil': 19,
        'Kharkiv': 20,
        'Kherson': 21,
        'Khmelnytskyi Oblast': 22,
        'Cherkasy': 23,
        'Chernivtsi': 24,
        'Chernihiv': 25
    }

    result = {}
    for loc in locations:
        if loc in city_id_map:
            n = city_id_map[loc]
            cut = prediction_array[n - 1]
            location_data = prediction_array[n - 1: n + 11]
            result[loc] = {"data": location_data}

    return result



    # creating right output format via our data
    # data = output_rows(dfender)

    return dfender
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
    return "<p><h2>KMA team 6: API Alarms.</h2></p>"


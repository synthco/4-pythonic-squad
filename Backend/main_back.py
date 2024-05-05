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
    # getting data from json doc and creating new vars using it
    requester_name = json_data.get("requester_name")
    locations = json_data.get("locations")
    # checking if toker is correct and is present, checking if other required members are present, etc.
    if locations is None:
        raise InvalidUsage("locations is required fields", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)


    dfender = Dfender()

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

